# /// script
# dependencies = [
#   "pygame-ce",
# ]
# ///

import asyncio
import pygame

pygame.init()

# =========================================================
# SCREEN
# =========================================================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VS_GAME - Breakout")

clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================

WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
RED = (220, 60, 60)
BLUE = (60, 130, 220)
GREEN = (60, 200, 120)
YELLOW = (230, 200, 60)
ORANGE = (240, 140, 50)

# =========================================================
# FONTS
# =========================================================

title_font = pygame.font.Font(None, 80)
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# =========================================================
# GAME SETTINGS
# =========================================================

PADDLE_WIDTH = 110
PADDLE_HEIGHT = 16
PADDLE_SPEED = 8

BALL_RADIUS = 9

BRICK_ROWS = 5
BRICK_COLS = 10

BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 28

# =========================================================
# GAME VARIABLES
# =========================================================

score = 0
lives = 3

game_started = False
game_over = False
you_win = False

# =========================================================
# PADDLE
# =========================================================

paddle = pygame.Rect(
    WIDTH // 2 - PADDLE_WIDTH // 2,
    HEIGHT - 50,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# =========================================================
# BALL
# =========================================================

ball = pygame.Rect(
    WIDTH // 2 - BALL_RADIUS,
    HEIGHT // 2 - BALL_RADIUS,
    BALL_RADIUS * 2,
    BALL_RADIUS * 2
)

ball_x = float(WIDTH // 2)
ball_y = float(HEIGHT // 2)

ball_speed_x = 5.0
ball_speed_y = -5.0

# =========================================================
# BRICKS
# =========================================================

brick_colors = [
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    BLUE
]


def create_bricks():

    new_bricks = []

    for row in range(BRICK_ROWS):

        for col in range(BRICK_COLS):

            brick = pygame.Rect(
                col * BRICK_WIDTH + 2,
                row * BRICK_HEIGHT + 60,
                BRICK_WIDTH - 4,
                BRICK_HEIGHT - 4
            )

            color = brick_colors[row]

            new_bricks.append(
                (brick, color)
            )

    return new_bricks


bricks = create_bricks()

# =========================================================
# RESET BALL
# =========================================================

def reset_ball():

    global ball_x
    global ball_y
    global ball_speed_x
    global ball_speed_y

    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2

    ball.center = (
        int(ball_x),
        int(ball_y)
    )

    ball_speed_x = 5.0
    ball_speed_y = -5.0

    paddle.centerx = WIDTH // 2


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global score
    global lives
    global game_started
    global game_over
    global you_win
    global bricks

    score = 0
    lives = 3

    game_started = True
    game_over = False
    you_win = False

    bricks = create_bricks()

    reset_ball()


# =========================================================
# DRAW CENTER TEXT
# =========================================================

def draw_center_text(
    text,
    font_used,
    color,
    y
):

    text_surface = font_used.render(
        text,
        True,
        color
    )

    x = (
        WIDTH // 2
        - text_surface.get_width() // 2
    )

    screen.blit(
        text_surface,
        (x, y)
    )


# =========================================================
# MOVE PADDLE TO POSITION
# =========================================================

def move_paddle_to(x):

    paddle.centerx = int(x)

    if paddle.left < 0:
        paddle.left = 0

    if paddle.right > WIDTH:
        paddle.right = WIDTH


# =========================================================
# MAIN GAME
# =========================================================

async def main():

    global game_started
    global game_over
    global you_win

    global score
    global lives

    global ball_x
    global ball_y

    global ball_speed_x
    global ball_speed_y

    global bricks

    running = True

    while running:

        # -------------------------------------------------
        # PYGBAG
        # -------------------------------------------------

        await asyncio.sleep(0)

        clock.tick(60)

        # -------------------------------------------------
        # EVENTS
        # -------------------------------------------------

        for event in pygame.event.get():

            # -------------------------------------------------
            # QUIT
            # -------------------------------------------------

            if event.type == pygame.QUIT:

                running = False

            # -------------------------------------------------
            # KEYBOARD
            # -------------------------------------------------

            elif event.type == pygame.KEYDOWN:

                # Start
                if event.key == pygame.K_SPACE:

                    if not game_started:
                        reset_game()

                # Restart
                elif event.key == pygame.K_r:

                    if game_over or you_win:
                        reset_game()

                # Quit
                elif event.key == pygame.K_ESCAPE:

                    running = False

            # -------------------------------------------------
            # MOUSE CLICK
            # -------------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x = event.pos[0]

                # Start
                if not game_started:

                    reset_game()

                    move_paddle_to(mouse_x)

                # Restart
                elif game_over or you_win:

                    reset_game()

                    move_paddle_to(mouse_x)

                # Move paddle
                else:

                    move_paddle_to(mouse_x)

            # -------------------------------------------------
            # MOUSE MOVE
            # -------------------------------------------------

            elif event.type == pygame.MOUSEMOTION:

                if (
                    game_started
                    and not game_over
                    and not you_win
                ):

                    mouse_x = event.pos[0]

                    move_paddle_to(mouse_x)

            # -------------------------------------------------
            # TOUCH
            # -------------------------------------------------

            elif event.type == pygame.FINGERDOWN:

                touch_x = event.x * WIDTH

                # Start
                if not game_started:

                    reset_game()

                    move_paddle_to(touch_x)

                # Restart
                elif game_over or you_win:

                    reset_game()

                    move_paddle_to(touch_x)

                # Move paddle
                else:

                    move_paddle_to(touch_x)

            # -------------------------------------------------
            # TOUCH MOVE
            # -------------------------------------------------

            elif event.type == pygame.FINGERMOTION:

                if (
                    game_started
                    and not game_over
                    and not you_win
                ):

                    touch_x = event.x * WIDTH

                    move_paddle_to(touch_x)

        # =====================================================
        # KEYBOARD PADDLE CONTROL
        # =====================================================

        if (
            game_started
            and not game_over
            and not you_win
        ):

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:

                paddle.x -= PADDLE_SPEED

            if keys[pygame.K_RIGHT]:

                paddle.x += PADDLE_SPEED

            # Keep paddle inside screen

            if paddle.left < 0:
                paddle.left = 0

            if paddle.right > WIDTH:
                paddle.right = WIDTH

        # =====================================================
        # GAME UPDATE
        # =====================================================

        if (
            game_started
            and not game_over
            and not you_win
        ):

            # -------------------------------------------------
            # BALL MOVEMENT
            # -------------------------------------------------

            ball_x += ball_speed_x
            ball_y += ball_speed_y

            ball.center = (
                int(ball_x),
                int(ball_y)
            )

            # -------------------------------------------------
            # LEFT WALL
            # -------------------------------------------------

            if ball.left <= 0:

                ball.left = 0

                ball_x = ball.centerx

                ball_speed_x = abs(
                    ball_speed_x
                )

            # -------------------------------------------------
            # RIGHT WALL
            # -------------------------------------------------

            if ball.right >= WIDTH:

                ball.right = WIDTH

                ball_x = ball.centerx

                ball_speed_x = -abs(
                    ball_speed_x
                )

            # -------------------------------------------------
            # TOP WALL
            # -------------------------------------------------

            if ball.top <= 0:

                ball.top = 0

                ball_y = ball.centery

                ball_speed_y = abs(
                    ball_speed_y
                )

            # -------------------------------------------------
            # PADDLE COLLISION
            # -------------------------------------------------

            if (
                ball.colliderect(paddle)
                and ball_speed_y > 0
            ):

                ball.bottom = paddle.top

                ball_y = ball.centery

                ball_speed_y = -abs(
                    ball_speed_y
                )

                # Calculate hit position

                offset = (
                    ball.centerx
                    - paddle.centerx
                ) / (PADDLE_WIDTH / 2)

                ball_speed_x = offset * 6

                # Prevent straight vertical movement

                if abs(ball_speed_x) < 1.5:

                    if ball.centerx < paddle.centerx:

                        ball_speed_x = -1.5

                    else:

                        ball_speed_x = 1.5

            # -------------------------------------------------
            # BRICK COLLISION
            # -------------------------------------------------

            for brick_data in bricks[:]:

                brick, color = brick_data

                if ball.colliderect(brick):

                    bricks.remove(
                        brick_data
                    )

                    score += 10

                    # Collision direction

                    overlap_left = (
                        ball.right
                        - brick.left
                    )

                    overlap_right = (
                        brick.right
                        - ball.left
                    )

                    overlap_top = (
                        ball.bottom
                        - brick.top
                    )

                    overlap_bottom = (
                        brick.bottom
                        - ball.top
                    )

                    smallest_horizontal = min(
                        overlap_left,
                        overlap_right
                    )

                    smallest_vertical = min(
                        overlap_top,
                        overlap_bottom
                    )

                    if (
                        smallest_horizontal
                        < smallest_vertical
                    ):

                        ball_speed_x *= -1

                    else:

                        ball_speed_y *= -1

                    break

            # -------------------------------------------------
            # BALL FALLS
            # -------------------------------------------------

            if ball.top > HEIGHT:

                lives -= 1

                if lives <= 0:

                    game_over = True

                else:

                    reset_ball()

            # -------------------------------------------------
            # WIN
            # -------------------------------------------------

            if len(bricks) == 0:

                you_win = True

        # =====================================================
        # DRAW BACKGROUND
        # =====================================================

        screen.fill(BLACK)

        # =====================================================
        # DRAW BRICKS
        # =====================================================

        for brick, color in bricks:

            pygame.draw.rect(
                screen,
                color,
                brick,
                border_radius=5
            )

        # =====================================================
        # DRAW PADDLE
        # =====================================================

        pygame.draw.rect(
            screen,
            WHITE,
            paddle,
            border_radius=8
        )

        # =====================================================
        # DRAW BALL
        # =====================================================

        pygame.draw.circle(
            screen,
            WHITE,
            ball.center,
            BALL_RADIUS
        )

        # =====================================================
        # HUD
        # =====================================================

        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        lives_text = font.render(
            f"Lives: {lives}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (15, 15)
        )

        screen.blit(
            lives_text,
            (WIDTH - 120, 15)
        )

        # =====================================================
        # START SCREEN
        # =====================================================

        if not game_started:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            overlay.set_alpha(220)

            overlay.fill(BLACK)

            screen.blit(
                overlay,
                (0, 0)
            )

            draw_center_text(
                "BREAKOUT",
                title_font,
                RED,
                180
            )

            draw_center_text(
                "TAP / CLICK TO START",
                font,
                WHITE,
                290
            )

            draw_center_text(
                "Touch or mouse to move paddle",
                small_font,
                BLUE,
                340
            )

            draw_center_text(
                "Keyboard: LEFT / RIGHT",
                small_font,
                GREEN,
                375
            )

        # =====================================================
        # GAME OVER
        # =====================================================

        if game_over:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            overlay.set_alpha(210)

            overlay.fill(BLACK)

            screen.blit(
                overlay,
                (0, 0)
            )

            draw_center_text(
                "GAME OVER",
                title_font,
                RED,
                200
            )

            draw_center_text(
                f"Score: {score}",
                font,
                WHITE,
                290
            )

            draw_center_text(
                "TAP / CLICK TO RESTART",
                font,
                YELLOW,
                350
            )

            draw_center_text(
                "or press R",
                small_font,
                WHITE,
                395
            )

        # =====================================================
        # WIN SCREEN
        # =====================================================

        if you_win:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            overlay.set_alpha(210)

            overlay.fill(BLACK)

            screen.blit(
                overlay,
                (0, 0)
            )

            draw_center_text(
                "YOU WIN!",
                title_font,
                GREEN,
                200
            )

            draw_center_text(
                f"Score: {score}",
                font,
                WHITE,
                290
            )

            draw_center_text(
                "TAP / CLICK TO PLAY AGAIN",
                font,
                YELLOW,
                350
            )

            draw_center_text(
                "or press R",
                small_font,
                WHITE,
                395
            )

        # =====================================================
        # DISPLAY
        # =====================================================

        pygame.display.flip()

    pygame.quit()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())
