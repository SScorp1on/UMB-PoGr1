import sdl2.ext

img = sdl2.ext.load_image("../images/instagram30.jpg")
sdl2.ext.init()
window = sdl2.ext.Window("Test", size=(800, 700))
window.show()
plocha = window.get_surface()
pixle = sdl2.ext.PixelView(plocha)


class tlacidlo:
    def __init__(self, x, y, s, v, obr):
        self.x = x
        self.y = y
        self.s = s
        self.v = v
        self.obr = obr

    def kresli(self):
        r = sdl2.SDL_Rect()
        r.x = self.x + 1
        r.y = self.y + 1
        r.w, r.h = self.obr.w, self.obr.h
        sdl2.SDL_BlitSurface(self.obr, None, plocha, r)
        for xi in range(self.s):
            pixle[self.y][self.x + xi] = (0, 0, 0)
            pixle[self.y + self.v][self.x + xi] = (0, 0, 0)
        for yi in range(self.v):
            pixle[self.y + yi][self.x] = (0, 0, 0)
            pixle[self.y + yi][self.x + self.s] = (0, 0, 0)

    def zasah(self, x, y):
        return x > self.x and x < self.x + self.s and y > self.y and y < self.y + self.v


running = True
sdl2.ext.fill(plocha, sdl2.ext.Color(255, 255, 255))
window.refresh()
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                print("left")

                # obdĺžnik
                x = event.button.x
                y = event.button.y
                t1 = tlacidlo(x, y, 30, 30, img)
                t1.kresli()
                window.refresh()
            if event.button.button == sdl2.SDL_BUTTON_RIGHT:
                print("right")

sdl2.ext.quit()
