from NNMCTS import state
import random
import time
import numpy as np
import math
import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Input, Dense, Conv2D, BatchNormalization, Add, Concatenate, Flatten
from tensorflow.keras.models import Model, save_model, load_model
from tensorflow.keras.losses import mean_squared_error, categorical_crossentropy
def loss(y_true, y_pred):
    mask = np.zeros((1, 362))
    mask[-1] = 1
    value_loss = mean_squared_error(K.sum(mask*y_true, axis=-1), K.sum(mask*y_pred, axis=-1))
    mask = 1-mask
    policy_loss = categorical_crossentropy(K.sum(mask*y_true, axis=-1), K.sum(mask*y_pred, axis=-1))
    return value_loss+policy_loss
model = load_model("Connect6.h5", compile=False)
model.compile(optimizer="nadam", loss=loss)
c = 5
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
        if(depth==361):
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
    def getnnstuff(self, board, player):
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
        playerinp = np.ones((19, 19, 1))*player*-1
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
        inp2 = np.concatenate((playerinp, p1inp, p2inp), axis=-1).reshape((1, 19, 19, 3))
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
    i_state.children.sort(key=lambda x: x.move)
    return [i.visits for i in i_state.children], depth, i_state.visits, i_state.children
board = [[0 for i in range(19)] for j in range(19)]
turn = -1
t = time.time()
shit = get_visits(board, turn, 512, connect6())
print(time.time()-t)
