import pygame
import piece

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


