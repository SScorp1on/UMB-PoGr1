import random

from PIL import Image

obr = Image.new('RGB', (300, 200), 'black')


def nahodne_usecky(min_x, min_y, max_x, max_y, pocet):
    for i in range(pocet):
        x1 = int(random.randrange(min_x, max_x))
        y1 = int(random.randrange(min_y, max_y))
        x2 = int(random.randrange(min_x, max_x))
        y2 = int(random.randrange(min_y, max_y))
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        usecka(x1, y1, x2, y2, (r, g, b))


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
        if i % 2 == 0:
            obr.putpixel((int(x), int(y)), farba)


#usecka(0, 50, 299, 100, (0, 255, 0))
nahodne_usecky(0, 0, 200, 100, 10)
obr.show()
