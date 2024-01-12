import random

import numpy as np
import sdl2.ext


class Bod:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Polygon:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color


def kresli_ciaru(plocha, x1, y1, x2, y2, color):
    sdl2.ext.line(plocha, color, (x1, y1, x2, y2))

#def kresli_ciaru(x1, y1, x2, y2, farba):
#    dx = abs(x2 - x1)
#    dy = abs(y2 - y1)
#    dlzka = dx if dx >= dy else dy
#    if dlzka == 0:
#        return
#    dx = float(x2 - x1) / dlzka
#    dy = float(y2 - y1) / dlzka
#    x = x1
#    y = y1
#    i = 1
#    while i <= dlzka:
#        x = x + dx
#        y = y + dy
#        i = i + 1
#        if 0 <= x < SIRKA and 0 <= y < VYSKA:
#            pixle[int(y)][int(x)] = farba


def random_color():
    return sdl2.ext.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)


def otocanie(point, angle, center):
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])

    point_array = np.array([point.x - center.x, point.y - center.y])

    rotated_point = np.dot(rotation_matrix, point_array)

    rotated_point = Bod(rotated_point[0] + center.x, rotated_point[1] + center.y)

    return rotated_point


sdl2.ext.init()
SIRKA = 800
VYSKA = 600
window = sdl2.ext.Window("Skuska", size=(SIRKA, VYSKA))
window.show()
plocha = window.get_surface()
pixels = sdl2.ext.PixelView(plocha)

polygons = []
current_polygon = []
window.refresh()
center = Bod(SIRKA / 2, VYSKA / 2)
angle = 0.01

running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                current_polygon.append(Bod(event.button.x, event.button.y))
            elif event.button.button == sdl2.SDL_BUTTON_RIGHT:
                if current_polygon:
                    polygons.append(Polygon(current_polygon, (random_color())))
                    current_polygon = []

    sdl2.ext.fill(plocha, sdl2.ext.Color(0, 0, 0))
    for polygon in polygons:
        for i in range(len(polygon.vertices)):
            polygon.vertices[i] = otocanie(polygon.vertices[i], angle, center)
            kresli_ciaru(plocha, polygon.vertices[i].x, polygon.vertices[i].y,
                         polygon.vertices[(i + 1) % len(polygon.vertices)].x,
                         polygon.vertices[(i + 1) % len(polygon.vertices)].y, polygon.color)

    for i in range(len(current_polygon)):
        kresli_ciaru(plocha, current_polygon[i].x, current_polygon[i].y,
                     current_polygon[(i + 1) % len(current_polygon)].x,
                     current_polygon[(i + 1) % len(current_polygon)].y,
                     sdl2.ext.Color(255, 255, 255))

    window.refresh()

sdl2.ext.quit()
