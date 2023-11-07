import random

from PIL import Image

obr = Image.new('RGB', (300, 200), (0, 0, 0))


def ciarkovy_kruh(obrazok, x_c, y_c, r, d, farba):
    x, y = r, 0
    p = 1 - r
    dash = 0
    while x > y:
        if dash % 2 * d < d:
            if obrazok.size[0] > x_c + x > 0 and obrazok.size[1] > y_c + y > 0:
                obrazok.putpixel((x_c + x, y_c + y), farba)
            if obrazok.size[0] > x_c + y > 0 and obrazok.size[1] > y_c + x > 0:
                obrazok.putpixel((x_c + y, y_c + x), farba)
            if obrazok.size[0] > x_c + y > 0 and obrazok.size[1] > y_c - x > 0:
                obrazok.putpixel((x_c + y, y_c - x), farba)
            if obrazok.size[0] > x_c + x > 0 and obrazok.size[1] > y_c - y > 0:
                obrazok.putpixel((x_c + x, y_c - y), farba)
            if obrazok.size[0] > x_c - x > 0 and obrazok.size[1] > y_c - y > 0:
                obrazok.putpixel((x_c - x, y_c - y), farba)
            if obrazok.size[0] > x_c - y > 0 and obrazok.size[1] > y_c - x > 0:
                obrazok.putpixel((x_c - y, y_c - x), farba)
            if obrazok.size[0] > x_c - y > 0 and obrazok.size[1] > y_c + x > 0:
                obrazok.putpixel((x_c - y, y_c + x), farba)
            if obrazok.size[0] > x_c - x > 0 and obrazok.size[1] > y_c + y > 0:
                obrazok.putpixel((x_c - x, y_c + y), farba)
        dash += 1
        y += 1
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1


sirka = obr.size[0]
vyska = obr.size[1]
x = random.randrange(0, sirka)
y = random.randrange(0, vyska)
r = random.randrange(1, 50)
d = random.randrange(1, 30)
ciarkovy_kruh(obr, x, y, r, d, (255, 255, 255))
obr.show()
