#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Interactive game for the rehabilitation of patients with multiple sclerosis."""

import os
import pygame
from queue import Queue
from random import choice
from random import gauss
from random import randint
from threading import Thread
import winsound

# Import comands from MPU
from RPI_client import *

# Pygame costant
W_SIZE = 480
H_SIZE = 320
COIN_POINTS = 10
FPS = 60
timer = 0.0
dt = 1.0 / FPS

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREY = (128, 128, 128)
GREY2 = (190, 190, 190)
GREY3 = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (0, 210, 0)
BLUE = (8, 124, 181)
PINK = (225, 140, 131)
YELLOW = (239, 202, 131)
YELLOW2 = (237, 200, 133)
YELLOW3 = (217, 180, 113)
LIGHTBLUE = (144, 205, 202)
LIGHTBLUE2 = (151, 207, 202)
LIGHTGREY = (246, 244, 237)
BROWN = (200, 100, 30)
BROWN2 = (170, 81, 15)
GOLD = (221, 175, 25)
ORANGE = (255, 139, 27)
YELLOW4 = (253, 211, 73)


class HangGlider(object):
    """HangGlider class."""

    def __init__(self, scale):
        """HangGlider class initialization."""
        self.Screen_scale = scale
        self.color1 = ORANGE
        self.color2 = YELLOW4
        self.shade = 27
        self.color1_shade = (ORANGE[0] - self.shade, ORANGE[1] - self.shade, ORANGE[2] - self.shade)
        self.color2_shade = (YELLOW4[0] - self.shade, YELLOW4[1] - self.shade, YELLOW4[2] - self.shade)
        self.height = 50 * self.Screen_scale
        self.base = 100 * self.Screen_scale
        self.size = (self.base, self.height)
        self.offset = 20 * self.Screen_scale
        self.shadow = 20 * self.Screen_scale
        self.pos = [(W_SIZE / 2) * self.Screen_scale, (H_SIZE * self.Screen_scale) - self.height - self.offset]

    def offset_shadow(self):
        """Adds offset to the shadow of the hang glider."""

        point_shadow = []
        for pos in self.pointlist:
            point_shadow.append((pos[0] + self.shadow, pos[1] + self.shadow / 2))
        return point_shadow

    def draw_shadow(self, surface):
        """Draw HangGlider shadow."""
        self.pointlist = (self.pos, (self.pos[0] - self.base / 2, self.pos[1] + self.height), (self.pos[0], self.pos[1] + self.height / 1.5), (self.pos[0] + self.base / 2, self.pos[1] + self.height))
        pygame.draw.polygon(surface, BLACK, self.offset_shadow())

    def draw_glider(self, surface):
        """Draw the HangGlider."""
        self.pointlist0 = (self.pos, (self.pos[0] - self.base / 2, self.pos[1] + self.height), (self.pos[0], self.pos[1] + 1.2 * self.height / 3))
        self.pointlist1 = ((self.pos[0], self.pos[1] + self.height / 3), (self.pos[0] - self.base / 2, self.pos[1] + self.height), (self.pos[0], self.pos[1] + 2 * self.height / 3))
        self.pointlist2 = (self.pos, (self.pos[0] + self.base / 2, self.pos[1] + self.height), (self.pos[0], self.pos[1] + 1.2 * self.height / 3))
        self.pointlist3 = ((self.pos[0], self.pos[1] + self.height / 3), (self.pos[0] + self.base / 2, self.pos[1] + self.height), (self.pos[0], self.pos[1] + 2 * self.height / 3))
        pygame.draw.polygon(surface, self.color2, self.pointlist1)
        pygame.draw.polygon(surface, self.color1, self.pointlist0)
        pygame.draw.polygon(surface, self.color2_shade, self.pointlist3)
        pygame.draw.polygon(surface, self.color1_shade, self.pointlist2)


class GameInfo(object):
    """Class that shows and updates information about the game."""

    def __init__(self, scale):
        """GameInfo initialization."""
        self.Screen_scale = scale
        self.banner_color = LIGHTGREY
        self.banner_size = (100 * self.Screen_scale, 50 * self.Screen_scale)
        self.countdown = 60
        self.score = 0
        self.percent = 100.0
        self.shadow = 20 * self.Screen_scale
        self.warning = False
        self.font = pygame.font.SysFont(name="Terminal", size=round(20 * self.Screen_scale))
        self.font2 = pygame.font.SysFont(name="Terminal", size=round(40 * self.Screen_scale))
        self.punti = self.font.render("Punti:", True, BLACK)
        self.tempo = self.font.render("Tempo:", True, BLACK)

    def draw_clouds(self, surface):
        """ Draw the clouds in background."""
        pygame.draw.circle(surface, BLACK, (round(60 * self.Screen_scale + self.shadow), round(25 * self.Screen_scale + self.shadow / 2)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(20 * self.Screen_scale + self.shadow), round(30 * self.Screen_scale + self.shadow / 2)), round(15 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(40 * self.Screen_scale + self.shadow), round(25 * self.Screen_scale + self.shadow / 2)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(80 * self.Screen_scale + self.shadow), round(35 * self.Screen_scale + self.shadow / 2)), round(15 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(35 * self.Screen_scale + self.shadow), round(40 * self.Screen_scale + self.shadow / 2)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(60 * self.Screen_scale + self.shadow), round(45 * self.Screen_scale + self.shadow / 2)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(W_SIZE * self.Screen_scale - 20 * self.Screen_scale + self.shadow), round(30 * self.Screen_scale + self.shadow / 2)), round(15 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(W_SIZE * self.Screen_scale - 40 * self.Screen_scale + self.shadow), round(25 * self.Screen_scale + self.shadow / 2)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(W_SIZE * self.Screen_scale - 60 * self.Screen_scale + self.shadow), round(25 * self.Screen_scale + self.shadow / 2)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(W_SIZE * self.Screen_scale - 80 * self.Screen_scale + self.shadow), round(35 * self.Screen_scale + self.shadow / 2)), round(15 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(W_SIZE * self.Screen_scale - 35 * self.Screen_scale + self.shadow), round(40 * self.Screen_scale + self.shadow / 2)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(W_SIZE * self.Screen_scale - 60 * self.Screen_scale + self.shadow), round(45 * self.Screen_scale + self.shadow / 2)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(20 * self.Screen_scale), round(30 * self.Screen_scale)), round(15 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(40 * self.Screen_scale), round(25 * self.Screen_scale)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(60 * self.Screen_scale), round(25 * self.Screen_scale)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(80 * self.Screen_scale), round(35 * self.Screen_scale)), round(15 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(35 * self.Screen_scale), round(40 * self.Screen_scale)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(60 * self.Screen_scale), round(45 * self.Screen_scale)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(W_SIZE * self.Screen_scale - 20 * self.Screen_scale), round(30 * self.Screen_scale)), round(15 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(W_SIZE * self.Screen_scale - 40 * self.Screen_scale), round(25 * self.Screen_scale)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(W_SIZE * self.Screen_scale - 60 * self.Screen_scale), round(25 * self.Screen_scale)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(W_SIZE * self.Screen_scale - 80 * self.Screen_scale), round(35 * self.Screen_scale)), round(15 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(W_SIZE * self.Screen_scale - 35 * self.Screen_scale), round(40 * self.Screen_scale)), round(20 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(W_SIZE * self.Screen_scale - 60 * self.Screen_scale), round(45 * self.Screen_scale)), round(20 * self.Screen_scale))

    def draw_info(self, surface, count):
        """Draw game info on the screen."""
        self.draw_clouds(surface)
        if self.countdown > dt:
            self.countdown -= dt
        else:
            self.countdown = 0
        if count != 0:
            self.percent = round(((self.score / COIN_POINTS) / count) * 100, 2)
        surface.blit(self.punti, (31 * self.Screen_scale, 15 * self.Screen_scale))
        surface.blit(self.tempo, ((W_SIZE - 72) * self.Screen_scale, 15 * self.Screen_scale))
        self.score_txt = self.font2.render(str(self.score), True, BLACK)
        self.timer_txt = self.font2.render(str(round(self.countdown)), True, BLACK)
        if self.score // 10 == 0:
            surface.blit(self.score_txt, (43 * self.Screen_scale, 30 * self.Screen_scale))
        elif self.score // 10 >= 1 and self.score // 100 == 0:
            surface.blit(self.score_txt, (35 * self.Screen_scale, 30 * self.Screen_scale))
        elif self.score // 100 >= 1:
            surface.blit(self.score_txt, (27 * self.Screen_scale, 30 * self.Screen_scale))
        if self.countdown // 10 == 0:
            surface.blit(self.timer_txt, ((W_SIZE - 56) * self.Screen_scale, 30 * self.Screen_scale))
        elif self.countdown // 1 >= 1 and self.countdown // 100 == 0:
            surface.blit(self.timer_txt, ((W_SIZE - 64) * self.Screen_scale, 30 * self.Screen_scale))
        elif self.countdown // 100 >= 0:
            surface.blit(self.timer_txt, ((W_SIZE - 71) * self.Screen_scale, 30 * self.Screen_scale))

    def draw_endgame(self, surface):
        """Draw the end game imgage."""
        pygame.draw.circle(surface, BLACK, (round(W_SIZE / 2 * self.Screen_scale + self.shadow), round(H_SIZE / 2 * self.Screen_scale + self.shadow / 2)), round(90 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(W_SIZE / 4 * self.Screen_scale + self.shadow), round(H_SIZE / 2 * self.Screen_scale + self.shadow / 2)), round(50 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(3 * W_SIZE / 4 * self.Screen_scale + self.shadow), round(H_SIZE / 2 * self.Screen_scale + self.shadow / 2)), round(50 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(1.5 * W_SIZE / 4 * self.Screen_scale + self.shadow), round(H_SIZE / 2 * self.Screen_scale + self.shadow / 2 - 20 * self.Screen_scale)), round(60 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(1.5 * W_SIZE / 4 * self.Screen_scale + self.shadow), round(H_SIZE / 2 * self.Screen_scale + self.shadow / 2 + 20 * self.Screen_scale)), round(60 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(2.5 * W_SIZE / 4 * self.Screen_scale + self.shadow), round(H_SIZE / 2 * self.Screen_scale + self.shadow / 2 - 20 * self.Screen_scale)), round(60 * self.Screen_scale))
        pygame.draw.circle(surface, BLACK, (round(2.5 * W_SIZE / 4 * self.Screen_scale + self.shadow), round(H_SIZE / 2 * self.Screen_scale + self.shadow / 2 + 20 * self.Screen_scale)), round(60 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(W_SIZE / 2 * self.Screen_scale), round(H_SIZE / 2 * self.Screen_scale)), round(90 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(W_SIZE / 4 * self.Screen_scale), round(H_SIZE / 2 * self.Screen_scale)), round(50 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(3 * W_SIZE / 4 * self.Screen_scale), round(H_SIZE / 2 * self.Screen_scale)), round(50 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(1.5 * W_SIZE / 4 * self.Screen_scale), round(H_SIZE / 2 * self.Screen_scale - 20 * self.Screen_scale)), round(60 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(1.5 * W_SIZE / 4 * self.Screen_scale), round(H_SIZE / 2 * self.Screen_scale + 20 * self.Screen_scale)), round(60 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(2.5 * W_SIZE / 4 * self.Screen_scale), round(H_SIZE / 2 * self.Screen_scale - 20 * self.Screen_scale)), round(60 * self.Screen_scale))
        pygame.draw.circle(surface, self.banner_color, (round(2.5 * W_SIZE / 4 * self.Screen_scale), round(H_SIZE / 2 * self.Screen_scale + 20 * self.Screen_scale)), round(60 * self.Screen_scale))
        self.font1 = pygame.font.SysFont(name="Terminal", size=round(50 * self.Screen_scale))
        self.font2 = pygame.font.SysFont(name="Terminal", size=round(30 * self.Screen_scale))
        self.congrats = self.font1.render("Congratulazioni!", True, RED)
        self.punteggio = self.font2.render("Punteggio: " + str(self.score), True, GREY)
        self.precisione = self.font2.render("Precisione: " + str(self.percent) + "%", True, GREY)
        surface.blit(self.congrats, (105 * self.Screen_scale, 125 * self.Screen_scale))
        surface.blit(self.punteggio, (150 * self.Screen_scale, 170 * self.Screen_scale))
        surface.blit(self.precisione, (150 * self.Screen_scale, 200 * self.Screen_scale))
        pygame.display.flip()


class GroupCoins(object):
    """Class that defines the number of coins on the screen and defines the methods for eliminating and creating them."""

    def __init__(self, num, scale):
        """GroupCoins class initialization."""
        self.Screen_scale = scale
        self.num = num
        self.dist = 150 * self.Screen_scale
        self.size = (30 * self.Screen_scale, 30 * self.Screen_scale)
        self.edge = 50 * self.Screen_scale
        self.std_dev = 30
        self.group = {}
        self.anim = 0
        self.timer = 0
        self.count = 0
        self.last_obs = ""
        self.flag = True
        self.coin0 = pygame.image.load("images/coin0.png")
        self.coin1 = pygame.image.load("images/coin1.png")
        self.coin2 = pygame.image.load("images/coin2.png")
        self.coin3 = pygame.image.load("images/coin3.png")
        self.coin4 = pygame.image.load("images/coin4.png")
        self.coin5 = pygame.image.load("images/coin5.png")
        self.coin0 = pygame.transform.scale(self.coin0, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.coin1 = pygame.transform.scale(self.coin1, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.coin2 = pygame.transform.scale(self.coin2, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.coin3 = pygame.transform.scale(self.coin3, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.coin4 = pygame.transform.scale(self.coin4, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.coin5 = pygame.transform.scale(self.coin5, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.init_coins()

    def init_coins(self):
        """Given a number of items, initialize the dictionary by creating coins."""
        for x in range(0, self.num):
            pos = (self.inv_gauss(), int((0 - 1) * x * self.dist - self.size[1]))
            self.group["coin{0}".format(x)] = Coin(pos, self.size, self.Screen_scale)

    def create_coin(self):
        """Method that creates new coins in the dictionary."""
        x = 0
        name = "coin{0}".format(x)
        while(name in self.group.keys()):
            x += 1
            name = "coin{0}".format(x)
        min_y = H_SIZE * self.Screen_scale
        for obs in self.group.keys():
            if self.group[obs].pos[1] < min_y:
                min_y = self.group[obs].pos[1]
        pos = (self.inv_gauss(), int(min_y - self.dist - self.size[1]))
        self.group[name] = Coin(pos, self.size, self.Screen_scale)

    def remove_coin(self, obs_key):
        """Remove a coin from dictionary given a key."""
        self.group.pop(obs_key)

    def check_if_out(self):
        """Method that checks which coins came out of the screen and deletes them from the dictionary."""
        remove_list = []
        for obs in self.group.keys():
            if self.group[obs].pos[1] > H_SIZE * self.Screen_scale:
                remove_list.append(obs)
        for i in range(0, len(remove_list)):
            self.remove_coin(remove_list[i])

    def check_if_taken(self, glider_pos, glider_size):
        """Method that checks if the coin has been taken."""
        remove_list = []
        for obs in self.group.keys():
            self.coin_count(obs, glider_pos, glider_size)
            if self.group[obs].pos[1] > glider_pos[1] and self.group[obs].pos[1] < glider_pos[1] + glider_size[1]:
                if self.group[obs].pos[0] > glider_pos[0] - glider_size[0] / 2 and self.group[obs].pos[0] < glider_pos[0] + glider_size[0] / 2:
                    remove_list.append(obs)
        for i in range(0, len(remove_list)):
            self.remove_coin(remove_list[i])
        return len(remove_list) * COIN_POINTS

    def coin_count(self, obs, pos, size):
        """Metodo che conta tutte le monete che passano dalla posizione y del deltaplano."""
        if self.group[obs].pos[1] > pos[1] and self.group[obs].pos[1] < pos[1] + size[1]:
            if obs != self.last_obs:
                self.last_obs = obs
                self.count += 1

    def check_number(self):
        """Method that counts all the coins passing through the y position of the hang glider."""
        if len(self.group) < self.num:
            missing_num = self.num - len(self.group)
            for i in range(0, missing_num):
                self.create_coin()

    def inv_gauss(self):
        """Method that returns an inverse probability bell to generate game elements."""
        mean_offset = 30 * self.Screen_scale
        mean_sx = self.edge + ((W_SIZE * self.Screen_scale) / 2 - self.edge) / 2 - mean_offset
        mean_dx = (W_SIZE * self.Screen_scale) / 2 + ((W_SIZE * self.Screen_scale) / 2 - self.edge) / 2 + mean_offset - self.size[0]
        if randint(0, 1) == 0:
            val = gauss(mean_sx, self.std_dev)
            while(val < self.edge and val > W_SIZE * self.Screen_scale / 2):
                val = gauss(mean_sx, self.std_dev)
            return round(val)
        else:
            val = gauss(mean_dx, self.std_dev)
            while(val < W_SIZE * self.Screen_scale / 2 and val > W_SIZE * self.Screen_scale - self.edge):
                val = gauss(mean_dx, self.std_dev)
            return round(val)

    def animate_coin(self):
        """Return the image of the animation to draw."""
        if int(self.timer * FPS % 10) == 0 and self.flag is True:
            if self.anim == 5:
                self.anim = 0
            else:
                self.anim += 1
            self.flag = False
        elif int(self.timer * FPS % 10) == 1:
            self.flag = True
        if self.anim == 0:
            coin = self.coin0
        elif self.anim == 1:
            coin = self.coin1
        elif self.anim == 2:
            coin = self.coin2
        elif self.anim == 3:
            coin = self.coin3
        elif self.anim == 4:
            coin = self.coin4
        elif self.anim == 5:
            coin = self.coin5
        return coin

    def draw_coins(self, surface):
        """Draw coin in the dictionary."""
        self.timer += dt
        for obs in self.group.keys():
            self.group[obs].draw_coin(surface, self.animate_coin())


class Background(object):
    """Class of the background elements of the game."""

    def __init__(self, num, scale):
        """Background class initialization."""
        self.Screen_scale = scale
        self.vel = 50 * self.Screen_scale
        self.edge = 50 * self.Screen_scale
        self.dist = 180 * self.Screen_scale
        self.dist_isle = 400 * self.Screen_scale
        self.isle = {}
        self.elements_sx = {}
        self.elements_dx = {}
        self.num_ele = 6
        self.num_isle = 2
        self.bush1 = pygame.image.load("images/bush1.png")
        self.bush1 = pygame.transform.scale(self.bush1, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.bush2 = pygame.image.load("images/bush2.png")
        self.bush2 = pygame.transform.scale(self.bush2, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.cactus = pygame.image.load("images/cactus.png")
        self.cactus = pygame.transform.scale(self.cactus, (round(30 * self.Screen_scale), round(55 * self.Screen_scale)))
        self.landslide = pygame.image.load("images/landslide.png")
        self.landslide = pygame.transform.scale(self.landslide, (round(30 * self.Screen_scale), round(30 * self.Screen_scale)))
        self.img_list = {"bush1": self.bush1, "bush2": self.bush2, "cactus": self.cactus, "landslide": self.landslide}
        self.create_elements_sx()
        self.create_elements_dx()
        self.create_islands()

    def create_elements_sx(self):
        """Create an instace of the class Background_img."""
        create_num = self.num_ele - len(self.elements_sx)
        for i in range(0, create_num):
            rnd_element = choice([*self.img_list])
            x = 0
            name = rnd_element + "{0}".format(x)
            while(name in self.elements_sx.keys()):
                x += 1
                name = rnd_element + "{0}".format(x)
            min_y = H_SIZE * self.Screen_scale + self.dist / 2
            for obs in self.elements_sx.keys():
                if self.elements_sx[obs].pos[1] < min_y:
                    min_y = self.elements_sx[obs].pos[1]
            self.elements_sx[name] = BackgroundImg(rnd_element, self.img_list[rnd_element], (5 * self.Screen_scale, min_y - self.dist), self.Screen_scale)

    def create_elements_dx(self):
        """Create an instace of the class Background_img."""
        create_num = self.num_ele - len(self.elements_dx)
        for i in range(0, create_num):
            rnd_element = choice([*self.img_list])
            x = 0
            name = rnd_element + "{0}".format(x)
            while(name in self.elements_dx.keys()):
                x += 1
                name = rnd_element + "{0}".format(x)
            min_y = H_SIZE * self.Screen_scale
            for obs in self.elements_dx.keys():
                if self.elements_dx[obs].pos[1] < min_y:
                    min_y = self.elements_dx[obs].pos[1]
            self.elements_dx[name] = BackgroundImg(rnd_element, self.img_list[rnd_element], (445 * self.Screen_scale, min_y - self.dist), self.Screen_scale)

    def create_islands(self):
        """Generates randomly sand island on the river."""
        create_num = self.num_isle - len(self.isle)
        for i in range(0, create_num):
            side = randint(0, 1)
            x = 0
            name = "Isle{0}".format(x)
            while(name in self.isle.keys()):
                x += 1
                name = "Isle{0}".format(x)
            min_y = H_SIZE * self.Screen_scale
            for obs in self.isle.keys():
                if self.isle[obs].pos[1] < min_y:
                    min_y = self.isle[obs].pos[1]
            if side == 0:
                self.isle[name] = Sand_Island((20 * self.Screen_scale, min_y - self.dist_isle), side, self.Screen_scale)
            elif side == 1:
                self.isle[name] = Sand_Island((400 * self.Screen_scale, min_y - self.dist_isle), side, self.Screen_scale)

    def remove_island(self, obj):
        """Remove islands of sand in the dictionary."""
        self.isle.pop(obj)

    def remove_element(self, obj, side):
        """Remove game's element in the dictionary."""
        if side == "sx":
            self.elements_sx.pop(obj)
        elif side == "dx":
            self.elements_dx.pop(obj)

    def check_if_out(self):
        """Method that controls which background elements left the screen and deletes them from the dictionary."""
        remove_list_sx = []
        remove_list_dx = []
        remove_list_isle = []
        for obs in self.elements_sx.keys():
            if self.elements_sx[obs].pos[1] > H_SIZE * self.Screen_scale:
                remove_list_sx.append(obs)
        for obs in self.elements_dx.keys():
            if self.elements_dx[obs].pos[1] > H_SIZE * self.Screen_scale:
                remove_list_dx.append(obs)
        for obs in self.isle.keys():
            if self.isle[obs].pos[1] > H_SIZE * self.Screen_scale + 90 * self.Screen_scale:
                remove_list_isle.append(obs)
        for i in range(0, len(remove_list_sx)):
            self.remove_element(remove_list_sx[i], side="sx")
        for i in range(0, len(remove_list_dx)):
            self.remove_element(remove_list_dx[i], side="dx")
        for i in range(0, len(remove_list_isle)):
            self.remove_island(remove_list_isle[i])

    def check_number(self):
        """Method that controls the number of background elements in play and procedurally creates them."""
        create_num_sx = self.num_ele - len(self.elements_sx)
        create_num_dx = self.num_ele - len(self.elements_dx)
        create_num_isle = self.num_isle - len(self.isle)
        if create_num_sx > 0:
            self.create_elements_sx()
        if create_num_dx > 0:
            self.create_elements_dx()
        if create_num_isle > 0:
            self.create_islands()

    def draw_elements(self, surface):
        """Draw all the background elements of the dictionary."""
        for obj in self.elements_sx.keys():
            self.elements_sx[obj].draw_image(surface)
        for obj in self.elements_dx.keys():
            self.elements_dx[obj].draw_image(surface)

    def draw_islands(self, surface):
        """Draw sand island inside the dictionary."""
        for obj in self.isle.keys():
            self.isle[obj].draw_island(surface)

    def draw_background(self, surface):
        """Draw all elements in the background."""
        surface.fill(LIGHTBLUE2)
        self.draw_islands(surface)
        pygame.draw.rect(surface, BROWN, (0, 0, self.edge, H_SIZE * self.Screen_scale))
        pygame.draw.rect(surface, BROWN2, (self.edge - 10 * self.Screen_scale, 0, 10 * self.Screen_scale, H_SIZE * self.Screen_scale))
        pygame.draw.rect(surface, BROWN, (W_SIZE * self.Screen_scale - self.edge, 0, self.edge, H_SIZE * self.Screen_scale))
        pygame.draw.rect(surface, BROWN2, (W_SIZE * self.Screen_scale - self.edge, 0, 10 * self.Screen_scale, H_SIZE * self.Screen_scale))
        self.draw_elements(surface)


class Coin(object):
    """Coin class."""

    def __init__(self, pos, size, scale):
        """Coin initialization class."""
        self.Screen_scale = scale
        self.width = size[0]
        self.height = size[1]
        self.time = 0
        self.init_pos = pos
        self.vel = 50 * self.Screen_scale

    def draw_coin(self, surface, coin):
        """Draw the coin."""
        self.time += dt
        self.pos = (self.init_pos[0], self.init_pos[1] + self.vel * self.time)
        surface.blit(coin, (self.pos[0], self.pos[1], self.width, self.height))


class BackgroundImg(object):
    """Background images class."""

    def __init__(self, name, img, pos, scale):
        """Background images class initialization."""
        self.Screen_scale = scale
        self.name = name
        self.img = img
        self.time = 0
        self.vel = 50 * self.Screen_scale
        self.init_pos = pos
        self.pos = (self.init_pos[0], self.init_pos[1] + self.vel * self.time)

    def draw_image(self, surface):
        """Draw the background image."""
        self.time += dt
        self.pos = (self.init_pos[0], self.init_pos[1] + self.vel * self.time)
        surface.blit(self.img, self.pos)


class Sand_Island(object):
    """Sand_Island class."""

    def __init__(self, pos, side, scale):
        """Sand_Island class initialization"""
        self.Screen_scale = scale
        self.init_pos = pos
        self.color = YELLOW
        self.side = side
        self.size = (60 * self.Screen_scale, 120 * self.Screen_scale)
        self.time = 0
        self.vel = 50 * self.Screen_scale
        self.pos = (self.init_pos[0], self.init_pos[1] + self.vel * self.time)

    def draw_island(self, surface):
        """Draw sand island."""
        self.time += dt
        self.pos = (self.init_pos[0], self.init_pos[1] + self.vel * self.time)
        if self.side == 0:
            pygame.draw.ellipse(surface, self.color, (self.pos[0], self.pos[1] - 50 * self.Screen_scale, self.size[0] / 0.9, self.size[1]))
        elif self.side == 1:
            pygame.draw.ellipse(surface, self.color, (self.pos[0] + 5 * self.Screen_scale, self.pos[1] - 50 * self.Screen_scale, self.size[0] * 2, self.size[1]))
            pygame.draw.ellipse(surface, self.color, (self.pos[0], self.pos[1] - 100 * self.Screen_scale, self.size[0] * 2, self.size[1]))
        pygame.draw.ellipse(surface, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))


def Buzzer_flag(glider, edge, scale):
    """Activates the acoustic notification when the user reaches the limit areas of the screen."""
    if glider.pos[0] + glider.base / 2 > W_SIZE * scale - edge or glider.pos[0] - glider.base / 2 < edge:
        return True
    else:
        return False


def Buzzer_beep(freq, dur):
    """Function that plays beep sound of the system."""
    while(True):
        winsound.Beep(freq, dur)


def Canyon_flight(Surface, scale):
    """Aequus minigame app: Canyon flight."""
    # Load game music
    dir_beep = "Music/beep.mp3"
    pygame.mixer.music.load(dir_beep)
    pygame.mixer.music.set_volume(1.0)

    # Mux initialization
    mux = MultiplexCommands()

    # MPU6050 initialization
    quat_queue = Queue(maxsize=1)
    quat_queue.put(False)
    mux.switch_channel(4)
    mpu4 = MPUCommands("mpu4")
    drift = mpu4.drift

    # Multithreading reading of MPU6050 data
    readThread = Thread(name="read_data", target=mpu4.read_value, args=[quat_queue])
    readThread.start()

    # Sensor calibration
    gravity = mpu4.read_gravity()
    tmp = quat_queue.get()
    quat_queue.put(tmp)
    rel_quat = Quaternion(tmp)
    abs_quat = orientate_quat(rel_quat, gravity)
    ref_pos = Quaternion(scalar=None, vector=abs_quat.axis)
    old_pos = convert_pos(ref_pos.x, scale)

    # CLass initialization
    background = Background(num=4, scale=scale)
    coins = GroupCoins(num=4, scale=scale)
    glider = HangGlider(scale=scale)
    gameinfo = GameInfo(scale=scale)

    # Flag buzz initialization
    buzz_flag = False

    # Pygame variables initialization
    Clock = pygame.time.Clock()
    timer = 0.0
    while(True):

        # TICK CLOCK
        Clock.tick(FPS)
        timer += dt

        # reading from sensors
        try:
            # read value from queue
            tmp = quat_queue.get()
            quat_queue.put(tmp)
            rel_quat = Quaternion(tmp)
            abs_quat = orientate_quat(rel_quat, gravity)
            abs_quat = fix_drifting(abs_quat, drift, dt)
            new_pos = abs_quat.rotate(ref_pos)
        except Exception as e:
            print(e)
            continue

        real_pos = convert_pos(-new_pos.x, scale)

        follow_position(real_pos, glider, scale)
        old_pos = real_pos

        # Main commands
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        pressed_keys = pygame.key.get_pressed()

        # Debug commands
        if pressed_keys[pygame.K_LEFT]:
            tmp = glider.pos[0] - 10 * scale
            if tmp - glider.base / 2 >= 0 * scale:
                glider.pos[0] = tmp

        if pressed_keys[pygame.K_RIGHT]:
            tmp = glider.pos[0] + 10 * scale
            if tmp + glider.base / 2 <= W_SIZE * scale:
                glider.pos[0] = tmp

        if gameinfo.countdown != 0:
            background.draw_background(Surface)
            glider.draw_shadow(Surface)
            coins.draw_coins(Surface)
            glider.draw_glider(Surface)
            gameinfo.draw_info(Surface, coins.count)
            coins.check_if_out()
            gameinfo.score += coins.check_if_taken(glider.pos, glider.size)
            coins.check_number()
            background.check_if_out()
            background.check_number()
            # if buzz_flag is False:
            if(Buzzer_flag(glider, background.edge, scale)):
                # pygame.mixer.music.play()

                winsound.Beep(432 * 4, 1)
            '''
            else:
                buzz_flag = Buzzer_flag(glider, background.edge, scale)
                if buzz_flag is True:
            '''
            # pygame.mixer.music.stop()

        elif gameinfo.countdown == 0:
            gameinfo.draw_endgame(Surface)

        # Update display
        pygame.display.flip()


if __name__ == "__main__":

    # Pygame initialization
    pygame.init()
    pygame.font.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('AEQUUS TRAINING APP')

    # Calculate screen resolition
    pygame.init()
    infoObject = pygame.display.Info()
    Screen_scale = (infoObject.current_h / H_SIZE) * 0.7

    # Create pygame display
    Surface = pygame.display.set_mode((round(W_SIZE * Screen_scale), round(H_SIZE * Screen_scale)))

    # Start the Caynon flight minigame
    Canyon_flight(Surface, Screen_scale)
