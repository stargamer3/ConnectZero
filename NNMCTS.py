import math
from copy import deepcopy
import numpy as np
class state():
    def __init__(self, board, turn, c, game, parent=None, move=None, P=None):
        self.board = board
        self.visits = 0
        self.turn = turn
        self.player = game.getplayer(turn)
        self.getplayer = game.getplayer
        self.getboard = game.getboard
        self.moveset = game.moveset
        self.movelegal = game.movelegal
        self.players = game.players
        self.game = game
        self.parent = parent
        self.c = c
        self.P = P
        self.Q = 0
        self.W = {}
        self.V = {}
        for i in self.players:
            self.W[i] = 0
            self.V[i] = 0
        self.children = []
        self.move = move
    def new_child(self, move, P):
        child = state(None, self.turn+1, self.c, self.game, self, move, P)
        return child
    def add_child(self, child):
        self.children.append(child)
        return self
    def is_leaf(self):
        if(len(self.children)!=0):
            return False
        return True
    def backprop(self, V=None):
        self.visits+=1
        if(V is None):
            V = {}
            for i in self.players:
                V[i] = self.V[i]
        for i in self.players:
            self.W[i]+=V[i]
        if(self.parent is not None):
            self.Q = self.W[self.parent.player]/self.visits
            return self.parent.backprop(self.V)
        return self
    def get_score(self):
        if(self.parent is not None):
            return self.Q+self.c*self.P*math.sqrt(self.parent.visits)/(self.visits+1)
        return 0
    def get_board(self):
        if(self.board is None):
            self.board = deepcopy(self.parent.board)
            self.board = self.getboard(self.move, self.board, self.parent.player)
    def choose_child(self):
        scores = []
        for i in self.children:
            scores.append(i.get_score())
        ind = scores.index(max(scores))
        return self.children[ind]
