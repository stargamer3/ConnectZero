import math
from copy import deepcopy
class state():
    def __init__(self, board, turn, getplayer, getboard, c, moveset, network, fast_policy, getnninp, getP, elitism, parent=None, move=None):
        self.board = board
        self.visits = 0
        self.network = network
        self.fast_policy = fast_policy
        self.getnninp = getnninp
        self.getP = getP
        self.elitism = elitism
        self.V = 0
        self.P = 0
        self.Q = 0
        if(self.parent is not None):
            self.V = (1+network.predict(getnninp(board, self.parent.turn))[0][-1])/2
            self.P = getP(network.predict(getnninp(self.parent.board, self.parent.turn))[0][:-1], self.move)
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
        ps = [i.P for i in self.children+unexplored]
        good_ps = []
        num = math.floor(self.elitism*len(ps))
        for i in range(num):
            m = max(ps)
            ps.pop(ps.index(m))
            good_ps.append(m)
        good_unexplored = []
        for i in range(len(unexplored)):
            if(unexplored[i].P in good_ps):
                good_unexplored.append(unexplored[i])
        return (len(good_unexplored)>0) or (len(good_unexplored)==0 and len(good_self.children)==0), good_unexplored
    def backprop(self):
        self.visits+=1
        #write some stuff to avg V with V of all children (and grandchildren to the end of the simulation) playing as the same player, gives Q
        if(self.parent is not None):
            return self.parent.backprop()
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
