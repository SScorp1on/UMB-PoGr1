import random

import sdl2.ext


def main():
    sirka = 800
    vyska = 700
    sdl2.ext.init()
    window = sdl2.ext.Window("Test", size=(sirka, vyska))
    window.show()
    plocha = window.get_surface()
    pixle = sdl2.ext.PixelView(plocha)
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_h:
                    print("h")
                    # náhodná horizontálna úsečka
                    x = random.randint(0, sirka - 1)
                    y = random.randint(0, vyska - 1)
                    x1 = random.randint(0, sirka - 1)
                    for i in range(x, x1):
                        pixle[i][y] = sdl2.ext.Color(255, 255, 255)
                    window.refresh()
                if event.key.keysym.sym == sdl2.SDLK_v:
                    print("v")
                    # náhodná vertikálna úsečka
                    x = random.randint(0, sirka - 1)
                    y = random.randint(0, vyska - 1)
                    y1 = random.randint(0, vyska - 1)
                    for i in range(y, y1):
                        pixle[x][i] = sdl2.ext.Color(255, 255, 255)
                    window.refresh()
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                if event.button.button == sdl2.SDL_BUTTON_LEFT:
                    print("left")
                    # náhodný vyplnený obdĺžnik
                    x = random.randint(0, sirka - 1)
                    y = random.randint(0, vyska - 1)
                    x1 = random.randint(0, sirka - 1)
                    y1 = random.randint(0, vyska - 1)
                    for i in range(x, x1):
                        for j in range(y, y1):
                            pixle[i][j] = sdl2.ext.Color(255, 255, 255)

                    window.refresh()
                if event.button.button == sdl2.SDL_BUTTON_RIGHT:
                    print("right")
                    # vymazanie celej plochy okna
                    for i in range(sirka - 1):
                        for j in range(vyska - 1):
                            pixle[i][j] = sdl2.ext.Color(0, 0, 0)
                    window.refresh()
    return 0


main()
