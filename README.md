MAZE RUNNER
===========

A Python + Pygame based maze generation and solving project.

The application contains two main modes:

1. Game Mode
2. Solver Mode


FEATURES
========

- Random maze generation
- Seed-based maze reproduction
- Adjustable maze size
- Adjustable extra path count
- Multiple pathfinding algorithms
- Real-time playable maze
- Live game statistics
- Optimal path comparison after finishing
- Responsive maze scaling based on window size


GAME MODE
=========

In Game Mode the player solves the generated maze manually.

Configurable settings:
- Rows: number of maze rows
- Columns: number of maze columns
- Extra paths: additional openings added to the maze
- Random Labyrinth: generates a random maze
- Import From Seed: recreates the same maze using a seed

Controls:
- Arrow keys
- WASD keys

The game tracks:
- elapsed time
- player steps

After reaching the goal:
- the player's path is drawn in red
- the optimal BFS path is drawn in green
- BFS runtime is displayed
- optimal path length is displayed


SOLVER MODE
===========

In Solver Mode the maze is solved automatically using multiple algorithms.

Implemented algorithms:
- BFS
- DFS
- Dijkstra
- Bellman-Ford

The solver displays:
- algorithm name
- runtime
- path length

Results are sorted by:
1. path length
2. runtime


SEED SYSTEM
===========

The project supports deterministic maze generation using seeds.

Using the same:
- seed
- row count
- column count
- extra path count

will always generate the exact same maze.

Maximum seed length:
- 10 characters

Allowed seed characters:
- letters
- numbers


PROJECT FILES
=============

main.py
- Application entry point.

ui.py
- Complete graphical user interface.
- Menu handling.
- Game mode.
- Solver mode.
- Maze rendering.
- Player movement.
- Statistics rendering.

maze.py
- Maze generation logic.
- Extra path generation.
- Seed-based generation.

solver.py
- Pathfinding algorithms.
- BFS, DFS, Dijkstra and Bellman-Ford implementations.

constants.py
- Maze constants and shared values.


REQUIREMENTS
============

Required software:
- Python 3.10 or newer
- Pygame

Python package installation:

pip install pygame


RUNNING THE PROJECT
===================

Run the program with:

python main.py


TECHNOLOGIES
============

- Python
- Pygame


AUTHORS
=======

Developed by:
- Hornyik Bence
- Hajdu Veronika