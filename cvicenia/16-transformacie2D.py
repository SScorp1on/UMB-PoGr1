#!/usr/bin/python3

"""16-transformacie2D.py: priklad aplikovania transformacii na 2D tvary"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

import numpy as np
import sdl2.ext

SIRKA = 400
VYSKA = 300

sdl2.ext.init()
window = sdl2.ext.Window("Priklad 2D transformacie", size=(SIRKA, VYSKA))
window.show()

plocha = window.get_surface()
pixle = sdl2.ext.PixelView(plocha)


class model:
    def __init__(self, position, orientation, scale):
        self.trojuholniky = []
        self.position = position
        self.orientation = orientation
        self.scale = scale

    def pridaj_trojuholnik(self, t):
        self.trojuholniky.append(t)

    def kresli(self):
        for t in self.trojuholniky:
            t.kresli()

    def transformuj(self):
        # scale
        Sx = self.scale[0]
        Sy = self.scale[1]
        Sz = self.scale[2]
        scale = np.array([[Sx, 0, 0, 0],
                          [0, Sy, 0, 0],
                          [0, 0, Sz, 0],
                          [0, 0, 0, 1]])
        # posun
        Tx = self.position[0]
        Ty = self.position[1]
        Tz = self.position[2]
        posun = np.array([[1, 0, 0, Tx],
                          [0, 1, 0, Ty],
                          [0, 0, 1, Tz],
                          [0, 0, 0, 1]])
        # rotacia
        a = np.radians(self.orientation[0])
        rotacia_x = np.array([[1, 0, 0, 0],
                              [0, np.cos(a), -np.sin(a), 0],
                              [0, np.sin(a), np.cos(a), 0],
                              [0, 0, 0, 1]])
        b = np.radians(self.orientation[1])
        #
        rotacia_y = np.array([[np.cos(b), 0, np.sin(b), 0],
                              [0, 1, 0, 0],
                              [-np.sin(b), 0, np.cos(b), 0],
                              [0, 0, 0, 1]])
        c = np.radians(self.orientation[2])
        rotacia_z = np.array([[np.cos(c), -np.sin(c), 0, 0],
                              [np.sin(c), np.cos(c), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
        # transformacia
        model2world = posun.dot(scale).dot(rotacia_x).dot(rotacia_y).dot(rotacia_z)
        for t in self.trojuholniky:
            t.transformacia = model2world


def usecka(x1, y1, x2, y2, farba):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dlzka = dx if dx >= dy else dy
    if dlzka == 0:
        return
    dx = float(x2 - x1) / dlzka
    dy = float(y2 - y1) / dlzka
    x = x1
    y = y1
    i = 1
    while i <= dlzka:
        x = x + dx
        y = y + dy
        i = i + 1
        if 0 <= x < SIRKA and 0 <= y < VYSKA:
            pixle[int(y)][int(x)] = farba


class bod:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.w = w
        self.z = z

    def vrat_np(self):
        return np.array([self.x, self.y, self.z, self.w])

    def __repr__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.w)


class trojuholnik:
    def __init__(self, bod1, bod2, bod3, col):
        self.bod1 = bod1
        self.bod2 = bod2
        self.bod3 = bod3
        self.col = col
        self.transformacia = np.array([[1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]])

    def transformuj(self, T):
        self.transformacia = T.dot(self.transformacia)

    def kresli(self):
        bod1t = self.transformacia.dot(self.bod1.vrat_np())
        bod2t = self.transformacia.dot(self.bod2.vrat_np())
        bod3t = self.transformacia.dot(self.bod3.vrat_np())
        usecka(SIRKA // 2 + bod1t[0], VYSKA // 2 + bod1t[1], SIRKA // 2 + bod2t[0], VYSKA // 2 + bod2t[1], self.col)
        usecka(SIRKA // 2 + bod2t[0], VYSKA // 2 + bod2t[1], SIRKA // 2 + bod3t[0], VYSKA // 2 + bod3t[1], self.col)
        usecka(SIRKA // 2 + bod3t[0], VYSKA // 2 + bod3t[1], SIRKA // 2 + bod1t[0], VYSKA // 2 + bod1t[1], self.col)

    def zasah(self, x, y):
        # if x > min(self.x1, self.x2) and x < max(self.x1, self.x2)\
        #         and y > min(self.y1, self.y2) and y < max(self.y1, self.y2):
        #     return True
        # return False
        if self.bod1.x - 5 < x < self.bod1.x + 5 and self.bod1.y - 5 < y < self.bod1.y + 5:
            return 1
        if self.bod2.x - 5 < x < self.bod2.x + 5 and self.bod2.y - 5 < y < self.bod2.y + 5:
            return 2
        return 0


# vsetko zmaz
sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
window.refresh()
m = model((0, 0, 0), (0, 0, 0), (1, 1, 1))
m.pridaj_trojuholnik(trojuholnik(bod(10, 20, 5, 1), bod(50, 40, 5, 1), bod(30, 70, 5, 1), sdl2.ext.Color(0, 200, 100)))
m.pridaj_trojuholnik(trojuholnik(bod(40, 50, 5, 1), bod(80, 70, 5, 1), bod(60, 90, 5, 1), sdl2.ext.Color(200, 100, 0)))
m.transformuj()
running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_t:
                m.position = (m.position[0] + 5, m.position[1], m.position[2])
                m.transformuj()
            if event.key.keysym.sym == sdl2.SDLK_r:
                m.orientation = (m.orientation[0], m.orientation[1], m.orientation[2] + 5)
                m.transformuj()
            if event.key.keysym.sym == sdl2.SDLK_s:
                m.scale = (m.scale[0] + 0.1, m.scale[1], m.scale[2])
                m.transformuj()

        if event.type == sdl2.SDL_QUIT:
            running = False
            break
    # zmaz vsetko
    sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
    # obdlzniky
    m.kresli()
    window.refresh()

sdl2.ext.quit()
