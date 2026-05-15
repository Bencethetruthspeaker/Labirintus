import pygame
import random
import string
from constants import WALL, START, END
from maze import generate_maze
from solver import run_selected_solvers


DEFAULT_CELL_SIZE = 30
MIN_CELL_SIZE = 5

MIN_MAZE_SIZE = 5
MAX_MAZE_SIZE = 93

MARGIN = 25
MAZE_TOP_OFFSET = 80

MAX_SEED_LENGTH = 10

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
    pygame.key.set_repeat(0)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Maze Runner")

    font = pygame.font.SysFont("Arial", 28)
    small_font = pygame.font.SysFont("Arial", 22)
    title_font = pygame.font.SysFont("Arial", 42, bold=True)

    rows = 21
    cols = 41
    extra_connections = 20
    current_seed = ""
    seed_mode = "random"

    active_input = None
    input_text = ""
    held_button = None
    hold_start_time = 0
    last_repeat_time = 0

    maze = None
    path = None
    screen_mode = "main_menu"
    player_position = None
    game_started = False
    game_finished = False
    game_start_time = 0
    game_elapsed_time = 0
    player_steps = 0
    game_bfs_result = None
    player_path = []

    selected_solvers = {
        "BFS": True,
        "DFS": True,
        "Dijkstra": True,
        "Bellman-Ford": True
    }

    solver_results = {}

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        window_width, window_height = screen.get_size()
        center_x = window_width // 2
        center_y = window_height // 2
        current_time = pygame.time.get_ticks()

        game_button = pygame.Rect(center_x - 120, center_y - 40, 240, 60)
        solver_button = pygame.Rect(center_x - 120, center_y + 50, 240, 60)

        base_y = center_y - 140

        col_y = base_y + 90
        extra_y = base_y + 180
        mode_y = base_y + 245
        seed_y = base_y + 305
        run_y = base_y + 390

        run_button = pygame.Rect(window_width // 2 - 100, run_y, 200, 55)

        row_minus = pygame.Rect(center_x - 20, base_y, 45, 45)
        row_value_rect = pygame.Rect(center_x + 75, base_y, 80, 45)
        row_plus = pygame.Rect(center_x + 200, base_y, 45, 45)

        col_minus = pygame.Rect(center_x - 20, col_y, 45, 45)
        col_value_rect = pygame.Rect(center_x + 75, col_y, 80, 45)
        col_plus = pygame.Rect(center_x + 200, col_y, 45, 45)

        extra_minus = pygame.Rect(center_x - 20, extra_y, 45, 45)
        extra_value_rect = pygame.Rect(center_x + 75, extra_y, 80, 45)
        extra_plus = pygame.Rect(center_x + 200, extra_y, 45, 45)

        random_mode_button = pygame.Rect(center_x - 260, mode_y, 250, 45)
        seed_mode_button = pygame.Rect(center_x + 20, mode_y, 250, 45)

        seed_input_rect = pygame.Rect(center_x + 75, seed_y, 180, 45)

        back_button = pygame.Rect(20, 20, 120, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen_mode == "main_menu":
                    if game_button.collidepoint(mouse_pos):
                        screen_mode = "game_menu"

                    elif solver_button.collidepoint(mouse_pos):
                        screen_mode = "solver_menu"
                elif screen_mode == "solver_menu":
                    if back_button.collidepoint(mouse_pos):
                        screen_mode = "main_menu"
                        held_button = None
                        active_input = None
                        input_text = ""
                    
                    elif random_mode_button.collidepoint(mouse_pos):
                        seed_mode = "random"

                    elif seed_mode_button.collidepoint(mouse_pos):
                        seed_mode = "seed"

                    elif row_value_rect.collidepoint(mouse_pos):
                        rows, cols, extra_connections, current_seed = apply_active_input(
                            active_input,
                            input_text,
                            rows,
                            cols,
                            extra_connections,
                            current_seed
                        )
                        active_input = "rows"
                        input_text = ""

                    elif col_value_rect.collidepoint(mouse_pos):
                        rows, cols, extra_connections, current_seed = apply_active_input(
                            active_input,
                            input_text,
                            rows,
                            cols,
                            extra_connections,
                            current_seed
                        )
                        active_input = "cols"
                        input_text = ""
                    elif extra_value_rect.collidepoint(mouse_pos):
                        rows, cols, extra_connections, current_seed = apply_active_input(
                            active_input,
                            input_text,
                            rows,
                            cols,
                            extra_connections,
                            current_seed
                        )
                        active_input = "extra"
                        input_text = ""
                    
                    elif seed_input_rect.collidepoint(mouse_pos):
                        seed_mode = "seed"
                        input_text = current_seed
                        active_input = "seed"

                    elif row_minus.collidepoint(mouse_pos):
                        rows = make_valid_maze_size(rows - 2)
                        held_button = "row_minus"
                        hold_start_time = current_time
                        last_repeat_time = current_time
                        active_input = None
                        input_text = ""

                    elif row_plus.collidepoint(mouse_pos):
                        rows = make_valid_maze_size(rows + 2)
                        held_button = "row_plus"
                        hold_start_time = current_time
                        last_repeat_time = current_time
                        active_input = None
                        input_text = ""

                    elif col_minus.collidepoint(mouse_pos):
                        cols = make_valid_maze_size(cols - 2)
                        held_button = "col_minus"
                        hold_start_time = current_time
                        last_repeat_time = current_time
                        active_input = None
                        input_text = ""

                    elif col_plus.collidepoint(mouse_pos):
                        cols = make_valid_maze_size(cols + 2)
                        held_button = "col_plus"
                        hold_start_time = current_time
                        last_repeat_time = current_time
                        active_input = None
                        input_text = ""
                    elif extra_minus.collidepoint(mouse_pos):
                        extra_connections = max(0, extra_connections - 1)
                        held_button = "extra_minus"
                        hold_start_time = current_time
                        last_repeat_time = current_time
                        active_input = None
                        input_text = ""

                    elif extra_plus.collidepoint(mouse_pos):
                        extra_connections += 1
                        held_button = "extra_plus"
                        hold_start_time = current_time
                        last_repeat_time = current_time
                        active_input = None
                        input_text = ""

                    elif run_button.collidepoint(mouse_pos):
                        rows = make_valid_maze_size(rows)
                        cols = make_valid_maze_size(cols)
                        held_button = None

                        if seed_mode == "random":
                            current_seed = generate_random_seed()
                        elif current_seed == "":
                            current_seed = generate_random_seed()

                        maze = generate_maze(rows, cols, extra_connections, seed=current_seed)
                        solver_results = run_selected_solvers(maze, selected_solvers)

                        path = []
                        if "BFS" in solver_results:
                            path = solver_results["BFS"]["path"]
                        screen_mode = "maze"
                        active_input = None
                        input_text = ""

                    else:
                        rows, cols, extra_connections, current_seed = apply_active_input(
                            active_input,
                            input_text,
                            rows,
                            cols,
                            extra_connections,
                            current_seed
                        )
                        active_input = None
                        input_text = ""
                elif screen_mode == "game_menu":
                        if back_button.collidepoint(mouse_pos):
                            screen_mode = "main_menu"
                            held_button = None
                            active_input = None
                            input_text = ""

                        elif random_mode_button.collidepoint(mouse_pos):
                            seed_mode = "random"

                        elif seed_mode_button.collidepoint(mouse_pos):
                            seed_mode = "seed"

                        elif row_value_rect.collidepoint(mouse_pos):
                            rows, cols, extra_connections, current_seed = apply_active_input(
                                active_input, input_text, rows, cols, extra_connections, current_seed
                            )
                            active_input = "rows"
                            input_text = ""

                        elif col_value_rect.collidepoint(mouse_pos):
                            rows, cols, extra_connections, current_seed = apply_active_input(
                                active_input, input_text, rows, cols, extra_connections, current_seed
                            )
                            active_input = "cols"
                            input_text = ""

                        elif extra_value_rect.collidepoint(mouse_pos):
                            rows, cols, extra_connections, current_seed = apply_active_input(
                                active_input, input_text, rows, cols, extra_connections, current_seed
                            )
                            active_input = "extra"
                            input_text = ""

                        elif seed_input_rect.collidepoint(mouse_pos):
                            seed_mode = "seed"
                            input_text = current_seed
                            active_input = "seed"

                        elif row_minus.collidepoint(mouse_pos):
                            rows = make_valid_maze_size(rows - 2)
                            held_button = "row_minus"
                            hold_start_time = current_time
                            last_repeat_time = current_time
                            active_input = None
                            input_text = ""

                        elif row_plus.collidepoint(mouse_pos):
                            rows = make_valid_maze_size(rows + 2)
                            held_button = "row_plus"
                            hold_start_time = current_time
                            last_repeat_time = current_time
                            active_input = None
                            input_text = ""

                        elif col_minus.collidepoint(mouse_pos):
                            cols = make_valid_maze_size(cols - 2)
                            held_button = "col_minus"
                            hold_start_time = current_time
                            last_repeat_time = current_time
                            active_input = None
                            input_text = ""

                        elif col_plus.collidepoint(mouse_pos):
                            cols = make_valid_maze_size(cols + 2)
                            held_button = "col_plus"
                            hold_start_time = current_time
                            last_repeat_time = current_time
                            active_input = None
                            input_text = ""

                        elif extra_minus.collidepoint(mouse_pos):
                            extra_connections = max(0, extra_connections - 1)
                            held_button = "extra_minus"
                            hold_start_time = current_time
                            last_repeat_time = current_time
                            active_input = None
                            input_text = ""

                        elif extra_plus.collidepoint(mouse_pos):
                            extra_connections += 1
                            held_button = "extra_plus"
                            hold_start_time = current_time
                            last_repeat_time = current_time
                            active_input = None
                            input_text = ""

                        elif run_button.collidepoint(mouse_pos):
                            rows = make_valid_maze_size(rows)
                            cols = make_valid_maze_size(cols)
                            held_button = None

                            if seed_mode == "random":
                                current_seed = generate_random_seed()
                            elif current_seed == "":
                                current_seed = generate_random_seed()

                            maze = generate_maze(rows, cols, extra_connections, seed=current_seed)
                            player_position = find_player_start(maze)
                            player_path = [player_position]

                            selected_bfs = {"BFS": True}
                            game_solver_results = run_selected_solvers(maze, selected_bfs)
                            game_bfs_result = game_solver_results.get("BFS")

                            game_started = False
                            game_finished = False
                            game_start_time = 0
                            game_elapsed_time = 0
                            player_steps = 0

                            path = []
                            solver_results = {}
                            screen_mode = "game"

                            active_input = None
                            input_text = ""

                        else:
                            rows, cols, extra_connections, current_seed = apply_active_input(
                                active_input, input_text, rows, cols, extra_connections, current_seed
                            )
                            active_input = None
                            input_text = ""

                elif screen_mode == "maze":
                    if back_button.collidepoint(mouse_pos):
                        screen_mode = "solver_menu"
                elif screen_mode == "game":
                    if back_button.collidepoint(mouse_pos):
                        screen_mode = "game_menu"

            if event.type == pygame.MOUSEBUTTONUP:
                held_button = None        

            if event.type == pygame.KEYDOWN:
                if screen_mode in ("solver_menu", "game_menu"):
                    if active_input is not None:
                        if event.key == pygame.K_RETURN:
                            if active_input == "seed":
                                current_seed = input_text[:MAX_SEED_LENGTH]

                            elif input_text.strip().isdigit():
                                value = make_valid_maze_size(input_text.strip())

                                if active_input == "rows":
                                    rows = value
                                elif active_input == "cols":
                                    cols = value
                                elif active_input == "extra":
                                    extra_connections = max(0, min(200, int(input_text)))

                            active_input = None
                            input_text = ""

                        elif event.key == pygame.K_ESCAPE:
                            active_input = None
                            input_text = ""

                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]

                        elif active_input == "seed":
                            if event.unicode.isalnum():
                                if len(input_text) < MAX_SEED_LENGTH:
                                    input_text += event.unicode

                        elif event.unicode.isdigit():
                            if len(input_text) < 3:
                                input_text += event.unicode

                    else:
                        if event.key == pygame.K_RETURN:
                            rows = make_valid_maze_size(rows)
                            cols = make_valid_maze_size(cols)

                            if seed_mode == "random":
                                current_seed = generate_random_seed()
                            elif current_seed == "":
                                current_seed = generate_random_seed()

                            maze = generate_maze(rows, cols, extra_connections, seed=current_seed)
                            solver_results = run_selected_solvers(maze, selected_solvers)

                            path = []
                            if "BFS" in solver_results:
                                path = solver_results["BFS"]["path"]
                            screen_mode = "maze"
                elif screen_mode == "game":
                    if event.key == pygame.K_ESCAPE:
                        screen_mode = "main_menu"

                elif screen_mode == "maze":
                    if event.key == pygame.K_ESCAPE:
                        screen_mode = "main_menu"

        if held_button is not None:
            if current_time - hold_start_time >= 700:
                if current_time - last_repeat_time >= 120:
                    if held_button == "row_plus":
                        rows = make_valid_maze_size(rows + 2)
                    elif held_button == "row_minus":
                        rows = make_valid_maze_size(rows - 2)
                    elif held_button == "col_plus":
                        cols = make_valid_maze_size(cols + 2)
                    elif held_button == "col_minus":
                        cols = make_valid_maze_size(cols - 2)
                    elif held_button == "extra_plus":
                        extra_connections += 1
                    elif held_button == "extra_minus":
                        extra_connections = max(0, extra_connections - 1)

                    last_repeat_time = current_time
        pressed_keys = pygame.key.get_pressed()

        if screen_mode == "game":
            if current_time - last_repeat_time >= 120:
                if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
                    old_position = player_position
                    player_position, player_steps, game_started, game_start_time, game_finished, game_elapsed_time = handle_player_move(
                        maze,
                        player_position,
                        pygame.K_UP,
                        player_steps,
                        game_started,
                        game_start_time,
                        game_finished,
                        game_elapsed_time
                    )
                    if player_position != old_position:
                        player_path.append(player_position)
                    last_repeat_time = current_time
                elif pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
                    old_position = player_position
                    player_position, player_steps, game_started, game_start_time, game_finished, game_elapsed_time = handle_player_move(
                        maze,
                        player_position,
                        pygame.K_DOWN,
                        player_steps,
                        game_started,
                        game_start_time,
                        game_finished,
                        game_elapsed_time
                    )
                    if player_position != old_position:
                        player_path.append(player_position)
                    last_repeat_time = current_time
                elif pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
                    old_position = player_position
                    player_position, player_steps, game_started, game_start_time, game_finished, game_elapsed_time = handle_player_move(
                        maze,
                        player_position,
                        pygame.K_LEFT,
                        player_steps,
                        game_started,
                        game_start_time,
                        game_finished,
                        game_elapsed_time
                    )
                    if player_position != old_position:
                        player_path.append(player_position)
                    last_repeat_time = current_time
                elif pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
                    old_position = player_position
                    player_position, player_steps, game_started, game_start_time, game_finished, game_elapsed_time = handle_player_move(
                        maze,
                        player_position,
                        pygame.K_RIGHT,
                        player_steps,
                        game_started,
                        game_start_time,
                        game_finished,
                        game_elapsed_time
                    )
                    if player_position != old_position:
                        player_path.append(player_position)
                    last_repeat_time = current_time

        if screen_mode == "game" and game_started and not game_finished:
            game_elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000

        screen.fill(BACKGROUND_COLOR)

        if screen_mode == "main_menu":
                draw_main_menu(
                    screen,
                    title_font,
                    font,
                    game_button,
                    solver_button,
                    mouse_pos
                )

        elif screen_mode == "solver_menu":
                draw_menu(
                    screen,
                    title_font,
                    font,
                    small_font,
                    rows,
                    cols,
                    extra_connections,
                    active_input,
                    input_text,
                    run_button,
                    row_minus,
                    row_plus,
                    row_value_rect,
                    col_minus,
                    col_plus,
                    col_value_rect,
                    extra_minus,
                    extra_plus,
                    extra_value_rect,
                    mouse_pos,
                    seed_mode,
                    current_seed,
                    seed_input_rect,
                    random_mode_button,
                    seed_mode_button,
                )


        elif screen_mode == "game_menu":
            draw_game_menu(
                screen,
                title_font,
                font,
                small_font,
                rows,
                cols,
                extra_connections,
                active_input,
                input_text,
                run_button,
                row_minus,
                row_plus,
                row_value_rect,
                col_minus,
                col_plus,
                col_value_rect,
                extra_minus,
                extra_plus,
                extra_value_rect,
                mouse_pos,
                seed_mode,
                current_seed,
                seed_input_rect,
                random_mode_button,
                seed_mode_button,
            )

        elif screen_mode == "game":
            draw_game_play_screen(
                screen,
                maze,
                back_button,
                small_font,
                mouse_pos,
                current_seed,
                player_position,
                game_elapsed_time,
                player_steps,
                game_finished,
                game_bfs_result,
                player_path
            )

        elif screen_mode == "maze":
                draw_maze_screen(
                    screen,
                    maze,
                    path,
                    back_button,
                    small_font,
                    mouse_pos,
                    current_seed,
                    solver_results
                )

        pygame.display.flip()

    pygame.quit()

def apply_active_input(active_input, input_text, rows, cols, extra_connections, current_seed):
    if active_input is None:
        return rows, cols, extra_connections, current_seed

    if active_input == "seed":
        current_seed = input_text[:MAX_SEED_LENGTH]

    elif input_text.strip().isdigit():
        if active_input == "rows":
            rows = make_valid_maze_size(input_text.strip())
        elif active_input == "cols":
            cols = make_valid_maze_size(input_text.strip())
        elif active_input == "extra":
            extra_connections = max(0, min(200, int(input_text.strip())))

    return rows, cols, extra_connections, current_seed

def make_valid_maze_size(value):
    value = int(value)

    if value < MIN_MAZE_SIZE:
        value = MIN_MAZE_SIZE

    if value > MAX_MAZE_SIZE:
        value = MAX_MAZE_SIZE

    if value % 2 == 0:
        value -= 1

    return value

def draw_main_menu(screen, title_font, font, game_button, solver_button, mouse_pos):
    window_width, window_height = screen.get_size()
    title = title_font.render("Maze Runner", True, TEXT_COLOR)
    screen.blit(title, (window_width // 2 - title.get_width() // 2, 140))

    draw_button(screen, game_button, "Game", font, mouse_pos)
    draw_button(screen, solver_button, "Solver", font, mouse_pos)

def draw_game_screen(screen, back_button, font, mouse_pos):
    screen.fill(BACKGROUND_COLOR)

    draw_button(screen, back_button, "Menu", font, mouse_pos)

    text = font.render("Game mód később jön.", True, TEXT_COLOR)
    screen.blit(
        text,
        (
            WINDOW_WIDTH // 2 - text.get_width() // 2,
            WINDOW_HEIGHT // 2 - text.get_height() // 2
        )
    )

def draw_menu(
    screen,
    title_font,
    font,
    small_font,
    rows,
    cols,
    extra_connections,
    active_input,
    input_text,
    run_button,
    row_minus,
    row_plus,
    row_value_rect,
    col_minus,
    col_plus,
    col_value_rect,
    extra_minus,
    extra_plus,
    extra_value_rect,
    mouse_pos,
    seed_mode,
    current_seed,
    seed_input_rect,
    random_mode_button,
    seed_mode_button,
):
    title = title_font.render("Labyrinth Solver", True, TEXT_COLOR)
    window_width, window_height = screen.get_size()
    center_y = window_height // 2

    screen.blit(title, (window_width // 2 - title.get_width() // 2, center_y - 230))
    menu_button = pygame.Rect(20, 20, 120, 40)
    draw_button(screen, menu_button, "Menu", small_font, mouse_pos)

    draw_mode_button(
        screen,
        random_mode_button,
        "Random Labyrinth",
        font,
        mouse_pos,
        seed_mode == "random"
    )

    draw_mode_button(
        screen,
        seed_mode_button,
        "Import From Seed",
        font,
        mouse_pos,
        seed_mode == "seed"
    )


    draw_setting_row(
        screen,
        font,
        "Rows:",
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
        "Columns:",
        cols,
        col_minus,
        col_plus,
        col_value_rect,
        mouse_pos,
        active_input == "cols",
        input_text
    )

    draw_setting_row(
        screen,
        font,
        "Extra paths:",
        extra_connections,
        extra_minus,
        extra_plus,
        extra_value_rect,
        mouse_pos,
        active_input == "extra",
        input_text
    )

    if seed_mode == "seed":
        seed_label = font.render("Seed:", True, TEXT_COLOR)
        screen.blit(seed_label, (420, 522))

        pygame.draw.rect(screen, INPUT_COLOR, seed_input_rect, border_radius=8)

        border_color = INPUT_ACTIVE_BORDER if active_input == "seed" else INPUT_BORDER

        pygame.draw.rect(
            screen,
            border_color,
            seed_input_rect,
            3,
            border_radius=8
        )

        seed_display = current_seed if active_input != "seed" else input_text
        seed_text_surface = font.render(seed_display, True, TEXT_COLOR)

        screen.blit(
            seed_text_surface,
            (
                seed_input_rect.x + 10,
                seed_input_rect.y + 7
            )
        )
    draw_button(screen, run_button, "Run", font, mouse_pos)


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
    label_x = value_rect.x - 340
    screen.blit(label_text, (label_x, y + 8))

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

def draw_mode_button(screen, rect, text, font, mouse_pos, is_selected):
    if is_selected:
        color = (40, 110, 220)
    elif rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR

    pygame.draw.rect(screen, color, rect, border_radius=12)

    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)

    screen.blit(
        text_surface,
        (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2
        )
    )


def draw_maze_screen(screen, maze, path, back_button, font, mouse_pos, current_seed, solver_results):
    screen.fill(BACKGROUND_COLOR)

    draw_button(screen, back_button, "Return", font, mouse_pos)
    seed_text = font.render(f"Seed: {current_seed}", True, TEXT_COLOR)
    screen.blit(seed_text, (160, 28))

    cell_size = calculate_cell_size(maze, screen)

    draw_walls(screen, maze, cell_size)
    draw_solution_path(screen, path, cell_size)
    draw_start_and_end(screen, maze, cell_size)
    draw_solver_results(screen, solver_results, font)

def draw_game_play_screen(screen, maze, back_button, font, mouse_pos, current_seed, player_position, game_elapsed_time, player_steps, game_finished, game_bfs_result, player_path):
    screen.fill(BACKGROUND_COLOR)

    draw_button(screen, back_button, "Return", font, mouse_pos)

    seed_text = font.render(f"Seed: {current_seed}", True, TEXT_COLOR)
    screen.blit(seed_text, (160, 28))

    cell_size = calculate_cell_size(maze, screen)

    draw_walls(screen, maze, cell_size)
    if game_finished:
        draw_colored_path(screen, game_bfs_result["path"], cell_size, SOLUTION_COLOR)
        draw_colored_path(screen, player_path, cell_size, (255, 60, 60))

    draw_start_and_end(screen, maze, cell_size)
    draw_player(screen, player_position, cell_size)
    draw_game_stats(screen, font, game_elapsed_time, player_steps, game_finished, game_bfs_result)

def calculate_cell_size(maze,screen):
    window_width, window_height = screen.get_size()
    visual_rows = (len(maze) - 1) // 2
    visual_cols = (len(maze[0]) - 1) // 2

    available_width = window_width - MARGIN * 2
    available_height = window_height - MARGIN * 2 - MAZE_TOP_OFFSET

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
def generate_random_seed(length=MAX_SEED_LENGTH):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def draw_solver_results(screen, solver_results, font):
    window_width, _ = screen.get_size()
    x = window_width - 260
    y = 100

    title = font.render("Solver results", True, TEXT_COLOR)
    screen.blit(title, (x, y))

    y += 45

    sorted_results = sorted(
        solver_results.items(),
        key=lambda item: (item[1]["path_length"], item[1]["time"])
    )

    for name, result in sorted_results:
        path_length = result["path_length"]
        elapsed_time = result["time"]

        name_text = font.render(name, True, TEXT_COLOR)
        screen.blit(name_text, (x, y))
        y += 28

        time_text = font.render(f"Time: {elapsed_time:.6f}s", True, TEXT_COLOR)
        screen.blit(time_text, (x, y))
        y += 28

        length_text = font.render(f"Path length: {path_length}", True, TEXT_COLOR)
        screen.blit(length_text, (x, y))
        y += 42

def draw_game_menu(
    screen,
    title_font,
    font,
    small_font,
    rows,
    cols,
    extra_connections,
    active_input,
    input_text,
    run_button,
    row_minus,
    row_plus,
    row_value_rect,
    col_minus,
    col_plus,
    col_value_rect,
    extra_minus,
    extra_plus,
    extra_value_rect,
    mouse_pos,
    seed_mode,
    current_seed,
    seed_input_rect,
    random_mode_button,
    seed_mode_button,
):
    draw_menu(
        screen,
        title_font,
        font,
        small_font,
        rows,
        cols,
        extra_connections,
        active_input,
        input_text,
        run_button,
        row_minus,
        row_plus,
        row_value_rect,
        col_minus,
        col_plus,
        col_value_rect,
        extra_minus,
        extra_plus,
        extra_value_rect,
        mouse_pos,
        seed_mode,
        current_seed,
        seed_input_rect,
        random_mode_button,
        seed_mode_button,
    )
def move_player(maze, player_position, key):
    if player_position is None:
        return None

    row, col = player_position

    if key in (pygame.K_UP, pygame.K_w):
        d_row, d_col = -2, 0
    elif key in (pygame.K_DOWN, pygame.K_s):
        d_row, d_col = 2, 0
    elif key in (pygame.K_LEFT, pygame.K_a):
        d_row, d_col = 0, -2
    elif key in (pygame.K_RIGHT, pygame.K_d):
        d_row, d_col = 0, 2
    else:
        return player_position

    wall_row = row + d_row // 2
    wall_col = col + d_col // 2

    new_row = row + d_row
    new_col = col + d_col

    if new_row < 0 or new_row >= len(maze):
        return player_position

    if new_col < 0 or new_col >= len(maze[0]):
        return player_position

    if maze[wall_row][wall_col] == WALL:
        return player_position
    
    if new_row % 2 == 0 or new_col % 2 == 0:
        return player_position

    return (new_row, new_col)


def draw_player(screen, player_position, cell_size):
    if player_position is None:
        return

    row, col = player_position
    x, y = maze_position_to_screen(row, col, cell_size)

    pygame.draw.circle(
        screen,
        (255, 170, 0),
        (x, y),
        max(8, cell_size // 3)
    )

    pygame.draw.circle(
        screen,
        (0, 0, 0),
        (x, y),
        max(8, cell_size // 3),
        2
    )

def find_player_start(maze):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == START:
                return (row, col)

    return (1, 1)

def is_player_at_end(maze, player_position):
    if player_position is None:
        return False

    row, col = player_position

    return maze[row][col] == END


def draw_game_stats(screen, font, game_elapsed_time, player_steps, game_finished, game_bfs_result):
    window_width, _ = screen.get_size()
    x = window_width - 260
    y = 100

    title = font.render("Game stats", True, TEXT_COLOR)
    screen.blit(title, (x, y))
    y += 45

    time_text = font.render(f"Time: {game_elapsed_time:.2f}s", True, TEXT_COLOR)
    screen.blit(time_text, (x, y))
    y += 32

    steps_text = font.render(f"Steps: {player_steps}", True, TEXT_COLOR)
    screen.blit(steps_text, (x, y))
    y += 45

    if game_finished:
        finished_text = font.render("Finished!", True, TEXT_COLOR)
        screen.blit(finished_text, (x, y))
        y += 45

    if game_bfs_result is not None:
        bfs_title = font.render("BFS optimal", True, TEXT_COLOR)
        screen.blit(bfs_title, (x, y))
        y += 32

        bfs_time = font.render(f"Time: {game_bfs_result['time']:.6f}s", True, TEXT_COLOR)
        screen.blit(bfs_time, (x, y))
        y += 32

        optimal_steps = max(0, (game_bfs_result["path_length"] - 1) // 2)
        bfs_length = font.render(f"Optimal steps: {optimal_steps}", True, TEXT_COLOR)
        screen.blit(bfs_length, (x, y))

def handle_player_move(
    maze,
    player_position,
    key,
    player_steps,
    game_started,
    game_start_time,
    game_finished,
    game_elapsed_time
):
    old_position = player_position

    if not game_started:
        game_started = True
        game_start_time = pygame.time.get_ticks()

    player_position = move_player(maze, player_position, key)

    if player_position != old_position:
        player_steps += 1

    if is_player_at_end(maze, player_position):
        game_finished = True
        game_elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000

    return player_position, player_steps, game_started, game_start_time, game_finished, game_elapsed_time

def draw_colored_path(screen, path, cell_size, color):
    if path is None or len(path) < 2:
        return

    points = []

    for row, col in path:
        x, y = maze_position_to_screen(row, col, cell_size)
        points.append((x, y))

    pygame.draw.lines(
        screen,
        color,
        False,
        points,
        max(2, cell_size // 5)
    )