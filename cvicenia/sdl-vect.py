import sdl2.ext

sdl2.ext.init()
window = sdl2.ext.Window("Priklad Event Loop", size=(400, 200))
window.show()

plocha = window.get_surface()
pixle = sdl2.ext.PixelView(plocha)


class obdlznik:
    def __init__(self, x1, y1, x2, y2, farba):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.farba = farba

    def kresli(self):
        for x in range(min(self.x1, self.x2), max(self.x1, self.x2)):
            for y in range(min(self.y1, self.y2), max(self.y1, self.y2)):
                pixle[y][x] = self.farba

    def zasah(self, x, y):
        # if x > min(self.x1, self.x2) and x < max(self.x1, self.x2)\
        #         and y > min(self.y1, self.y2) and y < max(self.y1,self.y2):
        #     return True
        # return False
        if self.x1 - 5 < x < self.x1 + 5 and self.y1 - 5 < y < self.y1 + 5:
            return 1
        if self.x2 - 5 < x < self.x2 + 5 and self.y2 - 5 < y < self.y2 + 5:
            return 2
        return 0


sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
# double buffering
# test kreslenia obdlznika
obdlzniky = []
obdlzniky.append(obdlznik(10, 10, 100, 100, sdl2.ext.Color(255, 0, 0)))
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
                    editovanyO.x1 = event.motion.x
                    editovanyO.y1 = event.motion.y
                elif editovanyV == 2:
                    editovanyO.x2 = event.motion.x
                    editovanyO.y2 = event.motion.y
            elif novy is not None:
                novy.x2 = event.motion.x
                novy.y2 = event.motion.y
            # obdlzniky[-1].x2 = event.motion.x
            # obdlzniky[-1].y2 = event.motion.y
        if event.type == sdl2.SDL_MOUSEBUTTONUP:
            novy = None
            editovanyO = None
            editovanyV = None
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
