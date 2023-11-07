from PIL import Image
img1 = Image.open("../images/earth.jpg").convert("L")
s, v = img1.size
vysledok = Image.new("L", (s, v))
for y in range(v):
    for x in range(s):
        col = img1.getpixel((x, y))
        col = int(100 * round(col / 100)) # zaokruhlenie na parne cislo
        vysledok.putpixel((x, y), col)
vysledok.show()
