from PIL import Image

width = 300
height = 200


def obdlznik(x, y, s, v):
    for i in range(x, x + s):
        for j in range(y, y + v):
            obr.putpixel((i, j), (255, 255, 255))


def horizontalna_ciara(x1, x2, y):
    for i in range(x1, x2):
        obr.putpixel((i, y), (255, 255, 255))  # biely bod na pozicii 10 10


def vertikalna_ciara(x, y1, y2):
    for i in range(y1, y2):
        obr.putpixel((x, i), (255, 255, 255))  # biely bod na pozicii 10 10


def kresli():
    for x in range(width):
        for y in range(height):
            r = 255 - x + y
            g = 255 - x
            b = 255 - x
            print(r, g, b)
            obr.putpixel((x, y), (r, g, b))


obr = Image.new('RGB', (width, height))
#horizontalna_ciara(0, width, 20)
#vertikalna_ciara(100, 0, height)
kresli()
#obdlznik(150, 10, 50, 50)
obr.show()
