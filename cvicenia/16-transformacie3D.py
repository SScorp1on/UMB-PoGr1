#!/usr/bin/python3

"""16-transformacie3D.py: priklad aplikovania transformacii na 3D objekty"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

import numpy as np
import sdl2.ext

SIRKA = 400
VYSKA = 300

sdl2.ext.init()
window = sdl2.ext.Window("Priklad 3D transformacie", size=(SIRKA, VYSKA))
window.show()

plocha = window.get_surface()
pixle = sdl2.ext.PixelView(plocha)


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
        self.z = z
        self.w = w

    def vrat_np(self):
        return np.array([self.x, self.y, self.z, self.w])

    def __repr__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.w)


class troj:
    def __init__(self, bod1, bod2, bod3, col):
        self.bod1 = bod1
        self.bod2 = bod2
        self.bod3 = bod3
        self.col = col
        # transformacna matica
        self.transformacia = np.array([[1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]])

    def kresli(self, premietnutie):
        # aplikuj transformacie a preved z homogenych do kartezianskych suradnic
        bod1hs = self.transformacia.dot(self.bod1.vrat_np())
        bod1hs = premietnutie.dot(bod1hs)
        bod1ks = (bod1hs[0] / bod1hs[3], bod1hs[1] / bod1hs[3])
        bod2hs = self.transformacia.dot(self.bod2.vrat_np())
        bod2hs = premietnutie.dot(bod2hs)
        bod2ks = (bod2hs[0] / bod2hs[3], bod2hs[1] / bod2hs[3])
        bod3hs = self.transformacia.dot(self.bod3.vrat_np())
        bod3hs = premietnutie.dot(bod3hs)
        bod3ks = (bod3hs[0] / bod3hs[3], bod3hs[1] / bod3hs[3])
        # prepocitaj z NDC (-1..1) na obrazovku
        usecka(SIRKA // 2 + bod1ks[0], VYSKA // 2 + bod1ks[1], SIRKA // 2 + bod2ks[0], VYSKA // 2 + bod2ks[1], self.col)
        usecka(SIRKA // 2 + bod2ks[0], VYSKA // 2 + bod2ks[1], SIRKA // 2 + bod3ks[0], VYSKA // 2 + bod3ks[1], self.col)
        usecka(SIRKA // 2 + bod3ks[0], VYSKA // 2 + bod3ks[1], SIRKA // 2 + bod1ks[0], VYSKA // 2 + bod1ks[1], self.col)


class model:
    def __init__(self, pozicia, orientacia, mierka=(1, 1, 1)):
        self.trojuholniky = []
        self.pozicia = pozicia
        self.orientacia = orientacia
        self.mierka = mierka

    def pridaj_trojuholnik(self, t):
        self.trojuholniky.append(t)

    def kresli(self, premietnutie):
        for t in self.trojuholniky:
            t.kresli(premietnutie)

    def transformuj(self):
        # mierka
        Sx = self.mierka[0]
        Sy = self.mierka[1]
        Sz = self.mierka[2]
        skalovanie_modelu = np.array([  # skalovanie
            [Sx, 0, 0, 0],
            [0, Sy, 0, 0],
            [0, 0, Sz, 0],
            [0, 0, 0, 1]])
        # pozicia
        Tx = self.pozicia[0]
        Ty = self.pozicia[1]
        Tz = self.pozicia[2]
        posunutie_modelu = np.array([  # posunutie
            [1, 0, 0, Tx],
            [0, 1, 0, Ty],
            [0, 0, 1, Tz],
            [0, 0, 0, 1]])
        # orientacia
        a = np.radians(self.orientacia[0])  # otocenie okolo osi x
        otocenie_modelu_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(a), -np.sin(a), 0],
            [0, np.sin(a), np.cos(a), 0],
            [0, 0, 0, 1]])
        b = np.radians(self.orientacia[1])  # otocenie okolo osi y
        otocenie_modelu_y = np.array([
            [np.cos(b), 0, np.sin(b), 0],
            [0, 1, 0, 0],
            [-np.sin(b), 0, np.cos(b), 0],
            [0, 0, 0, 1]])
        c = np.radians(self.orientacia[2])  # otocenie okolo osi z
        otocenie_modelu_z = np.array([
            [np.cos(c), -np.sin(c), 0, 0],
            [np.sin(c), np.cos(c), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        # celkova transformacia
        model_local2world = skalovanie_modelu.dot(posunutie_modelu).dot(otocenie_modelu_x).dot(otocenie_modelu_y).dot(
            otocenie_modelu_z)
        for t in self.trojuholniky:
            t.transformacia = model_local2world


# vsetko zmaz
sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
window.refresh()

m = model(pozicia=(0, 0, 00), orientacia=(0, 0, 0))
# m.pridaj_trojuholnik(troj(bod(10, 20, 5, 1), bod(50, 40, 5, 1), bod(30, 70, 5, 1), sdl2.ext.Color(0, 200, 100)))
# m.pridaj_trojuholnik(troj(bod(40, 50, 5, 1), bod(80, 70, 5, 1), bod(60, 90, 5, 1), sdl2.ext.Color(200, 100, 100)))
m.pridaj_trojuholnik(troj(bod(-30, -30, 5, 1), bod(30, -30, 5, 1), bod(30, 30, 5, 1), sdl2.ext.Color(0, 200, 100)))
m.pridaj_trojuholnik(troj(bod(-30, -30, 5, 1), bod(30, 30, 5, 1), bod(-30, 30, 5, 1), sdl2.ext.Color(200, 100, 100)))
m.transformuj()
# rovnobezne kolme
FOV = 80
blizko, daleko = 0.1, 100
S = 1 / np.tan(np.radians(FOV / 2))
#S = 1 / np.tan(np.radians(FOV / 2 * np.pi / 180))
premietnutie = np.array([[S, 0, 0, 0],
                            [0, S, 0, 0],
                            [0, 0, -(daleko + blizko) / (daleko - blizko), -2 * daleko * blizko / (daleko - blizko)],
                            [0, 0, -1, 0]])
running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_t:
                m.pozicia = (m.pozicia[0] + 1, m.pozicia[1], m.pozicia[2])
                m.transformuj()
            if event.key.keysym.sym == sdl2.SDLK_r:
                m.orientacia = (m.orientacia[0], m.orientacia[1], m.orientacia[2] + 5)
                m.transformuj()
            if event.key.keysym.sym == sdl2.SDLK_s:
                m.orientacia = (m.orientacia[0], m.orientacia[1] + 5, m.orientacia[2])
                m.transformuj()
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
    # zmaz vsetko
    sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
    # plochy
    m.kresli(premietnutie)
    window.refresh()

sdl2.ext.quit()
