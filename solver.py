from collections import deque
import heapq
import time

from constants import WALL, START, END
from maze import find_position


def run_selected_solvers(maze, selected_solvers):
    results = {}

    solvers = {
        "BFS": bfs_solve,
        "DFS": dfs_solve,
        "Dijkstra": dijkstra_solve,
        "Bellman-Ford": bellman_ford_solve
    }

    for name, is_selected in selected_solvers.items():
        if is_selected and name in solvers:
            start_time = time.perf_counter()
            path = solvers[name](maze)
            end_time = time.perf_counter()

            results[name] = {
                "path": path,
                "time": end_time - start_time,
                "path_length": len(path) if path else 0
            }

    return results


def bfs_solve(maze):
    start, end = get_start_and_end(maze)
    if start is None or end is None:
        return []

    queue = deque([start])
    visited = {start}
    parent = {}

    while queue:
        current = queue.popleft()

        if current == end:
            return reconstruct_path(parent, start, end)

        for next_pos in get_neighbors(maze, current):
            if next_pos not in visited:
                visited.add(next_pos)
                parent[next_pos] = current
                queue.append(next_pos)

    return []


def dfs_solve(maze):
    start, end = get_start_and_end(maze)
    if start is None or end is None:
        return []

    stack = [start]
    visited = {start}
    parent = {}

    while stack:
        current = stack.pop()

        if current == end:
            return reconstruct_path(parent, start, end)

        for next_pos in get_neighbors(maze, current):
            if next_pos not in visited:
                visited.add(next_pos)
                parent[next_pos] = current
                stack.append(next_pos)

    return []


def dijkstra_solve(maze):
    start, end = get_start_and_end(maze)
    if start is None or end is None:
        return []

    distances = {start: 0}
    parent = {}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)

        if current == end:
            return reconstruct_path(parent, start, end)

        if current_distance > distances[current]:
            continue

        for next_pos in get_neighbors(maze, current):
            new_distance = current_distance + 1

            if next_pos not in distances or new_distance < distances[next_pos]:
                distances[next_pos] = new_distance
                parent[next_pos] = current
                heapq.heappush(priority_queue, (new_distance, next_pos))

    return []


def bellman_ford_solve(maze):
    start, end = get_start_and_end(maze)
    if start is None or end is None:
        return []

    vertices = get_all_walkable_positions(maze)

    distances = {vertex: float("inf") for vertex in vertices}
    parent = {}

    distances[start] = 0

    for _ in range(len(vertices) - 1):
        changed = False

        for current in vertices:
            if distances[current] == float("inf"):
                continue

            for next_pos in get_neighbors(maze, current):
                new_distance = distances[current] + 1

                if new_distance < distances[next_pos]:
                    distances[next_pos] = new_distance
                    parent[next_pos] = current
                    changed = True

        if not changed:
            break

    if end not in parent and start != end:
        return []

    return reconstruct_path(parent, start, end)


def get_start_and_end(maze):
    start = find_position(maze, START)
    end = find_position(maze, END)
    return start, end


def get_all_walkable_positions(maze):
    positions = []

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] != WALL:
                positions.append((row, col))

    return positions


def get_neighbors(maze, position):
    row, col = position

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for d_row, d_col in directions:
        new_row = row + d_row
        new_col = col + d_col

        if is_valid_position(maze, new_row, new_col):
            neighbors.append((new_row, new_col))

    return neighbors


def is_valid_position(maze, row, col):
    if row < 0 or row >= len(maze):
        return False

    if col < 0 or col >= len(maze[0]):
        return False

    if maze[row][col] == WALL:
        return False

    return True


def reconstruct_path(parent, start, end):
    path = []
    current = end

    while current != start:
        path.append(current)

        if current not in parent:
            return []

        current = parent[current]

    path.append(start)
    path.reverse()

    return path