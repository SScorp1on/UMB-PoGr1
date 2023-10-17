import math

from PIL import Image

width, height = 500, 400
image = Image.new("RGB", (width, height), (0, 0, 0))


def frange(od, do, krok):
    while od < do:
        yield od
        od += krok


def horizontalna_ciara(obr, x1, x2, y):
    math.sin(0)
    for i in range(x1, x2):
        obr.putpixel((i, y), (255, 255, 255))  # biely bod na pozicii 10 10


def vertikalna_ciara(obr, x, y1, y2):
    for y in range(y1, y2):
        obr.putpixel((x, y), (255, 255, 255))  # biely bod na pozicii 10 10


def kresli_graf(obr, min_x, max_x, min_y, max_y, funkcia):
    # os x
    vdy = obr.height / (max_y - min_y)
    osx_y = int(max_y * vdy)
    horizontalna_ciara(obr, 0, obr.width, osx_y)
    # os y
    vdx = obr.width / (max_x - min_x)
    osy_x = int(abs(min_x) * vdx)
    vertikalna_ciara(obr, osy_x, 0, obr.height)

    poc_del = max_y - min_y
    # dieliky x
    for x in range(min_x, max_x):
        pom = int(x * vdx + osy_x)
        obr.putpixel((pom, osx_y - 1), (255, 255, 255))
        obr.putpixel((pom, osx_y - 2), (255, 255, 255))
        obr.putpixel((pom, osx_y - 3), (255, 255, 255))
    # dieliky y
    for y in range(min_y, max_y):
        pom = int(y * vdy - osx_y)
        obr.putpixel((osy_x + 1, pom), (255, 255, 255))
        obr.putpixel((osy_x + 2, pom), (255, 255, 255))
        obr.putpixel((osy_x + 3, pom), (255, 255, 255))
    # funkcia
    for x in frange(min_x, max_x, 0.0001):
        x2 = int(x * vdx + osy_x)
        y = eval(funkcia)
        y2 = int(y * vdy - osx_y)
        obr.putpixel((x2, y2), (255, 255, 255))


kresli_graf(image, -1, 7, -1, 1, "math.cos(x)")
image.show()
