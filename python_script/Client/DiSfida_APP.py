#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This is the MAIN of Aequus training app.

The script includes: interactive application suitable for
rehabilitation of people with multiple sclerosis, setup and calibration of
MPU6050 sensors, reading and processing data from sensors.

All credits go to the people who collaborated on the project
of the DiSfida non profit competition organized by the Politecnico di Milano in
collaboration with NEARlab.
"""

__author__ = "Manuel Carzaniga, Lorenzo Gualniera."
__credits__ = ["Manuel Carzaniga", "Lorenzo Gualniera"]
__version__ = "1.0.1"

import os
import pygame
import time

# Import HangGlide minigame
from HangGlider_game import Canyon_flight

# Import classes from disfida_menu
from disfida_menu import Init_menu
from disfida_menu import Main_menu
from disfida_menu import Pref_menu
from disfida_menu import Setup_menu
from disfida_menu import Train_menu

# Pygame constants
W_SIZE = 480            # Width in pixel
H_SIZE = 320            # Height in pixel
FPS = 60                # Frame per second


def select_menu(posx, posy):
    """Select the screen requested by the user."""
    global Menu_APP, Duration, Difficulty
    MENU_STATE = Menu_APP.controls(posx, posy)
    if Menu_APP.__class__.__name__ == "Main_menu":
        if MENU_STATE == "Training":
            Menu_APP = Train_menu(Surface)
        # TODO: implement the others button on the main menu
        '''
        elif MENU_STATE == "Progress":
            Menu_APP = Prog_menu(Surface)
        elif MENU_STATE == "Options":
            Menu_APP = Option_menu(Surface)
        '''
    elif Menu_APP.__class__.__name__ == "Train_menu":
        if MENU_STATE == "Home":
            Menu_APP = Main_menu(Surface)
        elif MENU_STATE == "Start":
            Menu_APP = Init_menu(Surface, Duration, Difficulty)
        elif MENU_STATE == "Preference":
            Menu_APP = Pref_menu(Surface, Duration, Difficulty)
    elif Menu_APP.__class__.__name__ == "Pref_menu":
        if MENU_STATE == "Back":
            Menu_APP = Train_menu(Surface)
        elif MENU_STATE == "Preference":
            Menu_APP = Pref_menu(Surface)
        else:
            Duration = Menu_APP.duration
            Difficulty = Menu_APP.difficulty
    elif Menu_APP.__class__.__name__ == "Init_menu":
        if MENU_STATE == "Back":
            Menu_APP = Train_menu(Surface)
        elif MENU_STATE == "Start":
            Canyon_flight(Surface, Screen_scale)


if __name__ == "__main__":
    # Pygame initialization
    pygame.init()
    pygame.font.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('AEQUUS TRAINING APP')

    # Screen resolution calculation
    infoObject = pygame.display.Info()
    Screen_scale = (infoObject.current_h / H_SIZE)
    Surface = pygame.display.set_mode((int(W_SIZE * Screen_scale), int(H_SIZE * Screen_scale)), pygame.FULLSCREEN)

    # Init training values prefereces
    Difficulty = "Low"
    Duration = 5

    # Init main menu
    Menu_APP = Main_menu(Surface)

    # Timer and clock
    Clock = pygame.time.Clock()
    timer = 0.0
    dt = 1.0 / FPS

    while(True):

        # Tick clock
        Clock.tick(FPS)
        timer += dt

        # Menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                Mouse_x, Mouse_y = pygame.mouse.get_pos()
                select_menu(Mouse_x, Mouse_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
