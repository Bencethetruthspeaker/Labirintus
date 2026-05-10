import pygame
from constants import WALL, START, END
from maze import generate_maze
from solver import bfs_solve


DEFAULT_CELL_SIZE = 30
MIN_CELL_SIZE = 5

MARGIN = 25
MAZE_TOP_OFFSET = 80

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650

BACKGROUND_COLOR = (245, 245, 245)
WALL_COLOR = (20, 20, 20)
TEXT_COLOR = (30, 30, 30)

START_COLOR = (50, 120, 255)
END_COLOR = (255, 70, 70)
SOLUTION_COLOR = (50, 200, 80)

BUTTON_COLOR = (80, 160, 255)
BUTTON_HOVER_COLOR = (50, 130, 230)
BUTTON_TEXT_COLOR = (255, 255, 255)

INPUT_COLOR = (255, 255, 255)
INPUT_ACTIVE_BORDER = (50, 120, 255)
INPUT_BORDER = (80, 80, 80)

WALL_THICKNESS = 2


def start_ui():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Labirintus megoldó")

    font = pygame.font.SysFont("Arial", 28)
    small_font = pygame.font.SysFont("Arial", 22)
    title_font = pygame.font.SysFont("Arial", 42, bold=True)

    rows = 21
    cols = 41

    active_input = None
    input_text = ""

    maze = None
    path = None
    screen_mode = "menu"

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        run_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, 430, 200, 55)

        row_minus = pygame.Rect(310, 210, 45, 45)
        row_plus = pygame.Rect(545, 210, 45, 45)
        row_value_rect = pygame.Rect(WINDOW_WIDTH // 2 - 40, 210, 80, 45)

        col_minus = pygame.Rect(310, 300, 45, 45)
        col_plus = pygame.Rect(545, 300, 45, 45)
        col_value_rect = pygame.Rect(WINDOW_WIDTH // 2 - 40, 300, 80, 45)

        back_button = pygame.Rect(20, 20, 120, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen_mode == "menu":
                    if row_value_rect.collidepoint(mouse_pos):
                        active_input = "rows"
                        input_text = str(rows)

                    elif col_value_rect.collidepoint(mouse_pos):
                        active_input = "cols"
                        input_text = str(cols)

                    elif row_minus.collidepoint(mouse_pos):
                        rows = max(5, rows - 2)
                        active_input = None
                        input_text = ""

                    elif row_plus.collidepoint(mouse_pos):
                        rows += 2
                        active_input = None
                        input_text = ""

                    elif col_minus.collidepoint(mouse_pos):
                        cols = max(5, cols - 2)
                        active_input = None
                        input_text = ""

                    elif col_plus.collidepoint(mouse_pos):
                        cols += 2
                        active_input = None
                        input_text = ""

                    elif run_button.collidepoint(mouse_pos):
                        rows = make_valid_maze_size(rows)
                        cols = make_valid_maze_size(cols)

                        maze = generate_maze(rows, cols)
                        path = bfs_solve(maze)
                        screen_mode = "maze"
                        active_input = None
                        input_text = ""

                    else:
                        active_input = None
                        input_text = ""

                elif screen_mode == "maze":
                    if back_button.collidepoint(mouse_pos):
                        screen_mode = "menu"

            if event.type == pygame.KEYDOWN:
                if screen_mode == "menu":
                    if active_input is not None:
                        if event.key == pygame.K_RETURN:
                            if input_text.isdigit():
                                value = make_valid_maze_size(int(input_text))

                                if active_input == "rows":
                                    rows = value
                                elif active_input == "cols":
                                    cols = value

                            active_input = None
                            input_text = ""

                        elif event.key == pygame.K_ESCAPE:
                            active_input = None
                            input_text = ""

                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]

                        elif event.unicode.isdigit():
                            if len(input_text) < 3:
                                input_text += event.unicode

                    else:
                        if event.key == pygame.K_RETURN:
                            rows = make_valid_maze_size(rows)
                            cols = make_valid_maze_size(cols)

                            maze = generate_maze(rows, cols)
                            path = bfs_solve(maze)
                            screen_mode = "maze"

                elif screen_mode == "maze":
                    if event.key == pygame.K_ESCAPE:
                        screen_mode = "menu"

        screen.fill(BACKGROUND_COLOR)

        if screen_mode == "menu":
            draw_menu(
                screen,
                title_font,
                font,
                small_font,
                rows,
                cols,
                active_input,
                input_text,
                run_button,
                row_minus,
                row_plus,
                row_value_rect,
                col_minus,
                col_plus,
                col_value_rect,
                mouse_pos
            )

        elif screen_mode == "maze":
            draw_maze_screen(screen, maze, path, back_button, small_font, mouse_pos)

        pygame.display.flip()

    pygame.quit()


def make_valid_maze_size(value):
    value = max(5, value)

    if value % 2 == 0:
        value += 1

    return value


def draw_menu(
    screen,
    title_font,
    font,
    small_font,
    rows,
    cols,
    active_input,
    input_text,
    run_button,
    row_minus,
    row_plus,
    row_value_rect,
    col_minus,
    col_plus,
    col_value_rect,
    mouse_pos
):
    title = title_font.render("Labirintus generátor", True, TEXT_COLOR)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 90))

    subtitle = small_font.render(
        "Állítsd be a labirintus méretét, majd indítsd el.",
        True,
        TEXT_COLOR
    )
    screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 145))

    draw_setting_row(
        screen,
        font,
        "Sorok:",
        rows,
        row_minus,
        row_plus,
        row_value_rect,
        mouse_pos,
        active_input == "rows",
        input_text
    )

    draw_setting_row(
        screen,
        font,
        "Oszlopok:",
        cols,
        col_minus,
        col_plus,
        col_value_rect,
        mouse_pos,
        active_input == "cols",
        input_text
    )

    hint = small_font.render(
        "Tipp: kattints a számra, és írd be billentyűzettel.",
        True,
        TEXT_COLOR
    )
    screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, 370))

    draw_button(screen, run_button, "Futtatás", font, mouse_pos)


def draw_setting_row(
    screen,
    font,
    label,
    value,
    minus_button,
    plus_button,
    value_rect,
    mouse_pos,
    is_active,
    input_text
):
    y = value_rect.y

    label_text = font.render(label, True, TEXT_COLOR)
    screen.blit(label_text, (WINDOW_WIDTH // 2 - 210, y + 8))

    draw_button(screen, minus_button, "-", font, mouse_pos)
    draw_button(screen, plus_button, "+", font, mouse_pos)

    pygame.draw.rect(screen, INPUT_COLOR, value_rect, border_radius=8)

    border_color = INPUT_ACTIVE_BORDER if is_active else INPUT_BORDER
    border_width = 3 if is_active else 2
    pygame.draw.rect(screen, border_color, value_rect, border_width, border_radius=8)

    displayed_value = input_text if is_active else str(value)
    value_text = font.render(displayed_value, True, TEXT_COLOR)

    screen.blit(
        value_text,
        (
            value_rect.centerx - value_text.get_width() // 2,
            value_rect.centery - value_text.get_height() // 2
        )
    )


def draw_button(screen, rect, text, font, mouse_pos):
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR

    pygame.draw.rect(screen, color, rect, border_radius=10)

    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    screen.blit(
        text_surface,
        (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2
        )
    )


def draw_maze_screen(screen, maze, path, back_button, font, mouse_pos):
    screen.fill(BACKGROUND_COLOR)

    draw_button(screen, back_button, "Vissza", font, mouse_pos)

    cell_size = calculate_cell_size(maze)

    draw_walls(screen, maze, cell_size)
    draw_solution_path(screen, path, cell_size)
    draw_start_and_end(screen, maze, cell_size)


def calculate_cell_size(maze):
    visual_rows = (len(maze) - 1) // 2
    visual_cols = (len(maze[0]) - 1) // 2

    available_width = WINDOW_WIDTH - MARGIN * 2
    available_height = WINDOW_HEIGHT - MARGIN * 2 - MAZE_TOP_OFFSET

    cell_width = available_width // visual_cols
    cell_height = available_height // visual_rows

    return max(MIN_CELL_SIZE, min(DEFAULT_CELL_SIZE, cell_width, cell_height))


def maze_position_to_screen(row, col, cell_size):
    x = MARGIN + ((col - 1) / 2) * cell_size + cell_size / 2
    y = MARGIN + ((row - 1) / 2) * cell_size + cell_size / 2 + MAZE_TOP_OFFSET
    return int(x), int(y)


def draw_walls(screen, maze, cell_size):
    rows = len(maze)
    cols = len(maze[0])

    for row in range(1, rows, 2):
        for col in range(1, cols, 2):
            x = MARGIN + ((col - 1) // 2) * cell_size
            y = MARGIN + ((row - 1) // 2) * cell_size + MAZE_TOP_OFFSET

            if maze[row - 1][col] == WALL:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    (x, y),
                    (x + cell_size, y),
                    WALL_THICKNESS
                )

            if maze[row + 1][col] == WALL:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    (x, y + cell_size),
                    (x + cell_size, y + cell_size),
                    WALL_THICKNESS
                )

            if maze[row][col - 1] == WALL:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    (x, y),
                    (x, y + cell_size),
                    WALL_THICKNESS
                )

            if maze[row][col + 1] == WALL:
                pygame.draw.line(
                    screen,
                    WALL_COLOR,
                    (x + cell_size, y),
                    (x + cell_size, y + cell_size),
                    WALL_THICKNESS
                )


def draw_solution_path(screen, path, cell_size):
    if len(path) < 2:
        return

    points = []

    for row, col in path:
        x, y = maze_position_to_screen(row, col, cell_size)
        points.append((x, y))

    pygame.draw.lines(
        screen,
        SOLUTION_COLOR,
        False,
        points,
        max(2, cell_size // 5)
    )


def draw_start_and_end(screen, maze, cell_size):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == START:
                draw_marker(screen, row, col, START_COLOR, cell_size)
            elif maze[row][col] == END:
                draw_marker(screen, row, col, END_COLOR, cell_size)


def draw_marker(screen, row, col, color, cell_size):
    x, y = maze_position_to_screen(row, col, cell_size)

    pygame.draw.circle(
        screen,
        color,
        (x, y),
        max(2, cell_size // 5)
    )