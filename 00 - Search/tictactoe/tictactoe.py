"""
Tic Tac Toe Player
"""

import math
import copy

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
    if board == initial_state():
        return 'X'

    X_count = sum([row.count('X') for row in board])
    O_count = sum([row.count('O') for row in board])

    return 'O' if O_count < X_count else 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action in actions(board):
        board_copy = copy.deepcopy(board)
        board_copy[action[0]][action[1]] = player(board)
        return board_copy

    raise Exception('Action not possible.')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    EMPTY = None

    diag_1 = [board[0][0], board[1][1], board[2][2]]
    diag_2 = [board[2][0], board[1][1], board[0][2]]

    if (len(set(diag_1)) == 1 and EMPTY not in diag_1) or (len(set(diag_2)) == 1 and EMPTY not in diag_2):
        return board[1][1]

    # Row / col check
    for i in range(3):
        row = board[i]
        col = [board[j][i] for j in range(3)]

        # Row check
        if (len(set(row)) == 1 and EMPTY not in row):
            return row[0]
        # Col check
        elif (len(set(col)) == 1 and EMPTY not in col):
            return col[0]
        else:
            continue

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == EMPTY:
                    return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result:
        return 1 if result == 'X' else -1

    return 0


def min_utility(board):
    # If terminal, board returns current board state utility
    if terminal(board):
        return utility(board)

    curr = float('inf')
    for action in actions(board):
        res = max_utility(result(board, action))
        # -1 result instantly provides the optimal outcome for player 0
        curr = min(curr, res)

    return curr


def max_utility(board):
    # If terminal, board returns current board state utility
    if terminal(board):
        return utility(board)

    curr = float('-inf')
    for action in actions(board):
        res = min_utility(result(board, action))
        # 1 result instantly provides the optimal outcome for player X
        curr = max(curr, res)

    return curr


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # X maximises score
    if player(board) == 'X':
        options = []
        for action in actions(board):
            if winner(result(board, action)) == 'X':
                return action
            options.append((min_utility(result(board, action)), action))
        # Sort options by utility value score, select first option
        return sorted(options, key=lambda x: x[0])[0][-1]

    else:
        options = []
        for action in actions(board):
            if winner(result(board, action)) == 'O':
                return action
            options.append((max_utility(result(board, action)), action))
        #
        return sorted(options, key=lambda x: x[0])[0][1]
