# /// script
# dependencies = [
#     "pygame-ce",
# ]
# ///

import asyncio
import random
import sys
import pygame


# =========================================================
# SETTINGS
# =========================================================

WIDTH = 900
HEIGHT = 700


# =========================================================
# COLORS
# =========================================================

WHITE = (255, 255, 255)
BLACK = (15, 18, 35)

DARK_BLUE = (20, 30, 90)
BLUE = (45, 150, 230)
LIGHT_BLUE = (70, 200, 255)

PURPLE = (145, 90, 220)
CYAN = (40, 200, 200)
GREEN = (60, 210, 130)
ORANGE = (245, 170, 60)
RED = (240, 70, 80)
YELLOW = (255, 215, 60)


# =========================================================
# GAME VARIABLES
# =========================================================

secret_num = 0
attempts = 0

selected_number = ""

message = "Choose a number and press GUESS"
message_color = WHITE

game_won = False


# =========================================================
# BUTTON CLASS
# =========================================================

class Button:

    def __init__(self, x, y, width, height, text, color):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text
        self.color = color


    def draw(self, screen, font, selected=False):

        # Mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Button color
        if selected:

            draw_color = YELLOW

        elif self.rect.collidepoint(mouse_pos):

            draw_color = tuple(
                min(value + 35, 255)
                for value in self.color
            )

        else:

            draw_color = self.color


        # Button
        pygame.draw.rect(
            screen,
            draw_color,
            self.rect,
            border_radius=10
        )


        # Border
        pygame.draw.rect(
            screen,
            WHITE,
            self.rect,
            width=2,
            border_radius=10
        )


        # Text
        text_surface = font.render(
            self.text,
            True,
            BLACK if selected else WHITE
        )


        text_rect = text_surface.get_rect(
            center=self.rect.center
        )


        screen.blit(
            text_surface,
            text_rect
        )


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global secret_num
    global attempts
    global selected_number
    global message
    global message_color
    global game_won


    secret_num = random.randint(
        1,
        50
    )

    attempts = 0

    selected_number = ""

    message = "Choose a number and press GUESS"

    message_color = WHITE

    game_won = False


# =========================================================
# ADD NUMBER
# =========================================================

def add_number(number):

    global selected_number


    # Maximum 2 digits
    if len(selected_number) >= 2:
        return


    # Don't allow 0 as first digit
    if number == 0 and selected_number == "":
        return


    new_number = selected_number + str(number)


    try:

        value = int(new_number)

    except ValueError:

        return


    # Only allow 1 - 50
    if 1 <= value <= 50:

        selected_number = new_number


# =========================================================
# CHECK GUESS
# =========================================================

def check_guess():

    global attempts
    global selected_number
    global message
    global message_color
    global game_won


    # No number
    if selected_number == "":

        message = "Please select a number first!"

        message_color = YELLOW

        return


    number = int(selected_number)


    # Safety check
    if number < 1 or number > 50:

        message = "Please choose a number from 1 to 50!"

        message_color = RED

        selected_number = ""

        return


    # Increase attempts
    attempts += 1


    # Correct
    if number == secret_num:

        message = "CORRECT! YOU WIN!"

        message_color = GREEN

        game_won = True

        return


    # Too low
    if number < secret_num:

        message = "TOO LOW! TRY A HIGHER NUMBER"

        message_color = CYAN


    # Too high
    else:

        message = "TOO HIGH! TRY A LOWER NUMBER"

        message_color = ORANGE


    # Clear selected number
    selected_number = ""


# =========================================================
# PROCESS TOUCH / MOUSE
# =========================================================

def handle_position(
    x,
    y,
    number_buttons,
    guess_button,
    play_again_button,
    quit_button
):

    global selected_number
    global game_won


    # =====================================================
    # NORMAL GAME
    # =====================================================

    if not game_won:


        # -----------------------------------------------
        # NUMBER BUTTONS
        # -----------------------------------------------

        for index, button in enumerate(number_buttons):

            if button.rect.collidepoint(x, y):

                # Button number
                number = index + 1

                # Directly select number
                selected_number = str(number)

                return


        # -----------------------------------------------
        # GUESS BUTTON
        # -----------------------------------------------

        if guess_button.rect.collidepoint(x, y):

            check_guess()

            return


    # =====================================================
    # WIN SCREEN
    # =====================================================

    else:


        # -----------------------------------------------
        # PLAY AGAIN
        # -----------------------------------------------

        if play_again_button.rect.collidepoint(x, y):

            reset_game()

            return


        # -----------------------------------------------
        # QUIT
        # -----------------------------------------------

        if quit_button.rect.collidepoint(x, y):

            game_won = False

            return


# =========================================================
# MAIN
# =========================================================

async def main():

    global selected_number


    # =====================================================
    # PYGAME INIT
    # =====================================================

    pygame.init()


    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )


    pygame.display.set_caption(
        "Guess The Number"
    )


    clock = pygame.time.Clock()


    # =====================================================
    # FONTS
    # =====================================================

    title_font = pygame.font.Font(
        None,
        65
    )

    big_font = pygame.font.Font(
        None,
        50
    )

    font = pygame.font.Font(
        None,
        32
    )

    small_font = pygame.font.Font(
        None,
        26
    )


    # =====================================================
    # NUMBER BUTTONS
    # =====================================================

    number_buttons = []


    button_width = 70
    button_height = 45

    gap_x = 12
    gap_y = 10

    start_x = 65
    start_y = 315


    row_colors = [
        BLUE,
        PURPLE,
        CYAN,
        ORANGE,
        GREEN
    ]


    for number in range(1, 51):

        row = (number - 1) // 10

        col = (number - 1) % 10


        x = start_x + col * (
            button_width + gap_x
        )


        y = start_y + row * (
            button_height + gap_y
        )


        number_buttons.append(
            Button(
                x,
                y,
                button_width,
                button_height,
                str(number),
                row_colors[row]
            )
        )


    # =====================================================
    # CONTROL BUTTONS
    # =====================================================

    guess_button = Button(
        350,
        615,
        200,
        55,
        "GUESS",
        GREEN
    )


    play_again_button = Button(
        330,
        400,
        240,
        55,
        "PLAY AGAIN",
        GREEN
    )


    quit_button = Button(
        330,
        475,
        240,
        55,
        "QUIT",
        RED
    )


    # =====================================================
    # START GAME
    # =====================================================

    reset_game()


    running = True


    # =====================================================
    # GAME LOOP
    # =====================================================

    while running:


        # =================================================
        # DRAW BACKGROUND
        # =================================================

        screen.fill(DARK_BLUE)


        # Decorative circles

        pygame.draw.circle(
            screen,
            PURPLE,
            (40, 40),
            25
        )


        pygame.draw.circle(
            screen,
            CYAN,
            (860, 55),
            30
        )


        pygame.draw.circle(
            screen,
            GREEN,
            (40, 650),
            25
        )


        pygame.draw.circle(
            screen,
            ORANGE,
            (860, 650),
            28
        )


        # =================================================
        # TITLE
        # =================================================

        title = title_font.render(
            "GUESS THE NUMBER",
            True,
            YELLOW
        )


        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 55)
            )
        )


        # =================================================
        # INSTRUCTIONS
        # =================================================

        info = font.render(
            "Find the secret number between 1 and 50",
            True,
            WHITE
        )


        screen.blit(
            info,
            info.get_rect(
                center=(WIDTH // 2, 105)
            )
        )


        # =================================================
        # SELECTED NUMBER BOX
        # =================================================

        pygame.draw.rect(
            screen,
            BLACK,
            (280, 130, 340, 60),
            border_radius=15
        )


        pygame.draw.rect(
            screen,
            LIGHT_BLUE,
            (280, 130, 340, 60),
            3,
            border_radius=15
        )


        if selected_number == "":

            display_text = "Choose 1 - 50"

        else:

            display_text = selected_number


        selected_surface = big_font.render(
            display_text,
            True,
            WHITE
        )


        screen.blit(
            selected_surface,
            selected_surface.get_rect(
                center=(WIDTH // 2, 160)
            )
        )


        # =================================================
        # ATTEMPTS
        # =================================================

        attempts_text = font.render(
            f"Attempts: {attempts}",
            True,
            YELLOW
        )


        screen.blit(
            attempts_text,
            attempts_text.get_rect(
                center=(WIDTH // 2, 215)
            )
        )


        # =================================================
        # MESSAGE
        # =================================================

        message_surface = small_font.render(
            message,
            True,
            message_color
        )


        screen.blit(
            message_surface,
            message_surface.get_rect(
                center=(WIDTH // 2, 255)
            )
        )


        # =================================================
        # NORMAL GAME
        # =================================================

        if not game_won:


            # Number buttons

            for index, button in enumerate(
                number_buttons
            ):

                selected = (
                    selected_number
                    == str(index + 1)
                )


                button.draw(
                    screen,
                    font,
                    selected
                )


            # Guess button

            guess_button.draw(
                screen,
                font
            )


        # =================================================
        # WIN SCREEN
        # =================================================

        else:


            # Dark overlay

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )


            overlay.fill(
                (0, 0, 0, 200)
            )


            screen.blit(
                overlay,
                (0, 0)
            )


            # YOU WIN

            win_text = title_font.render(
                "YOU WIN!",
                True,
                GREEN
            )


            screen.blit(
                win_text,
                win_text.get_rect(
                    center=(WIDTH // 2, 220)
                )
            )


            # Answer

            answer_text = big_font.render(
                f"The number was {secret_num}",
                True,
                WHITE
            )


            screen.blit(
                answer_text,
                answer_text.get_rect(
                    center=(WIDTH // 2, 280)
                )
            )


            # Attempts

            win_attempts = font.render(
                f"You found it in {attempts} attempts!",
                True,
                YELLOW
            )


            screen.blit(
                win_attempts,
                win_attempts.get_rect(
                    center=(WIDTH // 2, 335)
                )
            )


            # Play again

            play_again_button.draw(
                screen,
                font
            )


            # Quit

            quit_button.draw(
                screen,
                font
            )


        # =================================================
        # EVENTS
        # =================================================

        for event in pygame.event.get():


            # =================================================
            # QUIT
            # =================================================

            if event.type == pygame.QUIT:

                running = False


            # =================================================
            # KEYBOARD
            # =================================================

            elif event.type == pygame.KEYDOWN:


                # -----------------------------------------
                # RESTART
                # -----------------------------------------

                if event.key == pygame.K_r:

                    reset_game()


                # -----------------------------------------
                # ENTER / GUESS
                # -----------------------------------------

                elif event.key == pygame.K_RETURN:

                    if not game_won:

                        check_guess()


                # -----------------------------------------
                # BACKSPACE
                # -----------------------------------------

                elif event.key == pygame.K_BACKSPACE:

                    if not game_won:

                        selected_number = ""


                # -----------------------------------------
                # NUMBER KEYS
                # -----------------------------------------

                elif not game_won:

                    if pygame.K_0 <= event.key <= pygame.K_9:

                        digit = (
                            event.key
                            - pygame.K_0
                        )

                        add_number(digit)


            # =================================================
            # MOUSE
            # =================================================

            elif event.type == pygame.MOUSEBUTTONDOWN:


                if event.button == 1:

                    mouse_x, mouse_y = event.pos


                    handle_position(
                        mouse_x,
                        mouse_y,
                        number_buttons,
                        guess_button,
                        play_again_button,
                        quit_button
                    )


            # =================================================
            # MOBILE TOUCH
            # =================================================

            elif event.type == pygame.FINGERDOWN:


                # Pygbag touch coordinates
                # are 0.0 - 1.0

                touch_x = int(
                    event.x * WIDTH
                )


                touch_y = int(
                    event.y * HEIGHT
                )


                handle_position(
                    touch_x,
                    touch_y,
                    number_buttons,
                    guess_button,
                    play_again_button,
                    quit_button
                )


        # =================================================
        # DISPLAY
        # =================================================

        pygame.display.flip()


        # =================================================
        # FPS
        # =================================================

        clock.tick(60)


        # =================================================
        # PYGBAG
        # =================================================

        await asyncio.sleep(0)


    pygame.quit()

    sys.exit()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())
