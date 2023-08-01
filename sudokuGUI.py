import pygame
import sys
import time
import copy
import numpy as np
from sudoku import Sudoku


pygame.init()
BORDER = 15
WINDOW_WIDTH, WINDOW_HEIGHT = 450 + 2 * BORDER, 550
WIDTH, HEIGHT = 450, 450
GRID = 50
SMALL_LINE = 1
BIG_LINE = 4
BOARD_LEN = 9
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
FONT_NUMBERS = pygame.font.SysFont("Times New Roman", 35)
FONT_LETTERS = pygame.font.SysFont("Times New Roman", 24)
INSANE = 0.001
FAST = 0.01
MEDIUM = 0.05
SLOW = 0.1
SNAKE = 0.5
DONE = False
SPEED = MEDIUM
DIFFICULTY = np.random.rand()
SUDOKU = np.array(Sudoku(3).difficulty(DIFFICULTY).board)
SUDOKU[SUDOKU == None] = 0
SUDOKU_COPY = copy.deepcopy(SUDOKU)

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku with Backtracking")

FPS = 60


def main():
    global SPEED
    clock = pygame.time.Clock()
    clock.tick(FPS)
    draw_window()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    run = False
                elif event.key == pygame.K_UP:
                    if SPEED == SNAKE:
                        SPEED = SLOW
                    elif SPEED == SLOW:
                        SPEED = MEDIUM
                    elif SPEED == MEDIUM:
                        SPEED = FAST
                    elif SPEED == FAST:
                        SPEED = INSANE

                elif event.key == pygame.K_DOWN:
                    if SPEED == MEDIUM:
                        SPEED = SLOW
                    elif SPEED == FAST:
                        SPEED = MEDIUM
                    elif SPEED == INSANE:
                        SPEED = FAST
                    elif SPEED == SLOW:
                        SPEED = SNAKE

                elif event.key == pygame.K_RIGHT:
                    SPEED = INSANE

                elif event.key == pygame.K_LEFT:
                    SPEED = SNAKE
                draw_window()

    t = solve_sudoku()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    global RESPONSE
                    global SUDOKU
                    global DONE
                    global SUDOKU_COPY
                    SUDOKU = get_sudoku()
                    SUDOKU_COPY = copy.deepcopy(SUDOKU)
                    DONE = False
                    SPEED = MEDIUM
                    main()
        draw_window(t)


def solve_sudoku():
    global SPEED
    global SUDOKU
    solve(0, 0)
    SUDOKU = copy.deepcopy(SUDOKU_COPY)
    SPEED = False
    start = time.time()
    solve_immediate(0, 0)
    end = time.time()

    return end - start


def draw_window(time=None):
    WINDOW.fill(GREY)

    # horizontal
    for i in range(0, 10):
        if i == 0 or i == 9:
            pygame.draw.line(
                WINDOW,
                BLACK,
                (0 + BORDER, i * GRID + BORDER),
                (WIDTH + BORDER, i * GRID + BORDER),
                BIG_LINE,
            )
        elif i in [1, 2, 4, 5, 7, 8]:
            pygame.draw.line(
                WINDOW,
                BLACK,
                (0 + BORDER, GRID * i + BORDER),
                (WIDTH + BORDER, GRID * i + BORDER),
                SMALL_LINE,
            )
        else:
            pygame.draw.line(
                WINDOW,
                BLACK,
                (0 + BORDER, GRID * i + BORDER),
                (WIDTH + BORDER, GRID * i + BORDER),
                BIG_LINE,
            )

    # vertical
    for i in range(0, 10):
        if i == 0 or i == 9:
            pygame.draw.line(
                WINDOW,
                BLACK,
                (i * GRID + BORDER, 0 + BORDER),
                (i * GRID + BORDER, WIDTH + BORDER),
                BIG_LINE,
            )
        elif i in [1, 2, 4, 5, 7, 8]:
            pygame.draw.line(
                WINDOW,
                BLACK,
                (GRID * i + BORDER, 0 + BORDER),
                (GRID * i + BORDER, WIDTH + BORDER),
                SMALL_LINE,
            )
        else:
            pygame.draw.line(
                WINDOW,
                BLACK,
                (GRID * i + BORDER, 0 + BORDER),
                (GRID * i + BORDER, WIDTH + BORDER),
                BIG_LINE,
            )

    # values
    for i, row in enumerate(SUDOKU):
        for j, val in enumerate(row):
            if 0 < val < 10:
                value = FONT_NUMBERS.render(str(val), True, BLACK)
                WINDOW.blit(value, (j * GRID + 16 + BORDER, i * GRID + 4 + BORDER))

    if False != SPEED != DONE:
        speeds = {
            0.001: "INSANE",
            0.01: "FAST",
            0.05: "MEDIUM",
            0.1: "SLOW",
            0.5: "SNAKE",
        }
        value = FONT_LETTERS.render(f"Speed: {speeds[SPEED].title()}", True, BLACK)
        WINDOW.blit(value, (170, 490))
    elif SPEED == False:
        value = FONT_LETTERS.render(f"Done", True, BLACK)
        WINDOW.blit(value, (215, 475))
        value = FONT_LETTERS.render(
            f"Computation time: {round(time, 5)} seconds", True, BLACK
        )
        WINDOW.blit(value, (70, 510))

    pygame.display.update()


def solve(row, column):
    global SPEED
    global DONE

    if SPEED == DONE:
        return False

    draw_window()
    time.sleep(SPEED)

    # base case: if row == 9, SUDOKU[8][8] must have a value
    if row == 9:
        return True

    # for every possible entry: check if valid entry is possible
    for val in range(1, 10):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if SPEED == SNAKE:
                        SPEED = SLOW
                    elif SPEED == SLOW:
                        SPEED = MEDIUM
                    elif SPEED == MEDIUM:
                        SPEED = FAST
                    elif SPEED == FAST:
                        SPEED = INSANE

                elif event.key == pygame.K_DOWN:
                    if SPEED == MEDIUM:
                        SPEED = SLOW
                    elif SPEED == FAST:
                        SPEED = MEDIUM
                    elif SPEED == INSANE:
                        SPEED = FAST
                    elif SPEED == SLOW:
                        SPEED = SNAKE

                elif event.key == pygame.K_RIGHT:
                    SPEED = INSANE

                elif event.key == pygame.K_LEFT:
                    SPEED = SNAKE

                elif event.key == pygame.K_RETURN:
                    DONE = True
                    SPEED = DONE

        if SPEED != DONE:
            time.sleep(SPEED)
        # check if spot is free
        if SUDOKU[row][column] == 0:
            SUDOKU[row][column] = val
            draw_window()
            if SPEED != DONE:
                time.sleep(SPEED)
            if valid_position(row, column, val):
                # get next position
                next_row, next_column = get_next_pos(row, column)

                # next spot
                if solve(next_row, next_column):
                    if SPEED == DONE:
                        return False
                    draw_window()
                    time.sleep(SPEED)
                    return True
                else:
                    # if next spot has no more possible values reset current position and try another number
                    SUDOKU[row][column] = 0

            else:
                SUDOKU[row][column] = 0

        else:
            # skip starting numbers
            if not valid_position(row, column, SUDOKU[row][column]):
                sys.exit("Not solvable\nYour sudoku already had a mistake!\n")
            row, column = get_next_pos(row, column)
            if SPEED != DONE:
                time.sleep(SPEED)
            return solve(row, column)

    draw_window()
    if SPEED != DONE:
        time.sleep(SPEED)
    # return false if no entry is possible
    return False


def solve_immediate(row, column):
    global SUDOKU
    # base case: if row == 9, SUDOKU[8][8] must have a value
    if row == 9:
        return True

    # for every possible entry: check if valid entry is possible
    for val in range(1, 10):
        # check if spot is free
        if SUDOKU[row][column] == 0:
            SUDOKU[row][column] = val
            if valid_position(row, column, val):
                # get next position
                next_row, next_column = get_next_pos(row, column)

                # next spot
                if solve_immediate(next_row, next_column):
                    return True
                else:
                    # if next spot has no more possible values reset current position and try another number
                    SUDOKU[row][column] = 0
            else:
                SUDOKU[row][column] = 0

        else:
            # skip starting numbers
            if not valid_position(row, column, SUDOKU[row][column]):
                sys.exit("Not solvable\nYour sudoku already had a mistake!\n")
            row, column = get_next_pos(row, column)
            return solve_immediate(row, column)

    # return false if no entry is possible
    return False


def get_next_pos(row, column):
    if column < 8:
        column += 1
    else:
        row += 1
        column = 0
    return row, column


def valid_position(row, column, entry):
    for idx in range(9):
        # check column for duplicate
        if idx != column and SUDOKU[row][idx] == entry:
            return False

        # check row for duplicate
        elif idx != row and SUDOKU[idx][column] == entry:
            return False

    # check box for duplicate
    pos_column = int(column / 3) * 3
    pos_row = int(row / 3) * 3
    for i in range(3):
        for j in range(3):
            if (
                pos_row + i != row
                and pos_column + j != column
                and SUDOKU[pos_row + i][pos_column + j] == entry
            ):
                return False

    return True


def get_sudoku():
    diff = np.random.rand()
    s = np.array(Sudoku(3).difficulty(diff).board)
    s[s == None] = 0
    return s


if __name__ == "__main__":
    main()
