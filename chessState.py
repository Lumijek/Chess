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

    def load_images(self):
        self.pieces["R"] = pygame.image.load("pieces/Chess_rlt60.png").convert_alpha()
        self.pieces["r"] = pygame.image.load("pieces/Chess_rdt60.png").convert_alpha()
        self.pieces["B"] = pygame.image.load("pieces/Chess_blt60.png").convert_alpha()
        self.pieces["b"] = pygame.image.load("pieces/Chess_bdt60.png").convert_alpha()
        self.pieces["R"] = pygame.image.load("pieces/Chess_rlt60.png").convert_alpha()
        self.pieces["r"] = pygame.image.load("pieces/Chess_rdt60.png").convert_alpha()
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
            row = fen[i]
            row_length = len(row)
            j = 0
            while j < row_length:
                if row[j].isdigit():
                    j += int(row[j]) - 1
                    continue
                else:
                    self.board[i][j] = row[j]
                    j += 1

    def get_board(self):
        return self.board

    def get_piece_from_position(self, position):
        return self.board[position[0]][position[1]]

    def capture_piece(self, index, new_index):
        self.board[new_index[0]][new_index[1]] = self.board[index[0]][index[1]]
        self.board[index[0]][index[1]] = "e"

    def change_turn(self):
        self.turn_white = not self.turn_white

    def is_white_turn(self):
        return self.turn_white

    def get_valid_moves(self, index):
        piece = self.get_piece_from_position(index)
        piece = piece.lower()
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
            return self.piece_engine.get_king_moves(self.board, index)
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
            if not all_valid_index:
                return "Black Wins"
        elif not self.turn_white:
            all_valid_index = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j].islower() and self.is_piece((i, j)):
                        valid_index = self.get_valid_moves((i, j))
                        valid_index = self.emulate_move_capture((i, j), valid_index)
                        all_valid_index += valid_index
            if not all_valid_index:
                return "White Wins"

        return "Play"
