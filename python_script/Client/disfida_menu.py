#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Application and graphic interface of Aequus trainig app."""


from math import sqrt
import os
import pygame

from HangGlider_game import *


# Pygame constants
W_SIZE = 480            # Width in pixel
H_SIZE = 320            # Height in pixel
FPS = 60                # Frame per second

# Screen resolution calculation
pygame.init()
infoObject = pygame.display.Info()
Screen_scale = (infoObject.current_h / H_SIZE) * 0.7

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREY = (128, 128, 128)
GREY2 = (190, 190, 190)
GREY3 = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (8, 124, 181)
PINK = (225, 140, 131)
YELLOW = (239, 202, 131)
YELLOW2 = (237, 200, 133)
YELLOW3 = (237 - 20, 200 - 20, 133 - 20)
LIGHTBLUE = (144, 205, 202)
LIGHTBLUE2 = (151, 207, 202)
LIGHTGREY = (246, 244, 237)


class Main_menu(object):
    """Classes of main menu."""

    def __init__(self, surface):
        """Init Main_menu."""
        self.surface = surface
        self.surface.fill(GREY)
        self.shift = 50
        self.pointlist = self.get_point(10, 3, self.shift)
        self.font = pygame.font.SysFont(name="Terminal", size=round(60 * (Screen_scale)))
        pygame.draw.polygon(self.surface, BLACK, self.pointlist[3])
        pygame.draw.polygon(self.surface, BLACK, self.pointlist[4])
        pygame.draw.polygon(self.surface, BLACK, self.pointlist[5])
        pygame.draw.polygon(self.surface, LIGHTBLUE, self.pointlist[0])
        pygame.draw.polygon(self.surface, LIGHTBLUE, self.pointlist[6])
        pygame.draw.polygon(self.surface, YELLOW, self.pointlist[1])
        pygame.draw.polygon(self.surface, LIGHTGREY, self.pointlist[2])
        Text_all = self.font.render("Training", True, BLACK)
        Text_pro = self.font.render("Progress", True, BLACK)
        Text_opz = self.font.render("Options", True, BLACK)
        surface.blit(Text_all, self.pointlist[7][0])
        surface.blit(Text_pro, self.pointlist[8][0])
        surface.blit(Text_opz, self.pointlist[9][0])
        pygame.display.flip()

    def get_point(self, space, shade, shift):
        """Obtains the points to draw the interface"""

        m = H_SIZE / W_SIZE
        offset = (2 / W_SIZE) * (space) * (sqrt((H_SIZE**2 / 4) + (W_SIZE**2 / 4)))
        y = m * ((W_SIZE / 2) - (space / 2)) + offset
        x1 = (W_SIZE / 2) - (space / 2)
        x2 = (W_SIZE / 2) + (space / 2)
        list0 = [[0, shift], [W_SIZE, shift], [W_SIZE / 2, H_SIZE / 2 + shift]]
        list1 = [[0, offset + shift], [x1, y + shift], [x1, H_SIZE + shift], [0, H_SIZE + shift]]
        list2 = [[W_SIZE, offset + shift], [x2, y + shift], [x2, H_SIZE + shift], [W_SIZE, H_SIZE + shift]]
        list3 = [[shade, shade + shift], [W_SIZE + shade, shade + shift], [W_SIZE / 2 + shade, H_SIZE / 2 + shade + shift]]
        list4 = [[shade, offset + shade + shift], [x1 + shade, y + shade + shift], [x1 + shade, H_SIZE + shade + shift], [shade, H_SIZE + shade + shift]]
        list5 = [[W_SIZE + shade, offset + shade + shift], [x2 + shade, y + shade + shift], [x2 + shade, H_SIZE + shade + shift], [W_SIZE + shade, H_SIZE + shade + shift]]
        list6 = [[0, 0], [0, self.shift], [W_SIZE, self.shift], [W_SIZE, 0]]
        list7 = [[108, 45 + self.shift / 2]]
        list8 = [[20, 210 + self.shift / 2]]
        list9 = [[282, 210 + self.shift / 2]]
        list = [list0, list1, list2, list3, list4, list5, list6, list7, list8, list9]
        list = self.scale_point(list, Screen_scale)
        return list

    def scale_point(self, list, scale):
        """Scale the points of the lists."""

        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                list[i][j][0] *= scale
                list[i][j][1] *= scale
        return list

    def controls(self, posx, posy):
        """Controls of main menu."""
        if self.check_training(posx, posy):
            print("Training")
            return "Training"
        if self.check_progress(posx, posy):
            print("Progress")
            return "Progress"
        if self.check_options(posx, posy):
            print("Options")
            return "Options"

    def check_training(self, posx, posy):
        """Check if the cursor is over the Trainig button."""
        m = (self.pointlist[0][2][1] - self.pointlist[0][0][1]) / (self.pointlist[0][2][0])
        q = self.pointlist[0][0][1]
        if posy < q:
            return True
        else:
            if posx < self.pointlist[0][2][0]:
                if posy < m * posx + q:
                    return True
                else:
                    return False
            else:
                if posy < (0 - m) * (posx - self.pointlist[0][2][0]) + self.pointlist[0][2][1]:
                    return True
                else:
                    return False

    def check_progress(self, posx, posy):
        """Check if the cursor is over the Progess button."""

        m = (self.pointlist[0][2][1] - self.pointlist[0][0][1]) / (self.pointlist[0][2][0])
        q = self.pointlist[1][0][1]
        if posy > self.pointlist[1][1][1]:
            if posx > self.pointlist[1][0][0] and posx < self.pointlist[1][1][0]:
                return True
            else:
                return False
        else:
            if posx > self.pointlist[1][0][0] and posx < self.pointlist[1][1][0]:
                if posy > m * posx + q:
                    return True
                else:
                    return False

    def check_options(self, posx, posy):
        """Check if the cursor is over the Options button."""

        m = (self.pointlist[0][2][1] - self.pointlist[0][0][1]) / (self.pointlist[0][2][0])
        q = self.pointlist[2][1][1]
        if posy > self.pointlist[2][1][1]:
            if posx > self.pointlist[2][1][0] and posx < self.pointlist[2][0][0]:
                return True
            else:
                return False
        else:
            if posx > self.pointlist[2][1][0] and posx < self.pointlist[2][0][0]:
                if posy > (0 - m) * (posx - self.pointlist[2][1][0]) + q:
                    return True
                else:
                    return False


class Train_menu(object):
    """Class of the Training menu."""

    def __init__(self, surface):
        """initialization of Train_menu class."""
        surface.fill(GREY)
        self.pointlist = self.get_point(12, 3)
        self.home = pygame.image.load("images/home.png")
        self.home = pygame.transform.scale(self.home, (round(62 * Screen_scale), round(53 * Screen_scale)))
        self.font1 = pygame.font.SysFont(name="Terminal", size=round(60 * Screen_scale))
        self.font2 = pygame.font.SysFont(name="Terminal", size=round(100 * Screen_scale))
        pygame.draw.polygon(surface, BLACK, self.pointlist[3])
        pygame.draw.polygon(surface, BLACK, self.pointlist[4])
        pygame.draw.polygon(surface, BLACK, self.pointlist[5])
        pygame.draw.polygon(surface, PINK, self.pointlist[0])
        pygame.draw.polygon(surface, LIGHTBLUE, self.pointlist[1])
        pygame.draw.polygon(surface, LIGHTGREY, self.pointlist[2])
        Text_pre = self.font1.render("Preference", True, BLACK)
        Text_ini = self.font2.render("Start", True, BLACK)
        surface.blit(Text_pre, self.pointlist[6][0])
        surface.blit(Text_ini, self.pointlist[7][0])
        surface.blit(self.home, self.pointlist[8][0])
        pygame.display.flip()

    def get_point(self, space, shade):
        """Obtains the points to draw the interface."""
        m1 = H_SIZE / W_SIZE
        q1 = H_SIZE
        q2 = H_SIZE + space
        y1 = (0 - m1) * W_SIZE + q1
        y2 = (0 - m1) * W_SIZE + q2
        y3 = (0 - m1) * 130 + q1
        m2 = ((y3 - 50) / 130)
        x4 = (q1 - 30) / (m1 + m2)
        y4 = m2 * x4 + 30
        list0 = [[0, 0], [0, 30], [x4, y4], [W_SIZE, y1]]
        list1 = [[W_SIZE, H_SIZE + space], [W_SIZE, y2], [0, H_SIZE + space]]
        list2 = [[0, 50], [130, y3], [0, H_SIZE]]
        list3 = [[shade, shade], [shade, 30 + shade], [x4 + shade, y4 + shade], [W_SIZE + shade, y1 + shade]]
        list4 = [[W_SIZE + shade, H_SIZE + space + shade], [W_SIZE + shade, y2 + shade], [shade, H_SIZE + space + shade]]
        list5 = [[shade, 50 + shade], [130 + shade, y3 + shade], [shade, H_SIZE + shade]]
        list6 = [[75, 70]]
        list7 = [[250, 210]]
        list8 = [[22, 180]]
        list = [list0, list1, list2, list3, list4, list5, list6, list7, list8]
        list = self.scale_point(list, Screen_scale)
        return list

    def scale_point(self, list, scale):
        """Scale the points of the lists."""
        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                list[i][j][0] *= scale
                list[i][j][1] *= scale
        return list

    def controls(self, posx, posy):
        """Controls of the training menu."""
        if self.check_preference(posx, posy):
            print("Preference")
            return "Preference"
        if self.check_inizio(posx, posy):
            print("Start")
            return "Start"
        if self.check_home(posx, posy):
            print("Home")
            return "Home"

    def check_preference(self, posx, posy):
        """Check if the cursor is over the Difficulty button."""

        m1 = self.pointlist[2][2][1] / self.pointlist[1][0][0]
        q1 = self.pointlist[2][2][1]
        q2 = self.pointlist[0][1][1]
        m2 = (self.pointlist[0][2][1] - q2) / (self.pointlist[0][2][0])
        if posx > self.pointlist[0][2][0]:
            if posy < (0 - m1) * posx + q1:
                return True
            else:
                return False
        else:
            if posy < self.pointlist[0][1][1]:
                return True
            else:
                if posy < m2 * posx + q2:
                    return True
                else:
                    return False

    def check_inizio(self, posx, posy):
        """Check if the cursor is over the Duration button."""
        q = self.pointlist[1][2][1]
        m = self.pointlist[2][2][1] / self.pointlist[1][0][0]
        if posy > (0 - m) * posx + q:
            return True
        else:
            return False

    def check_home(self, posx, posy):
        """Check if the cursor is over the Home button."""
        m1 = self.pointlist[2][2][1] / self.pointlist[1][0][0]
        q1 = self.pointlist[2][2][1]
        y3 = (0 - m1) * self.pointlist[2][1][0] + q1
        m = ((y3 - self.pointlist[2][0][1]) / self.pointlist[2][1][0])
        q2 = self.pointlist[2][0][1]
        if posy < self.pointlist[2][1][1]:
            if posy > m * posx + q2 and posx < self.pointlist[2][1][0] and posx > 0:
                return True
            else:
                return False
        else:
            if posy < (0 - m1) * posx + q1 and posx < self.pointlist[2][1][0] and posx > 0:
                return True
            else:
                return False


class Pref_menu(object):
    """Classes of the preference menu."""

    def __init__(self, surface, dur, diff):
        """Init Pref_menu class."""
        self.surface = surface
        self.duration = dur
        self.difficulty = diff
        surface.fill(GREY)
        self.pointlist = self.get_point()
        self.back = pygame.image.load("images/back.png")
        self.back = pygame.transform.scale(self.back, (round(60 * Screen_scale), round(60 * Screen_scale)))
        self.font1 = pygame.font.SysFont(name="Terminal", size=round(60 * Screen_scale))
        self.font2 = pygame.font.SysFont(name="Terminal", size=round(60 * Screen_scale))
        self.font3 = pygame.font.SysFont(name="Terminal", size=round(150 * Screen_scale))
        pygame.draw.rect(self.surface, YELLOW2, self.pointlist[0], 0)
        pygame.draw.rect(self.surface, LIGHTBLUE2, self.pointlist[1], 0)
        self.Text_diff2 = self.font2.render("Difficulty", True, GREY)
        self.Text_dur2 = self.font2.render("Duration", True, GREY)
        self.Text_diff = self.font2.render("Difficulty", True, WHITE)
        self.Text_dur = self.font2.render("Duration", True, WHITE)
        self.Text_alta = self.font1.render("High", True, BLACK)
        self.Text_media = self.font1.render("Medium", True, BLACK)
        self.Text_bassa = self.font1.render("Low", True, BLACK)
        self.surface.blit(self.Text_dur2, self.pointlist[2][0])
        self.surface.blit(self.Text_diff2, self.pointlist[3][0])
        self.surface.blit(self.Text_dur, self.pointlist[4][0])
        self.surface.blit(self.Text_diff, self.pointlist[5][0])
        # Difficulty
        self.diff_selection()
        # Counter
        pygame.draw.rect(self.surface, WHITE, self.pointlist[6], 0)
        pygame.draw.rect(self.surface, GREY, self.pointlist[7], round(1 * Screen_scale))
        # Buttons
        pygame.draw.rect(self.surface, BLACK, self.pointlist[8], 0)
        pygame.draw.rect(self.surface, BLACK, self.pointlist[9], 0)
        pygame.draw.rect(self.surface, GREY2, self.pointlist[10], 0)
        pygame.draw.rect(self.surface, GREY2, self.pointlist[11], 0)
        # Back
        pygame.draw.rect(self.surface, WHITE, self.pointlist[12], 0)
        pygame.draw.polygon(self.surface, YELLOW3, self.pointlist[13])
        pygame.draw.aaline(self.surface, YELLOW3, self.pointlist[14][0], self.pointlist[14][1])
        self.surface.blit(self.back, self.pointlist[15][0])
        pygame.draw.rect(self.surface, BLACK, self.pointlist[16], 0)
        pygame.draw.rect(self.surface, BLACK, self.pointlist[17], 0)
        pygame.draw.rect(self.surface, BLACK, self.pointlist[18], 0)
        pygame.draw.rect(self.surface, WHITE, self.pointlist[19], 0)
        pygame.draw.rect(self.surface, WHITE, self.pointlist[20], 0)
        pygame.draw.rect(self.surface, WHITE, self.pointlist[21], 0)
        self.surface.blit(self.Text_bassa, self.pointlist[22][0])
        self.surface.blit(self.Text_media, self.pointlist[23][0])
        self.surface.blit(self.Text_alta, self.pointlist[24][0])
        self.draw_numbers()
        pygame.display.flip()

    def get_point(self):
        """Obtains the points to draw the interface."""
        list0 = [[0, 0], [240.0, 320]]
        list1 = [[240.0, 0], [480, 320]]
        list2 = [[58, 18]]
        list3 = [[271, 18]]
        list4 = [[55, 15]]
        list5 = [[268, 15]]
        list6 = [[30, 65], [180, 105.0]]
        list7 = [[30, 65], [180, 105.0]]
        list8 = [[33, 193], [75, 45.0]]
        list9 = [[138, 193], [75, 45.0]]
        list10 = [[30, 190], [75, 45.0]]
        list11 = [[135, 190], [75, 45.0]]
        list12 = [[0, 255], [90, 65]]
        list13 = [[0, 255], [90, 320], [90, 255]]
        list14 = [[0, 255], [90, 320]]
        list15 = [[4, 269]]
        list16 = [[53, 209], [30, 10]]
        list17 = [[158, 209], [30, 10]]
        list18 = [[168, 199], [10, 30]]
        list19 = [[52, 208], [30, 10]]
        list20 = [[157, 208], [30, 10]]
        list21 = [[167, 198], [10, 30]]
        list22 = [[288, 77]]
        list23 = [[288, 162]]
        list24 = [[288, 247]]
        list25 = [[60, 70]]
        list26 = [[270 - 1, 65 - 1], [180, 60]]
        list27 = [[270, 65], [180, 60]]
        list28 = [[270 + 3, 150 + 3], [180, 60]]
        list29 = [[270 + 3, 235 + 3], [180, 60]]
        list30 = [[270, 150], [180, 60]]
        list31 = [[270, 235], [180, 60]]
        list32 = [[270 - 1, 150 - 1], [180, 60]]
        list33 = [[270, 150], [180, 60]]
        list34 = [[270 + 3, 65 + 3], [180, 60]]
        list35 = [[270 + 3, 235 + 3], [180, 60]]
        list36 = [[270, 65], [180, 60]]
        list37 = [[270, 235], [180, 60]]
        list38 = [[270 - 1, 235 - 1], [180, 60]]
        list39 = [[270, 235], [180, 60]]
        list40 = [[270 + 3, 65 + 3], [180, 60]]
        list41 = [[270 + 3, 150 + 3], [180, 60]]
        list42 = [[270, 65], [180, 60]]
        list43 = [[270, 150], [180, 60]]
        list44 = [[240, 60], [480, 260]]
        list = [list0, list1, list2, list3, list4, list5, list6, list7, list8, list9, list10, list11, list12, list13, list14, list15, list16, list17, list18, list19, list20, list21, list22,
                list23, list24, list25, list26, list27, list28, list29, list30, list31, list32, list33, list34, list35, list36, list37, list38, list39, list40, list41, list42, list43, list44]
        list = self.scale_point(list, Screen_scale)
        return list

    def scale_point(self, list, scale):
        """Scale the points of the lists."""
        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                list[i][j][0] *= scale
                list[i][j][1] *= scale
        return list

    def diff_selection(self):
        """Print the selected difficulty."""
        pygame.draw.rect(self.surface, LIGHTBLUE2, self.pointlist[44], 0)
        if self.difficulty == "Low":
            pygame.draw.rect(self.surface, BLACK, self.pointlist[26], 0)
            pygame.draw.rect(self.surface, GREY3, self.pointlist[27], 0)
            pygame.draw.rect(self.surface, BLACK, self.pointlist[28], 0)
            pygame.draw.rect(self.surface, BLACK, self.pointlist[29], 0)
            pygame.draw.rect(self.surface, GREY2, self.pointlist[30], 0)
            pygame.draw.rect(self.surface, GREY2, self.pointlist[31], 0)
        elif self.difficulty == "Medium":
            pygame.draw.rect(self.surface, BLACK, self.pointlist[32], 0)
            pygame.draw.rect(self.surface, GREY3, self.pointlist[33], 0)
            pygame.draw.rect(self.surface, BLACK, self.pointlist[34], 0)
            pygame.draw.rect(self.surface, BLACK, self.pointlist[35], 0)
            pygame.draw.rect(self.surface, GREY2, self.pointlist[36], 0)
            pygame.draw.rect(self.surface, GREY2, self.pointlist[37], 0)
        elif self.difficulty == "High":
            pygame.draw.rect(self.surface, BLACK, self.pointlist[38], 0)
            pygame.draw.rect(self.surface, GREY3, self.pointlist[39], 0)
            pygame.draw.rect(self.surface, BLACK, self.pointlist[40], 0)
            pygame.draw.rect(self.surface, BLACK, self.pointlist[41], 0)
            pygame.draw.rect(self.surface, GREY2, self.pointlist[42], 0)
            pygame.draw.rect(self.surface, GREY2, self.pointlist[43], 0)
        self.surface.blit(self.Text_bassa, self.pointlist[22][0])
        self.surface.blit(self.Text_media, self.pointlist[23][0])
        self.surface.blit(self.Text_alta, self.pointlist[24][0])
        pygame.display.flip()

    def draw_numbers(self):
        """Print the selected duration."""
        pygame.draw.rect(self.surface, WHITE, self.pointlist[6], 0)
        pygame.draw.rect(self.surface, GREY, self.pointlist[7], round(1 * Screen_scale))
        if int(self.duration / 10) == 0:
            num = self.font3.render("0" + str(self.duration), True, BLACK)
        else:
            num = self.font3.render(str(self.duration), True, BLACK)
        self.surface.blit(num, self.pointlist[25][0])
        pygame.display.flip()

    def controls(self, posx, posy):
        """Controls of the preference menu."""
        if self.check_low(posx, posy):
            print("Difficulty: Low")
            self.difficulty = "Low"
            self.diff_selection()
        if self.check_medium(posx, posy):
            print("Difficulty: Medium")
            self.difficulty = "Medium"
            self.diff_selection()
        if self.check_high(posx, posy):
            print("Difficulty: High")
            self.difficulty = "High"
            self.diff_selection()
        if self.check_plus(posx, posy):
            if self.duration < 60:
                self.duration += 5
                print("Duration: " + str(self.duration) + " min")
            self.draw_numbers()
        if self.check_minus(posx, posy):
            if self.duration > 5:
                self.duration -= 5
                print("Duration: " + str(self.duration) + " min")
            self.draw_numbers()
        if self.check_back(posx, posy):
            print("Back")
            return "Back"

    def check_low(self, posx, posy):
        """Check if the selected difficulty is low."""
        if posx > self.pointlist[27][0][0] and posx < self.pointlist[27][0][0] + self.pointlist[27][1][0]:
            if posy > self.pointlist[27][0][1] and posy < self.pointlist[27][0][1] + self.pointlist[27][1][1]:
                return True
            else:
                return False
        else:
            return False

    def check_medium(self, posx, posy):
        """Check if the selected difficulty is medium."""
        if posx > self.pointlist[27][0][0] and posx < self.pointlist[27][0][0] + self.pointlist[27][1][0]:
            if posy > self.pointlist[33][0][1] and posy < self.pointlist[33][0][1] + self.pointlist[33][1][1]:
                return True
            else:
                return False
        else:
            return False

    def check_high(self, posx, posy):
        """Check if the selected difficulty is high."""
        if posx > self.pointlist[27][0][0] and posx < self.pointlist[27][0][0] + self.pointlist[27][1][0]:
            if posy > self.pointlist[39][0][1] and posy < self.pointlist[39][0][1] + self.pointlist[39][1][1]:
                return True
            else:
                return False
        else:
            return False

    def check_plus(self, posx, posy):
        """Check if the duration has been increased."""
        if posx > self.pointlist[11][0][0] and posx < self.pointlist[11][0][0] + self.pointlist[11][1][0]:
            if posy > self.pointlist[11][0][1] and posy < self.pointlist[11][0][1] + self.pointlist[11][1][1]:
                return True
            else:
                return False
        else:
            return False

    def check_minus(self, posx, posy):
        """Check if the duration has been decreased."""
        if posx > self.pointlist[10][0][0] and posx < self.pointlist[10][0][0] + self.pointlist[10][1][0]:
            if posy > self.pointlist[10][0][1] and posy < self.pointlist[10][0][1] + self.pointlist[10][1][1]:
                return True
            else:
                return False
        else:
            return False

    def check_back(self, posx, posy):
        """Check if the back button has been selected."""
        m = self.pointlist[12][1][1] / self.pointlist[12][1][0]
        q = self.pointlist[12][0][1]
        if posx > self.pointlist[12][0][0] and posx < self.pointlist[12][0][0] + self.pointlist[12][1][0]:
            if posy > m * posx + q:
                return True
            else:
                return False
        else:
            return False


class Init_menu:
    """Class of the init menu."""

    def __init__(self, surface, dur, diff):
        """Init Init_menu class."""
        self.surface = surface
        self.surface.fill(GREY)
        self.division = H_SIZE / 5 - 5
        self.radius = 30
        self.difficulty = diff
        self.duration = str(dur) + " min"
        self.pointlist = self.get_point()
        self.font1 = pygame.font.SysFont(name="Terminal", size=round(Screen_scale * 60))
        self.font2 = pygame.font.SysFont(name="Terminal", size=round(Screen_scale * 40))
        self.font3 = pygame.font.SysFont(name="Terminal", size=round(Screen_scale * 60))
        pygame.draw.rect(self.surface, [LIGHTBLUE[0] + 20, LIGHTBLUE[1] + 20, LIGHTBLUE[2] + 20], self.pointlist[0])
        pygame.draw.rect(self.surface, [LIGHTBLUE[0] - 25, LIGHTBLUE[1] - 25, LIGHTBLUE[2] - 25], self.pointlist[1])
        pygame.draw.rect(self.surface, [LIGHTBLUE[0] - 25, LIGHTBLUE[1] - 25, LIGHTBLUE[2] - 25], self.pointlist[2])
        pygame.draw.rect(self.surface, [LIGHTBLUE[0] - 25, LIGHTBLUE[1] - 25, LIGHTBLUE[2] - 25], self.pointlist[3])
        pygame.draw.rect(self.surface, LIGHTGREY, self.pointlist[4])
        pygame.draw.rect(self.surface, LIGHTGREY, self.pointlist[5])
        pygame.draw.rect(self.surface, LIGHTGREY, self.pointlist[6])
        self.ese1_shadow = self.font3.render("Canyon flight     1' 00''", True, BLACK)
        self.ese2_shadow = self.font3.render("Giant slalom      1' 30''", True, BLACK)
        self.ese3_shadow = self.font3.render("Equilibrist               30''", True, BLACK)
        self.ese4_shadow = self.font3.render("Olympic dives         30''", True, BLACK)
        self.ese1 = self.font3.render("Canyon flight     1' 00''", True, LIGHTGREY)
        self.ese2 = self.font3.render("Giant slalom      1' 30''", True, LIGHTGREY)
        self.ese3 = self.font3.render("Equilibrist               30''", True, LIGHTGREY)
        self.ese4 = self.font3.render("Olympic dives         30''", True, LIGHTGREY)
        self.surface.blit(self.ese1_shadow, self.pointlist[17][0])
        self.surface.blit(self.ese2_shadow, self.pointlist[18][0])
        self.surface.blit(self.ese3_shadow, self.pointlist[19][0])
        self.surface.blit(self.ese4_shadow, self.pointlist[20][0])
        self.surface.blit(self.ese1, self.pointlist[13][0])
        self.surface.blit(self.ese2, self.pointlist[14][0])
        self.surface.blit(self.ese3, self.pointlist[15][0])
        self.surface.blit(self.ese4, self.pointlist[16][0])
        self.back = pygame.image.load("Images/back.png")
        self.start = pygame.image.load("Images/start.png")
        self.back = pygame.transform.scale(self.back, (round(60 * Screen_scale), round(60 * Screen_scale)))
        self.start = pygame.transform.scale(self.start, (round(46 * Screen_scale), round(46 * Screen_scale)))
        self.Text_dif = self.font2.render("Difficoltà: ", True, BLACK)
        self.Text_dur = self.font2.render("duration: ", True, BLACK)
        self.Text_dif_var = self.font2.render(self.difficulty, True, BLACK)
        self.Text_dur_var = self.font2.render(self.duration, True, BLACK)
        self.Text_dif_var_shadow = self.font2.render(self.difficulty, True, WHITE)
        self.Text_dur_var_shadow = self.font2.render(self.duration, True, WHITE)
        self.surface.blit(self.Text_dif, self.pointlist[7][0])
        self.surface.blit(self.Text_dur, self.pointlist[8][0])
        self.surface.blit(self.Text_dif_var_shadow, self.pointlist[21][0])
        self.surface.blit(self.Text_dur_var_shadow, self.pointlist[22][0])
        self.surface.blit(self.Text_dif_var, self.pointlist[9][0])
        self.surface.blit(self.Text_dur_var, self.pointlist[10][0])
        self.surface.blit(self.back, self.pointlist[11][0])
        self.surface.blit(self.start, self.pointlist[12][0])
        pygame.display.flip()

    def get_point(self):
        """Obtains the points to draw the interface."""
        list0 = [[0, 66.0], [480, 59.0]]
        list1 = [[0, 131.0], [480, 59.0]]
        list2 = [[0, 196.0], [480, 59.0]]
        list3 = [[0, 261.0], [480, 59.0]]
        list4 = [[0, 1], [115.0, 59.0]]
        list5 = [[365.0, 1], [235.0, 59.0]]
        list6 = [[120.0, 1], [240.0, 59.0]]
        list7 = [[124, 4]]
        list8 = [[124, 34]]
        list9 = [[268, 4]]
        list10 = [[268, 34]]
        list11 = [[24, 0]]
        list12 = [[400, 8]]
        list13 = [[11, 74.0]]
        list14 = [[10, 139.0]]
        list15 = [[10, 205.0]]
        list16 = [[12, 269.0]]
        list17 = [[12, 75.0]]
        list18 = [[11, 140.0]]
        list19 = [[11, 206.0]]
        list20 = [[13, 270.0]]
        list21 = [[269, 5]]
        list22 = [[269, 35]]
        list = [list0, list1, list2, list3, list4, list5, list6, list7, list8, list9, list10, list11, list12, list13, list14, list15, list16, list17, list18, list19, list20, list21, list22]
        list = self.scale_point(list, Screen_scale)
        return list

    def scale_point(self, list, scale):
        """Scale the points of the lists."""
        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                list[i][j][0] *= scale
                list[i][j][1] *= scale
        return list

    def controls(self, posx, posy):
        """Controls of the init menu."""
        if self.check_back(posx, posy):
            print("Back")
            return "Back"
        if self.check_start(posx, posy):
            print("Start")
            return "Start"

    def check_back(self, posx, posy):
        """Check if the back button was selected."""
        if posy > self.pointlist[4][0][1] and posy < self.pointlist[4][0][1] + self.pointlist[4][1][1]:
            if posx > self.pointlist[4][0][0] and posx < self.pointlist[4][0][0] + self.pointlist[4][1][0]:
                return True
            else:
                return False
        else:
            return False

    def check_start(self, posx, posy):
        """Check if the start button was selected."""

        if posy > self.pointlist[4][0][1] and posy < self.pointlist[4][0][1] + self.pointlist[4][1][1]:
            if posx > self.pointlist[5][0][0] and posx < self.pointlist[5][0][0] + self.pointlist[5][1][0]:
                return True
            else:
                return False
        else:
            return False


class Setup_menu:
    """Class of setup sensors menu."""

    def __init__(self, surface):
        """Init of Setup_menu class."""
        self.surface = surface
        self.pointlist = self.get_point()
        self.font1 = pygame.font.SysFont(name="Terminal", size=round(Screen_scale * 50))
        self.font2 = pygame.font.SysFont(name="Terminal", size=round(Screen_scale * 30))
        self.surface.fill(GREY)
        self.Text_con = self.font1.render("Connection in progress...", True, LIGHTGREY)
        self.Text_sens0 = self.font2.render("Waiting sensor 0", True, LIGHTGREY)
        self.Text_sens1 = self.font2.render("Waiting sensor 1", True, LIGHTGREY)
        self.Text_sens2 = self.font2.render("Waiting sensor 2", True, LIGHTGREY)
        self.Text_sens3 = self.font2.render("Waiting sensor 3", True, LIGHTGREY)
        self.Text_sens4 = self.font2.render("Waiting sensor 4", True, LIGHTGREY)
        self.Text_sens5 = self.font2.render("Waiting sensor 5", True, LIGHTGREY)
        self.surface.blit(self.Text_con, self.pointlist[0][0])
        pygame.draw.rect(self.surface, BLACK, self.pointlist[1])
        pygame.draw.rect(self.surface, LIGHTGREY, self.pointlist[2])
        pygame.draw.rect(self.surface, BLACK, [self.pointlist[3][0][0] + 3, self.pointlist[3][0][1] + 3, self.pointlist[3][1][0], self.pointlist[3][1][1]])
        pygame.draw.rect(self.surface, BLACK, [self.pointlist[4][0][0] + 3, self.pointlist[4][0][1] + 3, self.pointlist[4][1][0], self.pointlist[3][1][1]])
        pygame.draw.rect(self.surface, BLACK, [self.pointlist[5][0][0] + 3, self.pointlist[5][0][1] + 3, self.pointlist[5][1][0], self.pointlist[3][1][1]])
        pygame.draw.rect(self.surface, BLACK, [self.pointlist[6][0][0] + 3, self.pointlist[6][0][1] + 3, self.pointlist[6][1][0], self.pointlist[3][1][1]])
        pygame.draw.rect(self.surface, BLACK, [self.pointlist[7][0][0] + 3, self.pointlist[7][0][1] + 3, self.pointlist[7][1][0], self.pointlist[3][1][1]])
        pygame.draw.rect(self.surface, BLACK, [self.pointlist[8][0][0] + 3, self.pointlist[8][0][1] + 3, self.pointlist[8][1][0], self.pointlist[3][1][1]])
        pygame.draw.rect(self.surface, LIGHTBLUE, self.pointlist[3])
        pygame.draw.rect(self.surface, LIGHTBLUE, self.pointlist[4])
        pygame.draw.rect(self.surface, LIGHTBLUE, self.pointlist[5])
        pygame.draw.rect(self.surface, LIGHTBLUE, self.pointlist[6])
        pygame.draw.rect(self.surface, LIGHTBLUE, self.pointlist[7])
        pygame.draw.rect(self.surface, LIGHTBLUE, self.pointlist[8])
        self.surface.blit(self.Text_sens0, self.pointlist[9][0])
        self.surface.blit(self.Text_sens1, self.pointlist[10][0])
        self.surface.blit(self.Text_sens2, self.pointlist[11][0])
        self.surface.blit(self.Text_sens3, self.pointlist[12][0])
        self.surface.blit(self.Text_sens4, self.pointlist[13][0])
        self.surface.blit(self.Text_sens5, self.pointlist[14][0])
        pygame.display.flip()

    def conn_sensor(self, sensor, state):
        """Obtains sensors status."""
        sens0 = self.pointlist[3]
        sens1 = self.pointlist[4]
        sens2 = self.pointlist[5]
        sens3 = self.pointlist[6]
        sens4 = self.pointlist[7]
        sens5 = self.pointlist[8]
        txt0 = self.pointlist[9][0]
        txt1 = self.pointlist[10][0]
        txt2 = self.pointlist[11][0]
        txt3 = self.pointlist[12][0]
        txt4 = self.pointlist[13][0]
        txt5 = self.pointlist[14][0]
        self.sensors = {}
        self.sensors[sensor] = state
        if state == "Connected":
            color = GREEN
        elif state == "Error":
            color = RED
        if sensor == "mpu0":
            pos_rect = sens0
            pos_txt = txt0
            sens_txt = self.Text_sens0
        elif sensor == "mpu1":
            pos_rect = sens1
            pos_txt = txt1
            sens_txt = self.Text_sens1
        elif sensor == "mpu2":
            pos_rect = sens2
            pos_txt = txt2
            sens_txt = self.Text_sens2
        elif sensor == "mpu3":
            pos_rect = sens3
            pos_txt = txt3
            sens_txt = self.Text_sens3
        elif sensor == "mpu4":
            pos_rect = sens4
            pos_txt = txt4
            sens_txt = self.Text_sens4
        elif sensor == "mpu5":
            pos_rect = sens5
            pos_txt = txt5
            sens_txt = self.Text_sens5

        pygame.draw.rect(self.surface, color, pos_rect)
        self.surface.blit(sens_txt, pos_txt)
        pygame.display.flip()

    def draw_loading(self, percent):
        """Draw the loading."""
        if percent <= 100:
            pygame.draw.rect(self.surface, GREEN, [self.pointlist[2][0][0], self.pointlist[2][0][1], self.pointlist[2][1][0] * (percent / 100), self.pointlist[2][1][1]])
            pygame.display.flip()

    def get_point(self):
        """Obtains the points to draw the interface."""
        list0 = [[45, 10]]
        list1 = [[30 - 1, 60 - 1], [W_SIZE - 2 * 30, 20]]
        list2 = [[30, 60], [W_SIZE - 2 * 30, 20]]
        list3 = [[30, 100], [W_SIZE / 2 - 45, (H_SIZE - 70) / 5]]
        list4 = [[W_SIZE / 2 + 15, 100], [W_SIZE / 2 - 45, (H_SIZE - 70) / 5]]
        list5 = [[30, 170], [W_SIZE / 2 - 45, (H_SIZE - 70) / 5]]
        list6 = [[W_SIZE / 2 + 15, 170], [W_SIZE / 2 - 45, (H_SIZE - 70) / 5]]
        list7 = [[30, 240], [W_SIZE / 2 - 45, (H_SIZE - 70) / 5]]
        list8 = [[W_SIZE / 2 + 15, 240], [W_SIZE / 2 - 45, (H_SIZE - 70) / 5]]
        list9 = [[45, 115]]
        list10 = [[270, 115]]
        list11 = [[45, 185]]
        list12 = [[270, 185]]
        list13 = [[45, 255]]
        list14 = [[270, 255]]
        list = [list0, list1, list2, list3, list4, list5, list6, list7, list8, list9, list10, list11, list12, list13, list14]
        list = self.scale_point(list, Screen_scale)
        return list

    def scale_point(self, list, scale):
        """Scale the points of the lists."""
        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                list[i][j][0] *= scale
                list[i][j][1] *= scale
        return list

    def check_sensors(self):
        """Check the sensors status."""
        list_err = []
        for s in self.sensors.keys():
            if self.sensors[s] == "Error":
                list_err.append(s)
        if len(list_err) > 0:
            print("Sensors ", end=" ")
            print(list_err, end=" ")
            print("Not connected")
            return False
        else:
            print("All sensors correctly connected.")
            return True


def select_menu(posx, posy):
    """Select the screen requested by the user."""
    global Menu_APP, Duration, Difficulty
    MENU_STATUS = Menu_APP.controls(posx, posy)

    if Menu_APP.__class__.__name__ == "Main_menu":
        if MENU_STATUS == "Training":
            Menu_APP = Train_menu(Surface)
        # TODO: implement the others button on the main menu
        '''
        elif MENU_STATUS == "Progress":
            Menu_APP = Prog_menu(Surface)
        elif MENU_STATUS == "Options":
            Menu_APP = Option_menu(Surface)
        '''
    elif Menu_APP.__class__.__name__ == "Train_menu":
        if MENU_STATUS == "Home":
            Menu_APP = Main_menu(Surface)
        elif MENU_STATUS == "Start":
            Menu_APP = Init_menu(Surface, Duration, Difficulty)
        elif MENU_STATUS == "Preference":
            Menu_APP = Pref_menu(Surface, Duration, Difficulty)
    elif Menu_APP.__class__.__name__ == "Pref_menu":
        if MENU_STATUS == "Back":
            Menu_APP = Train_menu(Surface)
        elif MENU_STATUS == "Preference":
            Menu_APP = Pref_menu(Surface)
        else:
            Duration = Menu_APP.duration
            Difficulty = Menu_APP.difficulty
    elif Menu_APP.__class__.__name__ == "Init_menu":
        if MENU_STATUS == "Back":
            Menu_APP = Train_menu(Surface)
        elif MENU_STATUS == "Start":
            Canyon_flight(Surface, Screen_scale)


if __name__ == "__main__":
    # Pygame initialization
    pygame.init()
    pygame.font.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('AEQUUS TRAINING APP')

    # Create pygame display
    Surface = pygame.display.set_mode((round(W_SIZE * Screen_scale), round(H_SIZE * Screen_scale)), pygame.FULLSCREEN)

    # Init training values prefereces (default)
    Difficulty = "Low"
    Duration = 5
    Duration_txt = str(Duration) + " min"

    # Init main menu
    Menu_APP = Main_menu(Surface)

    # Timer
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
