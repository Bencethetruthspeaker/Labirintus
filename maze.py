import random
from constants import WALL, PATH, START, END


def generate_maze(rows, cols):
    if rows % 2 == 0:
        rows += 1
    if cols % 2 == 0:
        cols += 1

    maze = [[WALL for _ in range(cols)] for _ in range(rows)]

    start_row, start_col = 1, 1
    maze[start_row][start_col] = PATH

    carve_paths(maze, start_row, start_col)

    maze[1][1] = START
    maze[rows - 2][cols - 2] = END

    return maze


def carve_paths(maze, row, col):
    directions = [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2)
    ]

    random.shuffle(directions)

    for d_row, d_col in directions:
        new_row = row + d_row
        new_col = col + d_col

        if is_inside_maze(maze, new_row, new_col):
            if maze[new_row][new_col] == WALL:
                wall_row = row + d_row // 2
                wall_col = col + d_col // 2

                maze[wall_row][wall_col] = PATH
                maze[new_row][new_col] = PATH

                carve_paths(maze, new_row, new_col)


def is_inside_maze(maze, row, col):
    return (
        1 <= row < len(maze) - 1
        and 1 <= col < len(maze[0]) - 1
    )


def print_maze(maze):
    for row in maze:
        print("".join(row))


def find_position(maze, symbol):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == symbol:
                return row, col

    return None