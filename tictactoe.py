"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0
    # Count the number of each player's tokens
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                count_x += 1
            elif board[i][j] == O:
                count_o += 1
    
    # If they are equal it means X plays
    if count_o == count_x:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                actions.append((i,j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Check invalid cases
    #
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2 or board[action[0]][action[1]] is not EMPTY:
        raise Exception("Not valid option")
    
    #A copy of the list is made to create a new state.
    new_board = [board[0].copy(),board[1].copy(),board[2].copy()]
    new_board[action[0]][action[1]] = player(new_board)
    return new_board

    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Every possible winning situation is checked
    if board[0][0] == board[0][1] and board[0][1] == board[0][2]:
        return board[0][0]
    if board[1][0] == board[1][1] and board[1][1] == board[1][2]:
        return board[1][0]
    if board[2][0] == board[2][1] and board[2][1] == board[2][2]:
        return board[2][0]
    if board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    if board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    if board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there exists a winner it is over
    win_player = winner(board)
    if win_player == X or win_player == O:
        return True

    # If a cell is Empty it is not over
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                return False
    
    # Tie remains
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    if result == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Player O
    # Searches for the values of the different actions and picks the minimum
    if player(board) == O:
        current_actions = actions(board)
        values = []
        for index in range(len(current_actions)):
            values.append(max_value(result(board, current_actions[index])))
        minimum = min(values)
        return current_actions[values.index(minimum)]

    # Player X
    # Searches for the values of the different actions and picks the maximum
    current_actions = actions(board)
    values = []
    for index in range(len(current_actions)):
        values.append(min_value(result(board, current_actions[index])))
    maximum = max(values)
    return current_actions[values.index(maximum)]


def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = -2
    current_actions = actions(board)
    for action in current_actions:
        min = min_value(result(board, action))
        v = max(v, min)
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = 2
    current_actions = actions(board)
    for action in current_actions:
        max = max_value(result(board, action))
        v = min(v, max)
    return v