import pygame
import sys
import numpy as np

# Ініціалізація
pygame.init()

# Розміри
ROWS = 6
COLS = 7
SQUARESIZE = 100

WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE

SIZE = (WIDTH, HEIGHT)

RADIUS = SQUARESIZE // 2 - 5

# Кольори
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect Four")

board = np.zeros((ROWS, COLS))


def draw_board():
    for c in range(COLS):
        for r in range(ROWS):

            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE,
                 r * SQUARESIZE + SQUARESIZE,
                 SQUARESIZE,
                 SQUARESIZE)
            )

            pygame.draw.circle(
                screen,
                BLACK,
                (
                    c * SQUARESIZE + SQUARESIZE // 2,
                    r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2
                ),
                RADIUS
            )

    for c in range(COLS):
        for r in range(ROWS):

            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            else:
                continue

            pygame.draw.circle(
                screen,
                color,
                (
                    c * SQUARESIZE + SQUARESIZE // 2,
                    HEIGHT - (r * SQUARESIZE + SQUARESIZE // 2)
                ),
                RADIUS
            )

    pygame.display.update()


def drop_piece(row, col, piece):
    board[row][col] = piece


def is_valid_location(col):
    return board[ROWS - 1][col] == 0


def get_next_open_row(col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r


def winning_move(piece):

    # Горизонтально
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Вертикально
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Діагональ /
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Діагональ \
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False


draw_board()

turn = 0
game_over = False

font = pygame.font.SysFont("Arial", 50)

while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:

            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

            posx = event.pos[0]

            color = RED if turn == 0 else YELLOW

            pygame.draw.circle(
                screen,
                color,
                (posx, SQUARESIZE // 2),
                RADIUS
            )

            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:

            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

            posx = event.pos[0]
            col = posx // SQUARESIZE

            if is_valid_location(col):

                row = get_next_open_row(col)

                piece = 1 if turn == 0 else 2

                drop_piece(row, col, piece)

                if winning_move(piece):

                    text = "Червоний переміг!" if piece == 1 else "Жовтий переміг!"

                    label = font.render(text, True, RED if piece == 1 else YELLOW)

                    screen.blit(label, (40, 10))

                    game_over = True

                draw_board()

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(5000)