import math
from copy import deepcopy
class state():
    def __init__(self, board, turn, getplayer, getboard, c, moveset, parent=None, move=None):
        self.board = board
        self.visits = 0
        self.wins = 0
        self.turn = turn
        self.player = getplayer(turn)
        self.getplayer = getplayer
        self.getboard = getboard
        self.moveset = moveset
        self.parent = parent
        self.c = c
        self.children = []
        self.move = move
    def new_child(self, move):
        board = deepcopy(self.board)
        board = self.getboard(move, board, self.player)
        child = state(board, self.turn+1, self.getplayer, self.getboard, self.c, self.moveset, self, move)
        return child
    def add_child(self, child):
        self.children.append(child)
        return self
    def is_leaf(self):
        unexplored = []
        for i in self.moveset:
            try:
                a = self.new_child(i)
                if(a.board not in [k.board for k in self.children]):
                    unexplored.append(a)
            except:
                continue
        return (len(unexplored)>0) or (len(unexplored)==0 and len(self.children)==0), unexplored
    def backprop(self, winner):
        self.visits+=1
        self.wins+=(winner==self.parent.player)
        if(self.parent is not None):
            return self.parent.backprop(winner)
        return self
    def get_score(self):
        if(self.parent is not None):
            return self.wins/self.visits+self.c*math.sqrt(math.log(self.parent.visits)/self.visits)
        return 0
    def choose_child(self):
        scores = []
        for i in self.children:
            scores.append(i.get_score())
        ind = scores.index(max(scores))
        return self.children[ind]
