import sys

import pygame
from pygame.locals import *

import chessState

clock = pygame.time.Clock()

pygame.init()

WIDTH = 712

HEIGHT = 712

DIM = 8

SQUARE_SIZE = WIDTH // DIM

WINDOW_SIZE = (WIDTH, HEIGHT)

board = pygame.display.set_mode(WINDOW_SIZE)

INITIAL_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
engine = chessState.chessEngine()
engine.load_images()
engine.create_board(INITIAL_FEN)
engine.scale_images(SQUARE_SIZE)
font = pygame.font.SysFont("Arial", 11)

pygame.display.set_caption("Chess")

GAME_COLORS = ((150, 200, 100), (200, 205, 200))

GAME_COLORS_MAP = (GAME_COLORS[1], GAME_COLORS[0])

HIGHLIGHT_COLORS = [(140, 255, 90), (255, 255, 255)]

GAME_FPS = 15


def draw_chess_board(board):
    letter_position = "abcdefgh"
    number_position = [str(i) for i in range(1, 9)]

    for i in range(DIM):
        for j in range(DIM):
            pygame.draw.rect(
                board,
                GAME_COLORS[(i + j) % 2],
                pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )
    for i in range(8):
        number_color = GAME_COLORS_MAP[i % 2]
        letter_color = GAME_COLORS[i % 2]

        number = font.render(number_position[i], True, number_color)
        board.blit(number, (3, i * SQUARE_SIZE + 3))

        letter = font.render(letter_position[i], True, letter_color)
        board.blit(letter, ((i + 1) * SQUARE_SIZE - 12, 8 * SQUARE_SIZE - 15))


def render_pieces(board):
    surface = engine.get_board()
    for i in range(len(surface)):
        for j in range(len(surface)):
            if surface[i][j] != "e":
                board.blit(
                    engine.get_piece(surface[i][j]), (j * SQUARE_SIZE, i * SQUARE_SIZE)
                )


def piece_click(board, coordinates):
    index = (coordinates[1] // SQUARE_SIZE, coordinates[0] // SQUARE_SIZE)
    piece = engine.get_piece_from_position(index)
    return index, piece


def highlight_piece(board, index):
    pygame.draw.rect(
        board,
        HIGHLIGHT_COLORS[(index[0] + index[1]) % 2],
        pygame.Rect(
            index[1] * SQUARE_SIZE, index[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
        ),
    )


def is_oppisite_color(letter, landonletter):
    if letter.islower():
        return letter.islower() == landonletter.isupper()
    elif letter.isupper():
        return letter.isupper() == landonletter.islower()


def right_player(index):
    if not engine.is_piece(index):
        return False
    white_turn = engine.is_white_turn()
    if white_turn and not engine.get_piece_from_position(index).isupper():
        return False
    if not white_turn and not engine.get_piece_from_position(index).islower():
        return False
    return True


def main():

    index = None
    clicked = False
    previous_index = None
    allowed_index = []

    while True:
        draw_chess_board(board)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                index, piece = piece_click(board, pos)

                if (
                    previous_index != index
                ):  # Makes sure player didn't click on same square again
                    if not clicked:
                        if not right_player(index):
                            continue

                    allowed_index_highlight = engine.get_valid_moves(index)
                    allowed_index_highlight = engine.emulate_move_capture(
                        index, allowed_index_highlight
                    )
                    if previous_index is not None and engine.is_piece(previous_index):
                        allowed_index = engine.get_valid_moves(previous_index)
                        allowed_index = engine.emulate_move_capture(
                            previous_index, allowed_index
                        )
                        previous_piece = engine.get_piece_from_position(previous_index)
                        current_piece = engine.get_piece_from_position(index)
                        if is_oppisite_color(
                            previous_piece, current_piece
                        ) or not engine.is_piece(index):
                            if index not in allowed_index:
                                clicked = False
                                previous_index, index = None, None
                                continue
                            engine.capture_piece(previous_index, index)
                            clicked = False
                            previous_index, index = None, None
                            engine.change_turn()
                            check_mate = engine.checkmate()
                            if check_mate != "Play":
                                print(check_mate)

                    else:
                        clicked = True

                    previous_index = index

                else:  # if they did click on same square deselect it and continue
                    previous_index = None
                    clicked = False

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if clicked:
            highlight_piece(board, index)
            for ind in allowed_index_highlight:
                highlight_piece(board, ind)
        render_pieces(board)

        pygame.display.update()
        clock.tick(GAME_FPS)


if __name__ == "__main__":
    main()
