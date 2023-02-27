# Useful libraries:
from collections import defaultdict


def k_in_row(board, player, square, k):
    x = square[0]
    y = square[1]

    ## Define the target zone by indexes
    index = k - 1
    max_index = k + 1
    # Extract the rows
    # Vertical
    up_row = [player for j in range(k) if board[(x, y - j)] == player]
    # Bottom
    bottom_row = [player for j in range(k) if board[(x, y + j)] == player]
    # Left
    Left_row = [player for i in range(k) if board[(x - i, y)] == player]
    # Right
    Right_row = [player for i in range(k) if board[(i + x, y)] == player]
    # Right_upper_diagonal
    Right_upper_diag = [player for _ in range(k) if board[(x + _, y - _)] == player]
    # Right_bottom_diagonal
    Right_bottom_diag = [player for _ in range(k) if board[(x + _, y + _)] == player]
    # Left_bottom diag
    Left_bottom_diag = [player for _ in range(k) if board[(x - _, y + _)] == player]
    # Left upper diag
    Left_upper_diag = [player for _ in range(k) if board[(x - _, y - _)] == player]

    total_row = [
        len(up_row),
        len(Right_upper_diag),
        len(Right_row),
        len(Right_bottom_diag),
        len(bottom_row),
        len(Left_bottom_diag),
        len(Left_row),
        len(Left_upper_diag),
    ]
    return total_row


class Board(defaultdict):
    empty = "."
    used = "#"

    def __init__(self, width=7, height=6, current_player=None, **kwds):
        self.__dict__.update(
            width=width, height=height, current_player=current_player, **kwds
        )

    def __missing__(self, pos):

        if (pos[0] < self.width) and (pos[1] < (self.height)):

            return Board.empty
        else:
            return Board.used

    def __hash__(self):
        """
        Hash method stores the instances in hash tables.
        """
        return hash(tuple(sorted(self.items()))) + hash(self.current_player)

    def __repr__(self):
        def row(y):
            return " ".join(self[x, y] for x in range(self.width))

        return "\n".join(map(row, range(self.height))) + "\n"

    def update_board(self, changes: dict, **kwds) -> "Board":
        """
        Update the board with the new changes of each cell.
        """
        self.update(changes)
        return self


class TicTacToe:
    def __init__(self, height=3, width=3, k=3):
        self.k = k
        self.height = height
        self.width = width
        self.squares = {(x, y) for x in range(self.width) for y in range(self.height)}

        self.initial = Board(self.width, self.height, "X")
        self.board = self.initial

    def actions(self, board):
        moves = {}
        for square in self.squares:
            player = board[square]
            if player == ".":
                moves[square] = board.current_player
        return moves

    def utility(self, board):
        player = "X"
        rival = "O"
        player_utility = 0

        for pos in self.squares:
            # print('pos,',pos)
            player_rows = k_in_row(board, player, pos, self.k)
            if self.k in player_rows:
                player_utility = -1
            rival_rows = k_in_row(board, rival, pos, self.k)
            if self.k in rival_rows:
                player_utility = 1

        self.util = player_utility
        return player_utility

    def make_move(self, board, square):
        player = board.current_player
        board.update_board({square: player})
        board.utility = self.utility(board)
        if board.current_player == "X":
            board.current_player = "O"
        else:
            board.current_player = "X"
        return board

    def end(self, board):
        utility = self.utility(board)

        if (utility) != 0:
            return (True, utility)
        else:
            if self.actions(board) == {}:
                return (True, 0)
            else:
                return (False, 0)
