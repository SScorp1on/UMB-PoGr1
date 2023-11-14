import sdl2.ext

sdl2.ext.init()
window = sdl2.ext.Window("Priklad Event Loop", size=(900, 700))
window.show()

plocha = window.get_surface()
pixle = sdl2.ext.PixelView(plocha)


class postava:
    def __init__(self, nazov, x, y, sirka, vyska):
        self.obr = sdl2.ext.load_image(nazov)
        self.x = x
        self.y = y
        self.sirka = sirka
        self.vyska = vyska
        self.frame = 0

    def kresli(self):
        rsrc = sdl2.SDL_Rect()
        rsrc.x, rsrc.y = self.sirka * int(self.frame), 0
        rsrc.w, rsrc.h = self.sirka, self.vyska
        rdest = sdl2.SDL_Rect()
        rdest.x, rdest.y = self.x, self.y
        rdest.w, rdest.h = self.sirka, self.vyska
        sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255), rdest)
        sdl2.SDL_BlitSurface(self.obr, rsrc, plocha, rdest)

    def dalsi_frame(self):
        self.frame += 0.01
        if self.frame > self.obr.w / self.sirka - 1:
            self.frame = 0

class tlacidlo:
    def __init__(self, x, y, s, v, obr):
        self.x = x
        self.y = y
        self.s = s
        self.v = v
        self.obr = obr

    def kresli(self):
        r = sdl2.SDL_Rect()
        r.x, r.y = self.x + 1, self.y + 1
        r.w, r.h = self.obr.w, self.obr.h
        sdl2.SDL_BlitSurface(self.obr, None, plocha, r)

        for xi in range(self.s):
            pixle[self.y][self.x + xi] = sdl2.ext.Color(0, 0, 0)
            pixle[self.y + self.v][self.x + xi] = sdl2.ext.Color(0, 0, 0)
        for yi in range(self.v):
            pixle[self.y + yi][self.x] = sdl2.ext.Color(0, 0, 0)
            pixle[self.y + yi][self.x + self.s] = sdl2.ext.Color(0, 0, 0)

    def zasah(self, x, y):
        return self.x < x < self.x + self.s and self.y < y < self.y + self.v


t1 = tlacidlo(30, 20, 30, 30, sdl2.ext.load_image("../images/instagram30.jpg"))
t2 = tlacidlo(70, 20, 30, 30, sdl2.ext.load_image("../images/circle30.png"))
p1 = postava("../images/rytier.png", 100, 30, 72, 86)
# vsetko zmaz
sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
# vykresli co treba
t1.kresli()
t2.kresli()
p1.kresli()
# double buffering
window.refresh()
stlacene = False
running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if t1.zasah(event.motion.x, event.motion.y):
                print('zasah t1')
            elif t2.zasah(event.motion.x, event.motion.y):
                print('zasah t2')
            else:
                stlacene = True
        if event.type == sdl2.SDL_MOUSEBUTTONUP:
            stlacene = False
        if event.type == sdl2.SDL_MOUSEMOTION and stlacene:
            pixle[event.motion.y][event.motion.x] = sdl2.ext.Color(0, 0, 0)
            window.refresh()
        # kreslenie obdĺžnika
        # x = event.button.x
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
    p1.dalsi_frame()
    p1.kresli()
    window.refresh()
sdl2.ext.quit()
