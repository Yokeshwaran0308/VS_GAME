# /// script
# dependencies = [
#     "pygame-ce",
# ]
# ///

import asyncio
import random
import pygame


# =========================================================
# SETTINGS
# =========================================================

WIDTH = 800
HEIGHT = 600

SNAKE_BLOCK = 20
FPS = 10

# =========================================================
# GAME AREA
# =========================================================
# The bottom part of the screen is reserved for buttons.

GAME_TOP = 40
GAME_BOTTOM = 400


# =========================================================
# COLORS
# =========================================================

BLACK = (0, 0, 0)

GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)

RED = (255, 60, 60)

WHITE = (255, 255, 255)

GRAY = (150, 150, 150)

BLUE = (40, 150, 255)
DARK_BLUE = (20, 80, 150)

YELLOW = (255, 220, 50)


# =========================================================
# DRAW SNAKE
# =========================================================

def draw_snake(screen, snake_list):

    for i, block in enumerate(snake_list):

        if i == len(snake_list) - 1:

            color = GREEN

        else:

            color = DARK_GREEN

        pygame.draw.rect(
            screen,
            color,
            (
                block[0],
                block[1],
                SNAKE_BLOCK,
                SNAKE_BLOCK
            ),
            border_radius=4
        )


# =========================================================
# SCORE
# =========================================================

def show_score(screen, font, score):

    text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        text,
        (15, 8)
    )


# =========================================================
# CENTER TEXT
# =========================================================

def center_text(
    screen,
    font,
    text,
    color,
    y
):

    message = font.render(
        text,
        True,
        color
    )

    rect = message.get_rect(
        center=(WIDTH // 2, y)
    )

    screen.blit(
        message,
        rect
    )


# =========================================================
# DRAW TOUCH BUTTON
# =========================================================

def draw_button(
    screen,
    rect,
    text,
    font
):

    # Button background
    pygame.draw.rect(
        screen,
        BLUE,
        rect,
        border_radius=12
    )

    # Button border
    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        2,
        border_radius=12
    )

    # Button text
    text_surface = font.render(
        text,
        True,
        WHITE
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    screen.blit(
        text_surface,
        text_rect
    )


# =========================================================
# START SCREEN
# =========================================================

async def start_screen(
    screen,
    font
):

    waiting = True

    while waiting:

        screen.fill(BLACK)

        center_text(
            screen,
            font,
            "SNAKE GAME",
            GREEN,
            180
        )

        center_text(
            screen,
            font,
            "CLICK / TOUCH TO START",
            WHITE,
            250
        )

        center_text(
            screen,
            font,
            "Use Arrow Keys or Touch Buttons",
            GRAY,
            300
        )

        pygame.display.flip()

        for event in pygame.event.get():

            # Quit
            if event.type == pygame.QUIT:

                return False

            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:

                waiting = False

            # Keyboard
            elif event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_SPACE,
                    pygame.K_RETURN
                ):

                    waiting = False

            # Mobile touch
            elif event.type == pygame.FINGERDOWN:

                waiting = False

        await asyncio.sleep(0)

    return True


# =========================================================
# GAME OVER SCREEN
# =========================================================

async def game_over_screen(
    screen,
    font,
    score
):

    waiting = True

    while waiting:

        screen.fill(BLACK)

        center_text(
            screen,
            font,
            "GAME OVER",
            RED,
            180
        )

        center_text(
            screen,
            font,
            f"Score: {score}",
            WHITE,
            240
        )

        center_text(
            screen,
            font,
            "PRESS R OR TOUCH TO RESTART",
            YELLOW,
            300
        )

        center_text(
            screen,
            font,
            "Press Q to Quit",
            GRAY,
            350
        )

        pygame.display.flip()

        for event in pygame.event.get():

            # Quit
            if event.type == pygame.QUIT:

                return "quit"

            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:

                return "restart"

            # Keyboard
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    return "restart"

                elif event.key == pygame.K_q:

                    return "quit"

            # Touch
            elif event.type == pygame.FINGERDOWN:

                return "restart"

        await asyncio.sleep(0)

    return "restart"


# =========================================================
# SNAKE GAME
# =========================================================

async def play_game(
    screen,
    font,
    clock,
    button_font
):

    # =====================================================
    # START POSITION
    # =====================================================

    x = WIDTH // 2

    y = 200

    x_change = 0

    y_change = 0

    snake_list = []

    snake_length = 1


    # =====================================================
    # FOOD POSITION
    # =====================================================

    food_x = random.randrange(
        0,
        WIDTH - SNAKE_BLOCK,
        SNAKE_BLOCK
    )

    food_y = random.randrange(
        GAME_TOP,
        GAME_BOTTOM - SNAKE_BLOCK,
        SNAKE_BLOCK
    )


    # =====================================================
    # GAME OVER
    # =====================================================

    game_over = False


    # =====================================================
    # TOUCH BUTTONS
    # =====================================================

    up_button = pygame.Rect(
        350,
        415,
        100,
        50
    )

    left_button = pygame.Rect(
        235,
        475,
        100,
        50
    )

    down_button = pygame.Rect(
        350,
        475,
        100,
        50
    )

    right_button = pygame.Rect(
        465,
        475,
        100,
        50
    )


    # =====================================================
    # GAME LOOP
    # =====================================================

    while not game_over:


        # =================================================
        # EVENTS
        # =================================================

        for event in pygame.event.get():

            # ---------------------------------------------
            # QUIT
            # ---------------------------------------------

            if event.type == pygame.QUIT:

                return "quit"


            # ---------------------------------------------
            # KEYBOARD
            # ---------------------------------------------

            elif event.type == pygame.KEYDOWN:


                # LEFT
                if (
                    event.key == pygame.K_LEFT
                    and x_change == 0
                ):

                    x_change = -SNAKE_BLOCK

                    y_change = 0


                # RIGHT
                elif (
                    event.key == pygame.K_RIGHT
                    and x_change == 0
                ):

                    x_change = SNAKE_BLOCK

                    y_change = 0


                # UP
                elif (
                    event.key == pygame.K_UP
                    and y_change == 0
                ):

                    y_change = -SNAKE_BLOCK

                    x_change = 0


                # DOWN
                elif (
                    event.key == pygame.K_DOWN
                    and y_change == 0
                ):

                    y_change = SNAKE_BLOCK

                    x_change = 0


            # ---------------------------------------------
            # MOUSE / TOUCH CLICK
            # ---------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x, mouse_y = event.pos


                # UP
                if up_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    if y_change == 0:

                        y_change = -SNAKE_BLOCK

                        x_change = 0


                # LEFT
                elif left_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    if x_change == 0:

                        x_change = -SNAKE_BLOCK

                        y_change = 0


                # DOWN
                elif down_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    if y_change == 0:

                        y_change = SNAKE_BLOCK

                        x_change = 0


                # RIGHT
                elif right_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    if x_change == 0:

                        x_change = SNAKE_BLOCK

                        y_change = 0


            # ---------------------------------------------
            # DIRECT MOBILE TOUCH
            # ---------------------------------------------

            elif event.type == pygame.FINGERDOWN:

                touch_x = int(
                    event.x * WIDTH
                )

                touch_y = int(
                    event.y * HEIGHT
                )


                # UP
                if up_button.collidepoint(
                    touch_x,
                    touch_y
                ):

                    if y_change == 0:

                        y_change = -SNAKE_BLOCK

                        x_change = 0


                # LEFT
                elif left_button.collidepoint(
                    touch_x,
                    touch_y
                ):

                    if x_change == 0:

                        x_change = -SNAKE_BLOCK

                        y_change = 0


                # DOWN
                elif down_button.collidepoint(
                    touch_x,
                    touch_y
                ):

                    if y_change == 0:

                        y_change = SNAKE_BLOCK

                        x_change = 0


                # RIGHT
                elif right_button.collidepoint(
                    touch_x,
                    touch_y
                ):

                    if x_change == 0:

                        x_change = SNAKE_BLOCK

                        y_change = 0


        # =================================================
        # MOVE SNAKE
        # =================================================

        x += x_change

        y += y_change


        # =================================================
        # WALL COLLISION
        # =================================================

        if (
            x < 0
            or x >= WIDTH
            or y < GAME_TOP
            or y >= GAME_BOTTOM
        ):

            game_over = True


        # =================================================
        # SNAKE HEAD
        # =================================================

        snake_head = [
            x,
            y
        ]

        snake_list.append(
            snake_head
        )


        # =================================================
        # SNAKE LENGTH
        # =================================================

        if len(snake_list) > snake_length:

            del snake_list[0]


        # =================================================
        # SELF COLLISION
        # =================================================

        for block in snake_list[:-1]:

            if block == snake_head:

                game_over = True


        # =================================================
        # DRAW BACKGROUND
        # =================================================

        screen.fill(BLACK)


        # =================================================
        # GAME AREA BORDER
        # =================================================

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (
                0,
                GAME_TOP,
                WIDTH,
                GAME_BOTTOM - GAME_TOP
            ),
            2
        )


        # =================================================
        # FOOD
        # =================================================

        pygame.draw.rect(
            screen,
            RED,
            (
                food_x,
                food_y,
                SNAKE_BLOCK,
                SNAKE_BLOCK
            ),
            border_radius=4
        )


        # =================================================
        # SNAKE
        # =================================================

        draw_snake(
            screen,
            snake_list
        )


        # =================================================
        # SCORE
        # =================================================

        show_score(
            screen,
            font,
            snake_length - 1
        )


        # =================================================
        # CONTROL AREA
        # =================================================

        pygame.draw.line(
            screen,
            GRAY,
            (0, 405),
            (WIDTH, 405),
            2
        )


        # =================================================
        # TOUCH BUTTONS
        # =================================================

        draw_button(
            screen,
            up_button,
            "UP",
            button_font
        )

        draw_button(
            screen,
            left_button,
            "LEFT",
            button_font
        )

        draw_button(
            screen,
            down_button,
            "DOWN",
            button_font
        )

        draw_button(
            screen,
            right_button,
            "RIGHT",
            button_font
        )


        # =================================================
        # DISPLAY
        # =================================================

        pygame.display.flip()


        # =================================================
        # FOOD COLLISION
        # =================================================

        if x == food_x and y == food_y:

            snake_length += 1


            # Create new food only inside game area
            food_x = random.randrange(
                0,
                WIDTH - SNAKE_BLOCK,
                SNAKE_BLOCK
            )

            food_y = random.randrange(
                GAME_TOP,
                GAME_BOTTOM - SNAKE_BLOCK,
                SNAKE_BLOCK
            )


        # =================================================
        # FPS
        # =================================================

        clock.tick(FPS)


        # =================================================
        # PYGBAG
        # =================================================

        await asyncio.sleep(0)


    # =====================================================
    # GAME OVER
    # =====================================================

    return "game_over", snake_length - 1


# =========================================================
# MAIN
# =========================================================

async def main():

    pygame.init()


    # =====================================================
    # SCREEN
    # =====================================================

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )


    pygame.display.set_caption(
        "Snake Game"
    )


    # =====================================================
    # CLOCK
    # =====================================================

    clock = pygame.time.Clock()


    # =====================================================
    # FONTS
    # =====================================================

    font = pygame.font.Font(
        None,
        35
    )

    button_font = pygame.font.Font(
        None,
        27
    )


    # =====================================================
    # START SCREEN
    # =====================================================

    started = await start_screen(
        screen,
        font
    )


    if not started:

        pygame.quit()

        return


    # =====================================================
    # MAIN LOOP
    # =====================================================

    while True:


        result = await play_game(
            screen,
            font,
            clock,
            button_font
        )


        # -------------------------------------------------
        # QUIT
        # -------------------------------------------------

        if result == "quit":

            break


        # -------------------------------------------------
        # GAME OVER
        # -------------------------------------------------

        if isinstance(result, tuple):

            state, score = result

            if state == "game_over":

                result = await game_over_screen(
                    screen,
                    font,
                    score
                )


                if result == "quit":

                    break


    # =====================================================
    # QUIT
    # =====================================================

    pygame.quit()


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())
