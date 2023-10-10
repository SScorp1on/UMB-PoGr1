from PIL import Image

width, height = 500, 400
image = Image.new("RGB", (width, height), (0, 0, 0))


def horizontalna_ciara(obr, x1, x2, y):
    for i in range(x1, x2):
        obr.putpixel((i, y), (255, 255, 255))  # biely bod na pozicii 10 10


def vertikalna_ciara(obr, x, y1, y2):
    for y in range(y1, y2):
        obr.putpixel((x, y), (255, 255, 255))  # biely bod na pozicii 10 10


def kresli_graf(obr, min_x, max_x, min_y, max_y):
    # os x
    vdy = obr.height / (max_y - min_y)
    osx_y = int(max_y * vdy)
    # os y
    vdx = obr.width / (max_x - min_x)
    osy_x = int(abs(min_x) * vdx)

    horizontalna_ciara(obr, 0, obr.width, osx_y)

    vertikalna_ciara(obr, osy_x, 0, obr.height)

    poc_del = max_y - min_y
    # dieliky
    for i in range(poc_del):
        vyska_diel = int(obr.height / poc_del)
        horizontalna_ciara(obr, 0, i, vyska_diel)


kresli_graf(image, -1, 8, -1, 1)
image.show()
