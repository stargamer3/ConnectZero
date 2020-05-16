from simpleMCTS import state
import random
c = .5
moveset  = [[i, j] for i in range(19) for j in range(19)]
def getplayer(turn):
    m4 = turn%4
    if(m4 in [0, 1]):
        return -1
    return 1
def getboard(move, board, player):
    assert board[move[0]][move[1]]==0
    board[move[0]][move[1]] = player
    return board
def game_finished(board):
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
def get_visits(board, turn, its):
    i_state = state(board, turn, getplayer, getboard, c, moveset)
    depth = 0
    for its in range(its):
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
board = [[0 for i in range(19)] for j in range(19)]
turn = -1
