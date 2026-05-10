from collections import deque
from constants import WALL, START, END
from maze import find_position


def bfs_solve(maze):
    start = find_position(maze, START)
    end = find_position(maze, END)

    if start is None or end is None:
        return []

    queue = deque([start])
    visited = {start}
    parent = {}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()

        if current == end:
            return reconstruct_path(parent, start, end)

        row, col = current

        for d_row, d_col in directions:
            next_pos = (row + d_row, col + d_col)

            if is_valid_move(maze, next_pos, visited):
                visited.add(next_pos)
                parent[next_pos] = current
                queue.append(next_pos)

    return []


def is_valid_move(maze, position, visited):
    row, col = position

    if row < 0 or row >= len(maze):
        return False

    if col < 0 or col >= len(maze[0]):
        return False

    if maze[row][col] == WALL:
        return False

    if position in visited:
        return False

    return True


def reconstruct_path(parent, start, end):
    path = []
    current = end

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path