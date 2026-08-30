# /// script
# dependencies = [
#   "pygame-ce",
# ]
# ///

import asyncio
import sys
import pygame

# =========================================================
# WINDOW SETUP
# =========================================================
WIDTH, HEIGHT = 600, 700
CELL_SIZE = WIDTH // 3

# =========================================================
# COLORS
# =========================================================
WHITE = (255, 255, 255)
BLACK = (15, 15, 20)
BLUE = (50, 100, 255)
RED = (255, 50, 50)
GREEN = (0, 190, 80)
GRAY = (70, 70, 80)

# =========================================================
# BOARD STATE
# =========================================================
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
winner = None
game_over = False


# =========================================================
# DRAW BOARD
# =========================================================
def draw_board(screen, font):

    screen.fill(WHITE)

    # Board lines
    for i in range(1, 3):

        pygame.draw.line(
            screen,
            BLACK,
            (0, i * CELL_SIZE),
            (WIDTH, i * CELL_SIZE),
            6
        )

        pygame.draw.line(
            screen,
            BLACK,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, WIDTH),
            6
        )

    # Draw X and O
    for row in range(3):

        for col in range(3):

            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2

            # X
            if board[row][col] == "X":

                pygame.draw.line(
                    screen,
                    RED,
                    (x - 55, y - 55),
                    (x + 55, y + 55),
                    10
                )

                pygame.draw.line(
                    screen,
                    RED,
                    (x + 55, y - 55),
                    (x - 55, y + 55),
                    10
                )

            # O
            elif board[row][col] == "O":

                pygame.draw.circle(
                    screen,
                    BLUE,
                    (x, y),
                    60,
                    10
                )

    # Bottom status area
    pygame.draw.rect(
        screen,
        BLACK,
        (0, WIDTH, WIDTH, HEIGHT - WIDTH)
    )

    # Status message
    if winner == "X":

        text = font.render(
            "YOU WIN!",
            True,
            GREEN
        )

    elif winner == "O":

        text = font.render(
            "AI WINS!",
            True,
            RED
        )

    elif game_over:

        text = font.render(
            "DRAW GAME!",
            True,
            WHITE
        )

    elif current_player == "X":

        text = font.render(
            "YOUR TURN (X)",
            True,
            WHITE
        )

    else:

        text = font.render(
            "AI THINKING...",
            True,
            WHITE
        )

    screen.blit(
        text,
        text.get_rect(center=(WIDTH // 2, 645))
    )


# =========================================================
# CHECK GAME STATE
# =========================================================
def check_state(b):

    # Rows
    for row in b:

        if row[0] == row[1] == row[2] != "":
            return row[0]

    # Columns
    for col in range(3):

        if b[0][col] == b[1][col] == b[2][col] != "":
            return b[0][col]

    # Diagonal
    if b[0][0] == b[1][1] == b[2][2] != "":
        return b[0][0]

    if b[0][2] == b[1][1] == b[2][0] != "":
        return b[0][2]

    # Empty cells
    for row in b:

        if "" in row:
            return None

    return "Draw"


# =========================================================
# UPDATE GAME STATUS
# =========================================================
def update_game_status():

    global winner
    global game_over

    status = check_state(board)

    if status == "X":

        winner = "X"
        game_over = True

    elif status == "O":

        winner = "O"
        game_over = True

    elif status == "Draw":

        game_over = True


# =========================================================
# MINIMAX AI
# =========================================================
def minimax(temp_board, depth, is_maximizing):

    score = check_state(temp_board)

    if score == "O":
        return 10 - depth

    if score == "X":
        return depth - 10

    if score == "Draw":
        return 0

    # AI
    if is_maximizing:

        best_score = -float("inf")

        for r in range(3):

            for c in range(3):

                if temp_board[r][c] == "":

                    temp_board[r][c] = "O"

                    evaluation = minimax(
                        temp_board,
                        depth + 1,
                        False
                    )

                    temp_board[r][c] = ""

                    best_score = max(
                        best_score,
                        evaluation
                    )

        return best_score

    # Player
    else:

        best_score = float("inf")

        for r in range(3):

            for c in range(3):

                if temp_board[r][c] == "":

                    temp_board[r][c] = "X"

                    evaluation = minimax(
                        temp_board,
                        depth + 1,
                        True
                    )

                    temp_board[r][c] = ""

                    best_score = min(
                        best_score,
                        evaluation
                    )

        return best_score


# =========================================================
# GET BEST AI MOVE
# =========================================================
def get_best_move():

    best_score = -float("inf")
    move = None

    for r in range(3):

        for c in range(3):

            if board[r][c] == "":

                board[r][c] = "O"

                score = minimax(
                    board,
                    0,
                    False
                )

                board[r][c] = ""

                if score > best_score:

                    best_score = score
                    move = (r, c)

    return move


# =========================================================
# RESTART GAME
# =========================================================
def restart_game():

    global board
    global current_player
    global winner
    global game_over

    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    current_player = "X"
    winner = None
    game_over = False


# =========================================================
# HANDLE PLAYER MOVE
# =========================================================
def player_move(mx, my):

    global current_player

    # Only allow clicks inside board
    if my >= WIDTH:
        return

    # Convert screen position to board position
    row = int(my // CELL_SIZE)
    col = int(mx // CELL_SIZE)

    # Safety check
    if row < 0 or row > 2:
        return

    if col < 0 or col > 2:
        return

    # Empty cell
    if board[row][col] == "":

        board[row][col] = "X"

        update_game_status()

        if not game_over:

            current_player = "O"


# =========================================================
# MAIN
# =========================================================
async def main():

    global current_player

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "Tic-Tac-Toe VS AI"
    )

    clock = pygame.time.Clock()

    font = pygame.font.Font(
        None,
        40
    )

    running = True

    while running:

        # =================================================
        # DRAW
        # =================================================
        draw_board(
            screen,
            font
        )

        pygame.display.flip()

        # =================================================
        # AI TURN
        # =================================================
        if current_player == "O" and not game_over:

            await asyncio.sleep(0.3)

            ai_move = get_best_move()

            if ai_move:

                r, c = ai_move

                board[r][c] = "O"

                update_game_status()

                if not game_over:

                    current_player = "X"

        # =================================================
        # EVENTS
        # =================================================
        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:

                running = False

            # Keyboard
            elif event.type == pygame.KEYDOWN:

                # R = restart
                if event.key == pygame.K_r:

                    restart_game()

                # Q = quit
                elif event.key == pygame.K_q:

                    running = False

            # =================================================
            # LAPTOP MOUSE / TOUCHPAD
            # =================================================
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    # Restart if game finished
                    if game_over:

                        restart_game()

                    elif current_player == "X":

                        player_move(
                            event.pos[0],
                            event.pos[1]
                        )

            # =================================================
            # MOBILE / TOUCH SCREEN
            # =================================================
            elif event.type == pygame.FINGERDOWN:

                # Convert touch coordinates
                # (0.0 - 1.0) into screen coordinates
                touch_x = int(
                    event.x * WIDTH
                )

                touch_y = int(
                    event.y * HEIGHT
                )

                # Restart if game finished
                if game_over:

                    restart_game()

                elif current_player == "X":

                    player_move(
                        touch_x,
                        touch_y
                    )

        # =================================================
        # FPS
        # =================================================
        clock.tick(60)

        # Important for Pygbag/browser
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()


# =========================================================
# START
# =========================================================
if __name__ == "__main__":

    asyncio.run(main())