from PIL import Image

img0 = Image.open('../images/circle30.png')
img1 = Image.open('../images/k30.jpg')
img2 = Image.open('../images/instagram30.jpg')
ims = [img0, img1, img2]
import random
pole = []
for i in range(10):
    riadok = []
    for j in range(10):
        riadok.append(random.randint(0, 2))
    pole.append(riadok)
for i in pole:
    print(i)
vysledok = Image.new("RGB", (len(pole[0]*30), len(pole)*30))
for x in range(len(pole)):
    for y in range(len(pole[x])):
        im = ims[pole[x][y]]
        vysledok.paste(im, (x*30, y*30))
vysledok.show()

