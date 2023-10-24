from PIL import Image


def horizontálna_ciara(obrazok, x, y, dlzka, farba):
    for i in range(dlzka):
        obrazok.putpixel((x + i, y), farba)


def kresli_stlpce(zoznam, sirka, vyska):
    obrazok = Image.new('RGB', (sirka, vyska), (0, 0, 0))
    pocet_stlpcov = len(zoznam)
    sirka_stlpca = int(sirka / pocet_stlpcov)
    min_hodnota = min(zoznam)
    max_hodnota = max(zoznam)
    centralna_ciara = int((max_hodnota / (max_hodnota - min_hodnota)) * vyska)
    horizontálna_ciara(obrazok, 0, centralna_ciara, sirka, (255, 255, 255))
    for i in range(pocet_stlpcov):
        if zoznam[i] >= 0:
            vyska_stlpca = int((zoznam[i] / max_hodnota) * centralna_ciara)
            for x in range(i * sirka_stlpca, ((i + 1) * sirka_stlpca)):
                for y in range(centralna_ciara - vyska_stlpca, centralna_ciara):
                    obrazok.putpixel((x, y), (0, 255, 0))
            for x in range(i * sirka_stlpca, ((i + 1) * sirka_stlpca), sirka_stlpca):
                for y in range(centralna_ciara - vyska_stlpca, centralna_ciara):
                    obrazok.putpixel((x, y), (0, 255, 0))
        else:
            vyska_stlpca = int((abs(zoznam[i]) / abs(min_hodnota)) * (vyska - centralna_ciara))
            for x in range(i * sirka_stlpca, (i + 1) * sirka_stlpca):
                for y in range(centralna_ciara, centralna_ciara + vyska_stlpca):
                    obrazok.putpixel((x, y), (255, 0, 0))
    return obrazok


obr = kresli_stlpce([10, 5, 7, -4, -1], 300, 200)
obr.show()
