from NNMCTS import state
import random
import time
import numpy as np
from copy import deepcopy
import math
import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Input, Dense, Conv2D, BatchNormalization, Add, Concatenate, Flatten
from tensorflow.keras.models import Model, save_model, load_model
from tensorflow.keras.losses import mean_squared_error, categorical_crossentropy
def loss(y_true, y_pred):
    mask = np.zeros((1, 362))
    mask[0][-1] = 1
    value_loss = mean_squared_error(mask*y_true, mask*y_pred)
    mask = 1-mask
    policy_loss = K.sum(categorical_crossentropy(mask*y_true, mask*y_pred))
    return policy_loss+value_loss
model = load_model("Connect6.h5", compile=False)
model.compile(optimizer="adam", loss=loss)
c = 5
temperature = 1
class connect6():
    def __init__(self):
        self.moveset  = [[i, j] for i in range(19) for j in range(19)]
        self.players = [-1, 1]
    def getplayer(self, turn):
        m4 = turn%4
        if(m4 in [0, 1]):
            return -1
        return 1
    def getboard(self, move, board, player):
        assert board[move[0]][move[1]]==0
        board[move[0]][move[1]] = player
        return board
    def movelegal(self, board, move):
        return board[move[0]][move[1]]==0
    '''
    def game_finished(board, lastmove, depth):
        for i in range(len(board)):
            for j in range(len(board[i])-5):
                if([board[i][j] for k in range(6)]==[board[i][j+k] for k in range(6)] and board[i][j]!=0):
                    return True, board[i][j]
        for i in range(len(board)-5):
            for j in range(len(board[i])):
                if([board[i][j] for k in range(6)]==[board[i+k][j] for k in range(6)] and board[i][j]!=0):
                    return True, board[i][j]
        for i in range(5, len(board)):
            for j in range(len(board[i])-5):
                if([board[i][j] for k in range(6)]==[board[i-k][j+k] for k in range(6)] and board[i][j]!=0):
                    return True, board[i][j]
        for i in range(5, len(board)):
            for j in range(5, len(board[i])):
                if([board[i][j] for k in range(6)]==[board[i-k][j-k] for k in range(6)] and board[i][j]!=0):
                    return True, board[i][j]
        zeros = 0
        for i in board:
            zeros+=i.count(0)
        if(zeros==0):
            return True, 0
        return False, 0
    '''
    def game_finished(self, board, lastmove, depth):
        if(depth==210): #speed
            return True, 0
        if(lastmove is None):
            return False, 0

        mlen = 0
        ccolor = board[lastmove[0]][lastmove[1]]
        move = lastmove.copy()
        while(move[0]<19 and move[0]>0 and mlen<6 and board[move[0]][move[1]]==ccolor):
            move[0]+=1
            mlen+=1
        move = lastmove.copy()
        move[0]-=1
        while(move[0]<19 and move[0]>0 and mlen<6 and board[move[0]][move[1]]==ccolor):
            move[0]-=1
            mlen+=1
        if(mlen==6):
            return True, ccolor

        mlen = 0
        move = lastmove.copy()
        while(move[1]<19 and move[1]>0 and mlen<6 and board[move[0]][move[1]]==ccolor):
            move[1]+=1
            mlen+=1
        move = lastmove.copy()
        move[1]-=1
        while(move[1]<19 and move[1]>0 and mlen<6 and board[move[0]][move[1]]==ccolor):
            move[1]-=1
            mlen+=1
        if(mlen==6):
            return True, ccolor

        mlen = 0
        move = lastmove.copy()
        while(move[0]<19 and move[0]>0 and move[1]<19 and move[1]>0 and mlen<6 and board[move[0]][move[1]]==ccolor):
            move[1]+=1
            move[0]+=1
            mlen+=1
        move = lastmove.copy()
        move[1]-=1
        move[0]-=1
        while(move[0]<19 and move[0]>0 and move[1]<19 and move[1]>0 and mlen<6 and board[move[0]][move[1]]==ccolor):
            move[1]-=1
            move[0]-=1
            mlen+=1
        if(mlen==6):
            return True, ccolor

        mlen = 0
        move = lastmove.copy()
        while(move[0]<19 and move[0]>0 and move[1]<19 and move[1]>0 and mlen<6 and board[move[0]][move[1]]==ccolor):
            move[1]+=1
            move[0]-=1
            mlen+=1
        move = lastmove.copy()
        move[1]-=1
        move[0]+=1
        while(move[0]<19 and move[0]>0 and move[1]<19 and move[1]>0 and mlen<6 and board[move[0]][move[1]]==ccolor):
            move[1]-=1
            move[0]+=1
            mlen+=1
        if(mlen==6):
            return True, ccolor
        return False, 0
    def getnninp(self, board, player):
        playerinp = np.ones((19, 19, 1))*player
        p1inp = []
        p2inp = []
        for i in board:
            temp1 = []
            temp2 = []
            for j in i:
                if(j==1):
                    temp1.append([1])
                else:
                    temp1.append([0])
                if(j==-1):
                    temp2.append([1])
                else:
                    temp2.append([0])
            p1inp.append(temp1)
            p2inp.append(temp2)
        p1inp = np.array(p1inp)
        p2inp = np.array(p2inp)
        inp = np.concatenate((playerinp, p1inp, p2inp), axis=-1).reshape((1, 19, 19, 3))
        return inp
    def getnnstuff(self, board, player):
        inp = self.getnninp(board, player)
        inp2 = self.getnninp(board, player*-1)
        inp = np.concatenate((inp, inp2))
        nnout = model.predict(inp)
        policy = nnout[0][:-1]
        value1 = nnout[0][-1]
        value2 = nnout[1][-1]
        return policy, {player: value1, -1*player: value2}
def get_visits(board, turn, its, game):
    i_state = state(board, turn, c, game)
    depth = 0
    for its in range(its):
        k = 0
        sim_state = i_state
        leaf = sim_state.is_leaf()
        while(not leaf):
            sim_state = sim_state.choose_child()
            leaf = sim_state.is_leaf()
            k+=1
        sim_state.get_board()
        finished = game.game_finished(sim_state.board, sim_state.move, k)[0]
        if(leaf):
            nnstuff = game.getnnstuff(sim_state.board, sim_state.player)
            for i in nnstuff[1]:
                sim_state.V[i] = nnstuff[1][i]
            if(not finished):
                for i, j in enumerate(game.moveset):
                    if(game.movelegal(sim_state.board, j)):
                        new_state = sim_state.new_child(j, nnstuff[0][i])
                        new_state.parent.add_child(new_state)
                k+=1
        i_state = sim_state.backprop()
        depth = max([depth, k])
    return [i.visits for i in i_state.children], depth, i_state.visits, [i.move for i in i_state.children]
game = connect6()
n_games = 0
while True:
    t = time.time()
    board = [[0 for i in range(19)] for j in range(19)]
    turn = -1
    finished = False
    p1inps = []
    p2inps = []
    p1policies = []
    p2policies = []
    while(not finished):
        mcts = get_visits(board, turn, 512, game)
        visits = mcts[0]
        moves = mcts[3]
        policy = np.array(visits)**(1/temperature)
        policy/=sum(policy)
        fpolicy = np.zeros(361)
        for i, j in enumerate(moves):
            fpolicy[j[0]+j[1]*19] = policy[i]
        if(game.getplayer(turn)==1):
            p1inps.append(game.getnninp(board, game.getplayer(turn))[0])
            p1policies.append(np.array(fpolicy))
        else:
            p2inps.append(game.getnninp(board, game.getplayer(turn))[0])
            p2policies.append(np.array(fpolicy))
        policy = policy.tolist()
        move = moves[random.choices(range(len(policy)), weights=policy, k=1)[0]]
        board = game.getboard(move, board, game.getplayer(turn))
        turn+=1
        finished = game.game_finished(board, move, turn+1)[0]
    winner = game.game_finished(board, move, turn+1)[1]
    if(winner==0):
        p1reward = 0
        p2reward = 0
    else:
        p1reward = (winner==1)*2-1
        p2reward = -1*p1reward
    for i in range(len(p1policies)):
        p1policies[i] = np.append(p1policies[i], p1reward)
    for i in range(len(p2policies)):
        p2policies[i] = np.append(p2policies[i], p2reward)
    p1inps = np.array(p1inps)
    p2inps = np.array(p2inps)
    p1policies = np.array(p1policies)
    p2policies = np.array(p2policies)
    print(model.train_on_batch(p1inps, p1policies))
    print(model.train_on_batch(p2inps, p2policies))
    print(game.game_finished(board, move, turn+1)[1])
    n_games+=1
    print(n_games)
    print(time.time()-t)
