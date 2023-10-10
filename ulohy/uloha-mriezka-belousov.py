from PIL import Image

width, height = 300, 300
image = Image.new("RGB", (width, height), (0, 0, 0))


def kresli_mriezku(obrazok, poc_ciar_x, poc_ciar_y):
    for i in range(poc_ciar_x):
        if i > 0:
            x = i * width // poc_ciar_x
            for y in range(height):
                obrazok.putpixel((x, y), (255, 255, 255))
    for i in range(poc_ciar_y):
        if i > 0:
            y = i * height // poc_ciar_y
            for x in range(width):
                obrazok.putpixel((x, y), (255, 255, 255))


kresli_mriezku(image, 10, 10)
image.show()
