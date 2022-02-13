def is_oppisite_color(letter, landonletter):
    if letter.islower():
        return letter.islower() == landonletter.isupper()
    elif letter.isupper():
        return letter.isupper() == landonletter.islower()


def move(n):
    if n > 0:
        return n + 1
    elif n < 0:
        return n - 1
    else:
        return n


class pieceEngine:
    def __init__(self):
        pass

    def get_valid_horizontal_moves(self, board, index):
        valid_indexes = []
        piece = board[index[0]][index[1]]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        i, j = index
        for direction in directions:
            x, y = direction
            new_i, new_j = i, j
            terminate = False
            new_i, new_j = new_i + x, new_j + y
            while not terminate:
                if (
                    new_i >= 0
                    and new_i < len(board)
                    and new_j >= 0
                    and new_j < len(board[0])
                ):  # board[0] is just the column size of board assuming it has equal number of columns in all rows
                    current_piece = board[new_i][new_j]

                    if current_piece == "e":
                        valid_indexes.append((new_i, new_j))
                    else:
                        if is_oppisite_color(piece, current_piece):
                            valid_indexes.append((new_i, new_j))
                            terminate = True
                        else:
                            terminate = True

                else:
                    terminate = True
                x, y = move(x), move(y)
                new_i, new_j = i + x, j + y
        return valid_indexes

    def get_valid_diagonal_moves(self, board, index):
        valid_indexes = []
        piece = board[index[0]][index[1]]
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        i, j = index
        for direction in directions:
            x, y = direction
            new_i, new_j = i, j
            terminate = False
            new_i, new_j = new_i + x, new_j + y
            while not terminate:
                if (
                    new_i >= 0
                    and new_i < len(board)
                    and new_j >= 0
                    and new_j < len(board[0])
                ):  # board[0] is just the column size of board assuming it has equal number of columns in all rows
                    current_piece = board[new_i][new_j]

                    if current_piece == "e":
                        valid_indexes.append((new_i, new_j))
                    else:
                        if is_oppisite_color(piece, current_piece):
                            valid_indexes.append((new_i, new_j))
                            terminate = True
                        else:
                            terminate = True

                else:
                    terminate = True
                x, y = move(x), move(y)
                new_i, new_j = i + x, j + y
        return valid_indexes

    def get_pawn_moves(self, board, index):
        piece = board[index[0]][index[1]]
        if piece.isupper():
            if index[0] != 6:
                possible_horizontal_moves = [(-1, 0)]
            else:
                possible_horizontal_moves = [(-1, 0), (-2, 0)]

            possible_diagonal_moves = [(-1, 1), (-1, -1)]
        else:
            if index[0] != 1:
                possible_horizontal_moves = [(1, 0)]
            else:
                possible_horizontal_moves = [(1, 0), (2, 0)]

            possible_diagonal_moves = [(1, -1), (1, 1)]
        valid_indexes = []
        i, j = index
        for move in possible_horizontal_moves:
            x, y = move
            new_i, new_j = i + x, j + y
            if (
                new_i >= 0
                and new_i < len(board)
                and new_j >= 0
                and new_j < len(board[0])
            ):
                current_piece = board[new_i][new_j]
                if current_piece == "e":
                    valid_indexes.append((new_i, new_j))
                else:
                    break

        for move in possible_diagonal_moves:
            x, y = move
            new_i, new_j = i + x, j + y
            if (
                new_i >= 0
                and new_i < len(board)
                and new_j >= 0
                and new_j < len(board[0])
            ):
                current_piece = board[new_i][new_j]
                if is_oppisite_color(piece, current_piece) and current_piece != "e":
                    valid_indexes.append((new_i, new_j))
        return valid_indexes

    def get_bishop_moves(self, board, index):
        return self.get_valid_diagonal_moves(board, index)

    def get_knight_moves(self, board, index):
        possible_knight_move_index = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
        ]
        valid_indexes = []
        piece = board[index[0]][index[1]]
        i, j = index
        for move in possible_knight_move_index:
            x, y = move
            new_i, new_j = i + x, j + y
            if (
                new_i >= 0
                and new_i < len(board)
                and new_j >= 0
                and new_j < len(board[0])
            ):
                current_piece = board[new_i][new_j]
                if is_oppisite_color(piece, current_piece) or current_piece == "e":
                    valid_indexes.append((new_i, new_j))
        return valid_indexes

    def get_rook_moves(self, board, index):
        return self.get_valid_horizontal_moves(board, index)

    def get_queen_moves(self, board, index):
        return self.get_valid_horizontal_moves(
            board, index
        ) + self.get_valid_diagonal_moves(board, index)

    def get_king_moves(self, board, index):
        possible_king_move_index = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ]
        valid_indexes = []
        piece = board[index[0]][index[1]]
        i, j = index
        for move in possible_king_move_index:
            x, y = move
            new_i, new_j = i + x, j + y
            if (
                new_i >= 0
                and new_i < len(board)
                and new_j >= 0
                and new_j < len(board[0])
            ):
                current_piece = board[new_i][new_j]
                if is_oppisite_color(piece, current_piece) or current_piece == "e":
                    valid_indexes.append((new_i, new_j))
        return valid_indexes
