import math
from copy import deepcopy
class state():
    def __init__(self, board, turn, c, game, parent=None, move=None):
        self.board = board
        self.visits = 0
        self.wins = 0
        self.turn = turn
        self.player = game.getplayer(turn)
        self.getplayer = game.getplayer
        self.getboard = game.getboard
        self.moveset = game.moveset
        self.movelegal = game.movelegal
        self.game = game
        self.parent = parent
        self.c = c
        self.children = []
        self.move = move
    def new_child(self, move):
        board = deepcopy(self.board)
        board = self.getboard(move, board, self.player)
        child = state(board, self.turn+1, self.c, self.game, self, move)
        return child
    def add_child(self, child):
        self.children.append(child)
        return self
    def is_leaf(self):
        unexplored = []
        exploredmoves = [i.move for i in self.children]
        for i in self.moveset:
            if(self.movelegal(self.board, i) and i not in exploredmoves):
                unexplored.append(i)
        return (len(unexplored)>0) or (len(unexplored)==0 and len(self.children)==0), unexplored
    def backprop(self, winner):
        self.visits+=1
        if(self.parent is not None):
            self.wins+=(winner==self.parent.player)
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
