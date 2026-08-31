# /// script
# dependencies = [
#   "pygame-ce",
# ]
# ///

import asyncio
import math
import os
import random
import sys
import pygame
from pygame.locals import *


# =========================================================
# WINDOW SETUP
# =========================================================

WIDTH, HEIGHT = 600, 600

LANES = [60, 180, 300, 420, 540]

SPEED = 7


# =========================================================
# GAME VARIABLES
# =========================================================

current_lane = 2

ship_x = LANES[current_lane]
ship_y = 490

meteor_lane = 0

meteor_x = LANES[meteor_lane]
meteor_y = -100


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global current_lane
    global ship_x
    global ship_y
    global meteor_lane
    global meteor_x
    global meteor_y

    current_lane = 2

    ship_x = LANES[current_lane]
    ship_y = 490

    meteor_lane = random.randint(0, 4)

    meteor_x = LANES[meteor_lane]

    meteor_y = -120


# =========================================================
# LOAD IMAGE
# =========================================================

def load_img(base_dir, name):

    path = os.path.join(base_dir, name)

    if not os.path.exists(path):

        print("Missing image:", path)

        surf = pygame.Surface((100, 100))
        surf.fill((200, 200, 200))

        return surf

    return pygame.image.load(path).convert_alpha()


# =========================================================
# MOVE LEFT
# =========================================================

def move_left():

    global current_lane
    global ship_x

    if current_lane > 0:

        current_lane -= 1

        ship_x = LANES[current_lane]


# =========================================================
# MOVE RIGHT
# =========================================================

def move_right():

    global current_lane
    global ship_x

    if current_lane < 4:

        current_lane += 1

        ship_x = LANES[current_lane]


# =========================================================
# MAIN
# =========================================================

async def main():

    global current_lane
    global ship_x
    global ship_y

    global meteor_lane
    global meteor_x
    global meteor_y


    # =====================================================
    # INITIALIZE
    # =====================================================

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "Space Dodge"
    )

    clock = pygame.time.Clock()


    # =====================================================
    # ASSET DIRECTORY
    # =====================================================

    base_dir = (
        os.path.dirname(__file__)
        if "__file__" in locals()
        else "."
    )


    # =====================================================
    # LOAD BACKGROUND
    # =====================================================

    spacebg = pygame.transform.scale(
        load_img(
            base_dir,
            "Space BG.png"
        ),
        (WIDTH, HEIGHT)
    )


    # =====================================================
    # LOAD TITLE
    # =====================================================

    title = load_img(
        base_dir,
        "Gametitle.png"
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, 140)
    )


    # =====================================================
    # LOAD START MESSAGE
    # =====================================================

    gamestart = load_img(
        base_dir,
        "Start Msg.png"
    )

    gamestart_rect = gamestart.get_rect(
        center=(WIDTH // 2, 320)
    )


    # =====================================================
    # LOAD GAME OVER
    # =====================================================

    gameover = load_img(
        base_dir,
        "Game over.png"
    )

    gameover_rect = gameover.get_rect(
        center=(WIDTH // 2, 280)
    )


    # =====================================================
    # LOAD SPACESHIP
    # =====================================================

    spaceship_img = pygame.transform.scale(
        load_img(
            base_dir,
            "Spaceship.png"
        ),
        (250, 250)
    )


    # =====================================================
    # LOAD METEOR
    # =====================================================

    meteor_img = pygame.transform.scale(
        load_img(
            base_dir,
            "Meteor.png"
        ),
        (220, 220)
    )


    # =====================================================
    # FONTS
    # =====================================================

    font = pygame.font.Font(
        None,
        36
    )


    # =====================================================
    # RESTART TEXT
    # =====================================================

    restart_text = font.render(
        "TOUCH SCREEN OR PRESS R",
        True,
        (255, 255, 255)
    )

    restart_rect = restart_text.get_rect(
        center=(WIDTH // 2, 380)
    )


    # =====================================================
    # TOUCH BUTTONS
    # =====================================================

    # Left button
    left_button = pygame.Rect(
        20,
        500,
        200,
        80
    )

    # Right button
    right_button = pygame.Rect(
        380,
        500,
        200,
        80
    )


    # =====================================================
    # BUTTON FONTS
    # =====================================================

    button_font = pygame.font.Font(
        None,
        42
    )


    # =====================================================
    # GAME STATE
    # =====================================================

    state = "START"

    reset_game()

    running = True


    # =====================================================
    # GAME LOOP
    # =====================================================

    while running:


        # =================================================
        # EVENT LOOP
        # =================================================

        for event in pygame.event.get():


            # =============================================
            # QUIT
            # =============================================

            if event.type == QUIT:

                running = False

                pygame.quit()

                sys.exit()


            # =============================================
            # KEYBOARD
            # =============================================

            if event.type == KEYDOWN:


                # -----------------------------------------
                # START
                # -----------------------------------------

                if state == "START":

                    if event.key in [
                        K_s,
                        K_RETURN,
                        K_SPACE
                    ]:

                        reset_game()

                        state = "PLAYING"


                # -----------------------------------------
                # PLAYING
                # -----------------------------------------

                elif state == "PLAYING":

                    if event.key in [
                        K_a,
                        K_LEFT
                    ]:

                        move_left()


                    elif event.key in [
                        K_d,
                        K_RIGHT
                    ]:

                        move_right()


                # -----------------------------------------
                # GAME OVER
                # -----------------------------------------

                elif state == "GAMEOVER":

                    if event.key in [
                        K_r,
                        K_SPACE,
                        K_RETURN,
                        K_s
                    ]:

                        reset_game()

                        state = "PLAYING"


            # =============================================
            # MOUSE CLICK
            # =============================================

            if event.type == MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_x, mouse_y = event.pos


                    # -------------------------------------
                    # START
                    # -------------------------------------

                    if state == "START":

                        reset_game()

                        state = "PLAYING"


                    # -------------------------------------
                    # PLAYING
                    # -------------------------------------

                    elif state == "PLAYING":

                        if left_button.collidepoint(
                            mouse_x,
                            mouse_y
                        ):

                            move_left()


                        elif right_button.collidepoint(
                            mouse_x,
                            mouse_y
                        ):

                            move_right()


                        # Click left/right side
                        elif mouse_x < WIDTH // 2:

                            move_left()


                        else:

                            move_right()


                    # -------------------------------------
                    # GAME OVER
                    # -------------------------------------

                    elif state == "GAMEOVER":

                        reset_game()

                        state = "PLAYING"


            # =============================================
            # MOBILE TOUCH
            # =============================================

            if event.type == FINGERDOWN:

                # Convert touch coordinates
                # from 0.0 - 1.0
                # to screen coordinates

                touch_x = int(
                    event.x * WIDTH
                )

                touch_y = int(
                    event.y * HEIGHT
                )


                # -----------------------------------------
                # START
                # -----------------------------------------

                if state == "START":

                    reset_game()

                    state = "PLAYING"


                # -----------------------------------------
                # PLAYING
                # -----------------------------------------

                elif state == "PLAYING":

                    if touch_x < WIDTH // 2:

                        move_left()

                    else:

                        move_right()


                # -----------------------------------------
                # GAME OVER
                # -----------------------------------------

                elif state == "GAMEOVER":

                    reset_game()

                    state = "PLAYING"


        # =================================================
        # DRAW BACKGROUND
        # =================================================

        screen.blit(
            spacebg,
            (0, 0)
        )


        # =================================================
        # START SCREEN
        # =================================================

        if state == "START":

            screen.blit(
                title,
                title_rect
            )

            screen.blit(
                gamestart,
                gamestart_rect
            )


        # =================================================
        # PLAYING
        # =================================================

        elif state == "PLAYING":


            # ---------------------------------------------
            # MOVE METEOR
            # ---------------------------------------------

            meteor_y += SPEED


            # ---------------------------------------------
            # RESET METEOR
            # ---------------------------------------------

            if meteor_y > HEIGHT + 80:

                meteor_lane = random.randint(
                    0,
                    4
                )

                meteor_x = LANES[
                    meteor_lane
                ]

                meteor_y = -100


            # ---------------------------------------------
            # SPACESHIP RECT
            # ---------------------------------------------

            ship_rect = spaceship_img.get_rect(
                center=(
                    ship_x,
                    ship_y
                )
            )


            # ---------------------------------------------
            # METEOR RECT
            # ---------------------------------------------

            meteor_rect = meteor_img.get_rect(
                center=(
                    meteor_x,
                    meteor_y
                )
            )


            # ---------------------------------------------
            # DRAW SHIP
            # ---------------------------------------------

            screen.blit(
                spaceship_img,
                ship_rect
            )


            # ---------------------------------------------
            # DRAW METEOR
            # ---------------------------------------------

            screen.blit(
                meteor_img,
                meteor_rect
            )


            # ---------------------------------------------
            # TOUCH CONTROL BUTTONS
            # ---------------------------------------------

            pygame.draw.rect(
                screen,
                (30, 30, 30),
                left_button,
                border_radius=15
            )

            pygame.draw.rect(
                screen,
                (30, 30, 30),
                right_button,
                border_radius=15
            )


            # ---------------------------------------------
            # BUTTON TEXT
            # ---------------------------------------------

            left_text = button_font.render(
                "◀ LEFT",
                True,
                (255, 255, 255)
            )

            right_text = button_font.render(
                "RIGHT ▶",
                True,
                (255, 255, 255)
            )


            screen.blit(
                left_text,
                left_text.get_rect(
                    center=left_button.center
                )
            )

            screen.blit(
                right_text,
                right_text.get_rect(
                    center=right_button.center
                )
            )


            # ---------------------------------------------
            # COLLISION
            # ---------------------------------------------

            dist = math.hypot(
                ship_x - meteor_x,
                ship_y - meteor_y
            )


            if dist < 55:

                state = "GAMEOVER"


        # =================================================
        # GAME OVER
        # =================================================

        elif state == "GAMEOVER":


            # ---------------------------------------------
            # SHIP
            # ---------------------------------------------

            ship_rect = spaceship_img.get_rect(
                center=(
                    ship_x,
                    ship_y
                )
            )


            # ---------------------------------------------
            # METEOR
            # ---------------------------------------------

            meteor_rect = meteor_img.get_rect(
                center=(
                    meteor_x,
                    meteor_y
                )
            )


            screen.blit(
                spaceship_img,
                ship_rect
            )

            screen.blit(
                meteor_img,
                meteor_rect
            )


            # ---------------------------------------------
            # GAME OVER IMAGE
            # ---------------------------------------------

            screen.blit(
                gameover,
                gameover_rect
            )


            # ---------------------------------------------
            # RESTART MESSAGE
            # ---------------------------------------------

            screen.blit(
                restart_text,
                restart_rect
            )


        # =================================================
        # UPDATE DISPLAY
        # =================================================

        pygame.display.update()


        # =================================================
        # FPS
        # =================================================

        clock.tick(60)


        # =================================================
        # IMPORTANT FOR PYGBAG
        # =================================================

        await asyncio.sleep(0)


    pygame.quit()

    sys.exit()


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())
