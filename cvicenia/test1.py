from PIL import Image

width, height = 256, 256

image = Image.new("RGB", (width, height), (0, 0, 0))


def kresli(obr):
    for x in range(obr.width):
        obr.putpixel((x, x), (255 - x, 0 + x, 255))
    for x in range(obr.height):
        obr.putpixel((obr.width - x - 1, x), (0 + x, 255, 255 - x))


kresli(image)

image.show()
