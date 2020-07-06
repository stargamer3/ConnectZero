from NNMCTS import state
import random
import time
import numpy as np
import math
c = 20
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
        policy = []
        for i in self.moveset:
            if(self.movelegal(board, i)):
                policy.append(random.random())
            else:
                policy.append(0)
        policy = np.array(policy)/sum(policy)
        return policy, random.random()
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
            for i in game.players:
                if(i!=sim_state.player):
                    sim_state.V[i] = game.getnnstuff(sim_state.board, i)[1]
            sim_state.V[sim_state.player] = nnstuff[1]
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
shit = get_visits(board, turn, 1600, connect6())
print(time.time()-t)
