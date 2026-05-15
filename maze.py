import random
from constants import WALL, PATH, START, END


def generate_maze(rows, cols, extra_connections=0, seed=None):
    rng = random.Random(seed)

    if rows % 2 == 0:
        rows += 1
    if cols % 2 == 0:
        cols += 1

    maze = [[WALL for _ in range(cols)] for _ in range(rows)]

    start_row, start_col = 1, 1
    maze[start_row][start_col] = PATH

    carve_paths(maze, start_row, start_col, rng)

    add_extra_connections(maze, extra_connections, rng)

    maze[1][1] = START
    maze[rows - 2][cols - 2] = END

    return maze


def add_extra_connections(maze, amount, rng):
    candidate_walls = []

    rows = len(maze)
    cols = len(maze[0])

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if maze[row][col] == WALL and can_break_wall(maze, row, col):
                candidate_walls.append((row, col))

    rng.shuffle(candidate_walls)

    for row, col in candidate_walls[:amount]:
        maze[row][col] = PATH


def can_break_wall(maze, row, col):
    if row % 2 == col % 2:
        return False

    horizontal_connection = (
        row % 2 == 1 and
        col % 2 == 0 and
        maze[row][col - 1] != WALL and
        maze[row][col + 1] != WALL
    )

    vertical_connection = (
        row % 2 == 0 and
        col % 2 == 1 and
        maze[row - 1][col] != WALL and
        maze[row + 1][col] != WALL
    )

    return horizontal_connection or vertical_connection


def carve_paths(maze, row, col, rng):
    directions = [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2)
    ]

    rng.shuffle(directions)

    for d_row, d_col in directions:
        new_row = row + d_row
        new_col = col + d_col

        if is_inside_maze(maze, new_row, new_col):
            if maze[new_row][new_col] == WALL:
                wall_row = row + d_row // 2
                wall_col = col + d_col // 2

                maze[wall_row][wall_col] = PATH
                maze[new_row][new_col] = PATH

                carve_paths(maze, new_row, new_col, rng)


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