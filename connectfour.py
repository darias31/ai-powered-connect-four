import copy
import random
import warnings
import os
from time import sleep

#       TO DO:
#
#       Support for multiple board sizes (aka remove the hardcoded numbers in loops)
#       Pretty interface (maybe pygame)


# lol
warnings.filterwarnings("ignore", category=DeprecationWarning)

O = "O"  # player O
X = "X"  # player X

EMPTY = None


def empty_board():
    """
    returns empty connect four board
    """
    board = [
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
    ]

    return board


def print_board(board):
    """
    prints the board
    """

    # print the column nums
    print("\n\n  1    2    3    4    5    6    7")

    for row in board:
        print(row)


def get_player(board):
    """
    Returns the next player when provided a game board.
    """

    count_x = 0
    count_o = 0

    for row in board:
        for val in row:
            if val == X:
                count_x += 1
            elif val == O:
                count_o += 1

    # since B goes first, it's only O's turn if there's more of B on the board
    if count_x > count_o:
        return O

    return X


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    """

    if winner(board) != None:
        return True
    else:
        for row in board:
            if " " in row:
                return False
        return True


def actions(board):
    """
    Returns set of all possible actions (int, representing the column index) available on the board.
    """

    actions = set()

    # iterate through every column and check which columns are still not filled
    for col in range(7):
        if board[0][col] == " ":
            actions.add(col)

    return actions


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # I'll keep thinking about a faster algorithm

    def does_square_contain_win(i, j):

        # masks for winner checking
        masks = [
            [[i, j], [i - 1, j + 1], [i - 2, j + 2], [i - 3, j + 3]],
            [[i, j], [i - 1, j - 1], [i - 2, j - 2], [i - 3, j - 3]],
            [[i, j], [i, j + 1], [i, j + 2], [i, j + 3]],
            [[i, j], [i - 1, j], [i - 2, j], [i - 3, j]],
        ]

        last_seen_val = None

        for mask in masks:
            counter = 0
            for elem in mask:
                if (
                    0 <= elem[0] < 6 and 0 <= elem[1] < 7
                ):  # check if indices are within bounds
                    curr_elem = board[elem[0]][elem[1]]
                    if curr_elem == last_seen_val:
                        counter += 1
                        if counter == 4:
                            return last_seen_val
                    else:
                        if curr_elem != " ":
                            last_seen_val = curr_elem
                            counter = 1
                else:
                    break

        return None

    for row in range(6):
        for col in range(7):
            winner = does_square_contain_win(row, col)
            if winner != None:
                return winner

    return None


def result(board, action_col):
    """
    Returns the board that results from making a move (int) on the board.
    """
    copy_board = copy.deepcopy(board)
    player = get_player(copy_board)

    row = -1

    # find the lowest empty row given a column
    while row < 5 and copy_board[row + 1][action_col] == " ":
        row += 1

    if row == -1:
        print("\nUnable to make move. Please try another column...")

    copy_board[row][action_col] = player

    return copy_board


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    win = winner(board)

    if win == "X":
        return 1
    elif win == "O":
        return -1
    else:
        return 0


def minimax(board, max_actions_to_explore):
    """
    Returns the most optimal move to make on a given board, none if given board is terminal.
    """

    def max_value(board, alpha=float("-inf"), beta=float("inf")):
        if terminal(board):
            return utility(board)

        v = float("-inf")

        actions_to_explore = random.sample(
            actions(board), min(max_actions_to_explore, len(actions(board)))
        )
        for action in actions_to_explore:
            v = max(v, min_value(result(board, action), alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break

        return v

    def min_value(board, alpha=float("-inf"), beta=float("inf")):
        if terminal(board):
            return utility(board)

        v = float("inf")

        actions_to_explore = random.sample(
            actions(board), min(max_actions_to_explore, len(actions(board)))
        )
        for action in actions_to_explore:
            v = min(v, max_value(result(board, action), alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break

        return v

    player = get_player(board)
    possible_actions = actions(board)

    if player == "X":  # maximizing player
        highest_util = float("-inf")
        best_action = None

        actions_to_explore = random.sample(
            actions(board), min(max_actions_to_explore, len(actions(board)))
        )
        for action in actions_to_explore:
            result_board = result(board, action)
            util = max_value(result_board)
            if util > highest_util:
                highest_util = util
                best_action = action
        return best_action
    elif player == "O":  # minimizing player
        lowest_util = float("inf")
        best_action = None

        actions_to_explore = random.sample(
            actions(board), min(max_actions_to_explore, len(actions(board)))
        )
        for action in actions_to_explore:
            result_board = result(board, action)
            util = min_value(result_board)
            if util < lowest_util:
                lowest_util = util
                best_action = action
        return best_action

    return None


def main():
    """
    Provides the main code for the game of Connect Four
    """

    game_end = False
    turns_taken = 0
    max_actions_to_explore = 2
    board = empty_board()

    os.system("cls")
    print("\nWelcome to Connect Four!")
    print("You are player X.\n")
    print_board(board)

    while not game_end:

        # scale the amount of actions the AI explores based on how many turns were taken.
        # i'm not gonna lie, this thing beats me more often than I'd like to admit...
        # even when it's using only a fraction of its power haha
        if turns_taken == 25:
            max_actions_to_explore = 3
        elif turns_taken == 31:
            max_actions_to_explore = 4
        elif turns_taken == 37:
            max_actions_to_explore = 5

        player = get_player(board)

        if player == "X":
            player_move = input("\nPlease provide the column for your move: ")
            while (int(player_move) - 1) not in actions(board):
                player_move = input(
                    "\nSorry, you can't make a move there.\nPlease provide the column for your move: "
                )
            board = result(board, int(player_move) - 1)
        elif player == "O":
            print("\nComputer is thinking...")

            if turns_taken <= 9:
                sleep(1.5)
                # make initial moves close to player's move... otherwise it takes forever
                # maybe instead of completely random moves initially, we check if there's any 3 in a row??
                # ...so that we can make a smarter choice if the player is close to winning
                if int(player_move) < 7:
                    player_move = random.randint(int(player_move) - 2, int(player_move))
                else:
                    player_move = random.randint(
                        int(player_move) - 2, int(player_move) - 1
                    )
            elif turns_taken > 1:
                sleep(0.5)
                player_move = minimax(board, max_actions_to_explore)
            board = result(board, int(player_move))

        os.system("cls")
        print_board(board)

        turns_taken += 1

        if terminal(board):
            game_end = True
            print(f"\n\nWinner: {winner(board)}\n")


if __name__ == "__main__":
    main()
