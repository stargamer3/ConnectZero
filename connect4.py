import math
from copy import deepcopy
import random
import time
from multiprocessing import Pool
c = .5
temperature = 100
class state():
    def __init__(self, board, color, parent=None, move=None):
        self.board = board
        self.visits = 0
        self.wins = 0
        self.color = color
        self.parent = parent
        self.children = []
        self.move = move
    def new_child(self, move):
        board = deepcopy(self.board)
        assert board[move][-1]==0
        i = -1
        while(board[move][i]==0 and -1*i<len(board[move])):
            i-=1
        if(board[move][i]!=0):
            i+=1
        board[move][i] = self.color
        child = state(board, self.color*-1, self, move)
        return child
    def add_child(self, child):
        self.children.append(child)
        self.children.sort(key=lambda x: x.move)
        return self
    def is_leaf(self):
        unexplored = []
        for i in range(7):
            try:
                a = self.new_child(i)
                if(a.board not in [k.board for k in self.children]):
                    unexplored.append(a)
            except:
                continue
        return (len(unexplored)>0) or (len(unexplored)==0 and len(self.children)==0), unexplored
    def backprop(self, winner):
        self.visits+=1
        self.wins+=(winner==-1*self.color)
        if(self.parent is not None):
            return self.parent.backprop(winner)
        return self
    def get_score(self):
        global c
        if(self.parent is not None):
            return self.wins/self.visits+c*math.sqrt(math.log(self.parent.visits)/self.visits)
        return 0
    def choose_child(self):
        scores = []
        for i in self.children:
            scores.append(i.get_score())
        ind = scores.index(max(scores))
        return self.children[ind]
def game_finished(board):
    for i in range(len(board)):
        for j in range(len(board[i])-3):
            if([board[i][j], board[i][j], board[i][j], board[i][j]]==[board[i][j], board[i][j+1], board[i][j+2], board[i][j+3]] and board[i][j]!=0):
                return True, board[i][j]
    for i in range(len(board)-3):
        for j in range(len(board[i])):
            if([board[i][j], board[i][j], board[i][j], board[i][j]]==[board[i][j], board[i+1][j], board[i+2][j], board[i+3][j]] and board[i][j]!=0):
                return True, board[i][j]
    for i in range(3, len(board)):
        for j in range(len(board[i])-3):
            if([board[i][j], board[i][j], board[i][j], board[i][j]]==[board[i][j], board[i-1][j+1], board[i-2][j+2], board[i-3][j+3]] and board[i][j]!=0):
                return True, board[i][j]
    for i in range(3, len(board)):
        for j in range(3, len(board[i])):
            if([board[i][j], board[i][j], board[i][j], board[i][j]]==[board[i][j], board[i-1][j-1], board[i-2][j-2], board[i-3][j-3]] and board[i][j]!=0):
                return True, board[i][j]
    zeros = 0
    for i in board:
        zeros+=i.count(0)
    if(zeros==0):
        return True, 0
    return False, 0
board = [[0 for i in range(6)] for i in range(7)]
ccolor = random.choice([-1, 1])
color = 1
def get_visits(board, color):
    t = time.time()
    i_state = state(board, color)
    depth = 0
    for its in range(1000):
        k = 0
        sim_state = i_state
        leaf = sim_state.is_leaf()[0]
        while(not leaf):
            sim_state = sim_state.choose_child()
            leaf = sim_state.is_leaf()[0]
            k+=1
        finished = game_finished(sim_state.board)[0]
        while(not finished):
            unexplored = sim_state.is_leaf()[1]
            sim_state = random.choice(unexplored)
            sim_state.parent.add_child(sim_state)
            finished = game_finished(sim_state.board)[0]
            k+=1
        winner = game_finished(sim_state.board)[1]
        i_state = sim_state.backprop(winner)
        depth = max([depth, k])
    return [i.visits for i in i_state.children], depth, i_state.visits, i_state.children
def get_move(board, color):
    i_visits, depth, t_visits, children = get_visits(board, color)
    policy = [math.e**(i/temperature) for i in i_visits]
    policy = [i/sum(policy) for i in policy]
    move_ind = random.choices(list(range(len(i_visits))), weights=policy, k=1)[0]
    move = children[move_ind].move
    return move, depth
def make_move(pboard, move, color):
    board = deepcopy(pboard)
    assert board[move][-1]==0
    i = -1
    while(board[move][i]==0 and -1*i<len(board[move])):
        i-=1
    if(board[move][i]!=0):
        i+=1
    board[move][i] = color
    return board
finished = game_finished(board)[0]
fplayer = "Computer" if ccolor==color else "Human"
print("%s goes first"%fplayer)
while(not finished):
    if(ccolor==color):
        move, depth = get_move(board, color)
        print("Computer thought %s moves into the future and made move %s"%(str(depth), str(move)))
    else:
        move = int(input("What move do you make?\n"))
    board = make_move(board, move, color)
    finished = game_finished(board)[0]
    color*=-1
nwinner = game_finished(board)[1]
winner = "Computer" if nwinner==ccolor else "Human"
if(nwinner==0):
    winner = "Nobody"
print("%s won"%winner)
