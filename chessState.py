import pygame

import piece


def is_oppisite_color(letter, landonletter):
    if letter.islower():
        return letter.islower() == landonletter.isupper()
    elif letter.isupper():
        return letter.isupper() == landonletter.islower()


class chessEngine:
    def __init__(self):
        self.board = [["e" for j in range(8)] for i in range(8)]
        self.pieces = dict()
        self.turn_white = True
        self.piece_engine = piece.pieceEngine()
        self.white_castle = [True, True, True]
        self.black_castle = [True, True, True]

    def load_images(self):
        self.pieces["R"] = pygame.image.load("pieces/Chess_rlt60.png").convert_alpha()
        self.pieces["r"] = pygame.image.load("pieces/Chess_rdt60.png").convert_alpha()
        self.pieces["B"] = pygame.image.load("pieces/Chess_blt60.png").convert_alpha()
        self.pieces["b"] = pygame.image.load("pieces/Chess_bdt60.png").convert_alpha()
        self.pieces["N"] = pygame.image.load("pieces/Chess_nlt60.png").convert_alpha()
        self.pieces["n"] = pygame.image.load("pieces/Chess_ndt60.png").convert_alpha()
        self.pieces["P"] = pygame.image.load("pieces/Chess_plt60.png").convert_alpha()
        self.pieces["p"] = pygame.image.load("pieces/Chess_pdt60.png").convert_alpha()
        self.pieces["K"] = pygame.image.load("pieces/Chess_klt60.png").convert_alpha()
        self.pieces["k"] = pygame.image.load("pieces/Chess_kdt60.png").convert_alpha()
        self.pieces["Q"] = pygame.image.load("pieces/Chess_qlt60.png").convert_alpha()
        self.pieces["q"] = pygame.image.load("pieces/Chess_qdt60.png").convert_alpha()

    def scale_images(self, square_size):
        for p in self.pieces:
            self.pieces[p] = pygame.transform.smoothscale(
                self.pieces[p], (square_size, square_size)
            )

    def is_piece(self, index):
        return not self.board[index[0]][index[1]] == "e"

    def get_piece(self, piece):
        return self.pieces[piece]

    def create_board(self, fen):
        fen = fen.split("/")
        for i in range(len(self.board)):
            a = 0
            for char in fen[i]:
                if not char.isdigit():
                    self.board[i][a] = char
                    a += 1
                else:
                    a += int(char)

    def get_board(self):
        return self.board

    def get_piece_from_position(self, position):
        return self.board[position[0]][position[1]]

    def capture_piece(self, index, new_index):
        pi = self.get_piece_from_position(index)
        if (
            pi == "K" and abs(index[1] - new_index[1]) > 1
        ):  # Checking for white King castle
            if index == (7, 4):
                if new_index == (7, 2):
                    self.board[7][0] = "e"
                    self.board[7][2] = "K"
                    self.board[7][3] = "R"
                    self.board[7][4] = "e"
                elif new_index == (7, 6):
                    self.board[7][4] = "e"
                    self.board[7][5] = "R"
                    self.board[7][6] = "K"
                    self.board[7][7] = "e"
            return
        elif (
            pi == "k" and abs(index[1] - new_index[1]) > 1
        ):  # Checking for black King castle
            if index == (0, 4):
                if new_index == (0, 2):
                    self.board[0][0] = "e"
                    self.board[0][2] = "k"
                    self.board[0][3] = "r"
                    self.board[0][4] = "e"
                elif new_index == (0, 6):
                    self.board[0][4] = "e"
                    self.board[0][5] = "r"
                    self.board[0][6] = "k"
                    self.board[0][7] = "e"
            return

        self.board[new_index[0]][new_index[1]] = self.board[index[0]][index[1]]
        self.board[index[0]][index[1]] = "e"
        piece = self.get_piece_from_position(new_index)

        if piece == "R":
            if self.board[7][0] != "R":
                self.white_castle[0] = False
            elif self.board[7][7] != "R":
                self.white_castle[2] = False
        elif piece == "r":
            if self.board[0][0] != "r":
                self.black_castle[0] = False
            elif self.board[0][7] != "r":
                self.black_castle[2] = False
        elif piece == "K":
            self.white_castle[1] = False
        elif piece == "k":
            self.black_castle[1] = False

    def change_turn(self):
        self.turn_white = not self.turn_white

    def is_white_turn(self):
        return self.turn_white

    def get_piece_index(self, piece):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == piece:
                    return (i, j)

        return (0, 0)

    def get_valid_moves(self, index):
        p = self.get_piece_from_position(index)
        piece = p.lower()
        if piece == "r":
            return self.piece_engine.get_rook_moves(self.board, index)
        if piece == "n":
            return self.piece_engine.get_knight_moves(self.board, index)
        if piece == "p":
            return self.piece_engine.get_pawn_moves(self.board, index)
        if piece == "b":
            return self.piece_engine.get_bishop_moves(self.board, index)
        if piece == "q":
            return self.piece_engine.get_queen_moves(self.board, index)
        if piece == "k":
            return self.piece_engine.get_king_moves(self.board, index) + self.castle(
                index
            )
        return []

    def king_in_danger(self, index):
        all_opponent_indexes = []
        piece = self.get_piece_from_position(index)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                current_piece = self.get_piece_from_position((i, j))
                if is_oppisite_color(piece, current_piece):
                    all_opponent_indexes += self.get_valid_moves((i, j))
        if piece.isupper():
            king = "K"
        else:
            king = "k"
        for index in all_opponent_indexes:
            if self.get_piece_from_position(index) == king:
                return True
        return False

    def castle(self, index):
        ind = []
        piece = self.get_piece_from_position(index)
        if piece.isupper():
            if self.white_castle[:2] == [True, True]:
                rook_left_moves = self.piece_engine.get_rook_moves(self.board, (7, 0))
                if (
                    (7, 1) in rook_left_moves
                    and (7, 2) in rook_left_moves
                    and (7, 3) in rook_left_moves
                ):
                    if not self.king_in_danger(index):
                        ind.append((7, 2))
            if self.white_castle[1:] == [True, True]:
                rook_left_moves = self.piece_engine.get_rook_moves(self.board, (7, 7))
                if (7, 6) in rook_left_moves and (7, 5) in rook_left_moves:
                    if not self.king_in_danger(index):
                        ind.append((7, 6))
        else:
            if self.black_castle[:2] == [True, True]:
                rook_left_moves = self.piece_engine.get_rook_moves(self.board, (0, 0))
                if (
                    (0, 1) in rook_left_moves
                    and (0, 2) in rook_left_moves
                    and (0, 3) in rook_left_moves
                ):
                    if not self.king_in_danger(index):
                        ind.append((0, 2))
            if self.black_castle[1:] == [True, True]:
                rook_left_moves = self.piece_engine.get_rook_moves(self.board, (0, 7))
                if (0, 6) in rook_left_moves and (0, 5) in rook_left_moves:
                    if not self.king_in_danger(index):
                        ind.append((0, 6))
        return ind

    def pawn_reach_end(self, index):
        piece = self.get_piece_from_position(index)

        if piece == "P" and index[0] == 0:
            return True
        if piece == "p" and index[0] == 7:
            return True

        return False

    def emulate_move_capture(self, index, allowed_indexes):
        i, j = index
        return_index = []
        for ind in allowed_indexes:
            prev_piece = self.board[i][j]
            piece = self.board[ind[0]][ind[1]]
            self.board[ind[0]][ind[1]] = prev_piece
            self.board[i][j] = "e"
            if not self.king_in_danger(ind):
                return_index.append(ind)
            self.board[i][j] = prev_piece
            self.board[ind[0]][ind[1]] = piece
        return return_index

    def checkmate(self):
        if self.turn_white:
            all_valid_index = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j].isupper() and self.is_piece((i, j)):
                        valid_index = self.get_valid_moves((i, j))
                        valid_index = self.emulate_move_capture((i, j), valid_index)
                        all_valid_index += valid_index
            if self.king_in_danger(self.get_piece_index("K")) and (not all_valid_index):
                return "Black Wins"
            elif not self.king_in_danger(self.get_piece_index("K")) and (
                not all_valid_index
            ):
                return "Stalemate"
        elif not self.turn_white:
            all_valid_index = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j].islower() and self.is_piece((i, j)):
                        valid_index = self.get_valid_moves((i, j))
                        valid_index = self.emulate_move_capture((i, j), valid_index)
                        all_valid_index += valid_index
            if self.king_in_danger(self.get_piece_index("k")) and (not all_valid_index):
                return "White Wins"
            elif not self.king_in_danger(self.get_piece_index("k")) and (
                not all_valid_index
            ):
                return "Stalemate"

        return "Play"
