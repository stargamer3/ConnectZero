import math
from copy import deepcopy
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
        board = deepcopy(self.board)
        board = self.getboard(move, board, self.player)
        child = state(board, self.turn+1, self.c, self.game, self, move, P)
        return child
    def add_child(self, child):
        self.children.append(child)
        return self
    def is_leaf(self):
        if(len(self.children)!=0):
            return False, []
        unexplored = []
        for i in self.moveset:
            if(self.movelegal(self.board, i)):
                unexplored.append(i)
        return True, unexplored
    def backprop(self, W=None):
        self.visits+=1
        if(W is None):
            W = {}
            for i in self.players:
                W[i] = 0
        if(self.parent is not None):
            for i in players:
                self.W[i]+=W[i]
            self.Q = (self.W[self.parent.player]+self.V[self.parent.player])/self.visits
            bpW = {}
            for i in players:
                bpW[i] = self.W[i]+self.V[i]
            return self.parent.backprop(bpW)
        return self
    def get_score(self):
        if(self.parent is not None):
            return self.Q+self.c*self.P*math.sqrt(self.parent.visits)/(self.visits+1)
        return 0
    def choose_child(self):
        scores = []
        for i in self.children:
            scores.append(i.get_score())
        ind = scores.index(max(scores))
        return self.children[ind]
