import numpy as np
import sdl2.ext

sdl2.ext.init()
window = sdl2.ext.Window("Priklad Event Loop", size=(400, 400))
window.show()

plocha = window.get_surface()
pixle = sdl2.ext.PixelView(plocha)


def usecka(x1, y1, x2, y2, farba):
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2)):
            if 0 <= y < len(pixle) and 0 <= x1 < len(pixle[0]):
                pixle[y][x1] = farba
    else:
        for x in range(min(x1, x2), max(x1, x2)):
            if 0 <= y1 < len(pixle) and 0 <= x < len(pixle[0]):
                pixle[y1][x] = farba


class bod:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w

    def vrat_np(self):
        return np.array([self.x, self.y, self.w])

    def __repr__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.w)


class obdlznik:
    def __init__(self, x1, y1, x2, y2, farba):
        self.bod1 = bod(x1, y1, 1)
        self.bod2 = bod(x2, y2, 1)
        self.bod3 = bod(x2, y1, 1)
        self.bod4 = bod(x1, y2, 1)
        self.farba = farba
        self.transformacia = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def transformuj(self, T):
        self.transformacia = T.dot(self.transformacia)

    def kresli(self):
        bod1t = self.transformacia.dot(self.bod1.vrat_np())
        bod2t = self.transformacia.dot(self.bod2.vrat_np())
        bod3t = self.transformacia.dot(self.bod2.vrat_np())
        bod4t = self.transformacia.dot(self.bod2.vrat_np())

        usecka(bod1t[0], bod1t[1], bod3t[0], bod3t[1], self.farba)
        usecka(bod3t[0], bod3t[1], bod2t[0], bod2t[1], self.farba)
        usecka(bod2t[0], bod2t[1], bod4t[0], bod4t[1], self.farba)
        usecka(bod4t[0], bod4t[1], bod1t[0], bod1t[1], self.farba)

    def zasah(self, x, y):
        # if x > min(self.x1, self.x2) and x < max(self.x1, self.x2)\
        #         and y > min(self.y1, self.y2) and y < max(self.y1,self.y2):
        #     return True
        # return False
        if self.bod1.x - 5 < x < self.bod1.x + 5 and self.bod1.y - 5 < y < self.bod1.y + 5:
            return 1
        if self.bod2.x - 5 < x < self.bod2.x + 5 and self.bod2.y - 5 < y < self.bod2.y + 5:
            return 2
        return 0


sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
obdlzniky = [obdlznik(50, 50, 100, 100, sdl2.ext.Color(255, 0, 0)),
             obdlznik(10, 110, 100, 200, sdl2.ext.Color(0, 255, 0))]
edit = True
editovanyO = None
editovanyV = None
running = True
novy = None
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if edit:
                for o in obdlzniky:
                    v = o.zasah(event.motion.x, event.motion.y)
                    if v != 0:
                        editovanyO = o
                        editovanyV = v
                        break
            else:
                novy = obdlznik(event.motion.x, event.motion.y, event.motion.x, event.motion.y, sdl2.ext.Color(0, 0, 0))
                obdlzniky.append(novy)
        if event.type == sdl2.SDL_MOUSEMOTION:
            if edit and editovanyO is not None:
                if editovanyV == 1:
                    editovanyO.bod1.x = event.motion.x
                    editovanyO.bod1.y = event.motion.y
                elif editovanyV == 2:
                    editovanyO.bod2.x = event.motion.x
                    editovanyO.bod2.y = event.motion.y
            elif novy is not None:
                novy.bod2.x = event.motion.x
                novy.bod2.y = event.motion.y
            # obdlzniky[-1].x2 = event.motion.x
            # obdlzniky[-1].y2 = event.motion.y
        if event.type == sdl2.SDL_MOUSEBUTTONUP:
            novy = None
            editovanyO = None
            editovanyV = None
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_t:
                # TODO posunutie obdlznika
                posunutie = np.array([[1, 0, 10], [0, 1, 0], [0, 0, 1]])
                obdlzniky[0].transformuj(posunutie)
            if event.key.keysym.sym == sdl2.SDLK_r:
                # TODO rotacia obdlznika
                pom = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
                obdlzniky[0].transformuj(pom)
                b = np.radians(30)
                rotacia = np.array([
                    [np.cos(b), -np.sin(b), 0],
                    [np.sin(b), np.cos(b), 0],
                    [0, 0, 1]])
                obdlzniky[0].transformuj(rotacia)
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
    # vsetko zmaz
    sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
    # oblzniky
    for o in obdlzniky:
        o.kresli()
    window.refresh()

sdl2.ext.quit()
