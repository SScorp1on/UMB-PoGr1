#!/usr/bin/python3

"""18_9-opengl_sdl.py: Spojenie OpenGL s SDL"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

import sys
import ctypes
from OpenGL import GL, GLU
import sdl2


# https://github.com/syntonym/pysdl2/blob/master/examples/opengl.py

def run():
    # inicializacia SDL
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return -1

    # vytvorenie okna
    window = sdl2.SDL_CreateWindow(b"OpenGL demo",
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
                                   sdl2.SDL_WINDOW_OPENGL)
    if not window:
        print(sdl2.SDL_GetError())
        return -1

    # vytvorenie OpenGL kontextu
    context = sdl2.SDL_GL_CreateContext(window)

    # nastavenie premietania (ako to vsetko bude pouzivatel vidiet)
    GL.glMatrixMode(GL.GL_PROJECTION | GL.GL_MODELVIEW)
    GL.glLoadIdentity()
    GL.glOrtho(-400, 400, 300, -300, 0, 1)

    # pozicia modelu
    x = 0.0
    y = 30.0

    # SDL udalosti
    event = sdl2.SDL_Event()

    # jednoduchy event loop
    running = True
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False
        # vymaz obrazovku
        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        # cely model otocme
        GL.glRotatef(10.0, 0.0, 0.0, 1.0)
        # kresli trojuholnik
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glVertex2f(x, y + 90.0)
        GL.glColor3f(0.0, 1.0, 0.0)
        GL.glVertex2f(x + 90.0, y - 90.0)
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glVertex2f(x - 90.0, y - 90.0)
        GL.glEnd()
        # double-buffering
        sdl2.SDL_GL_SwapWindow(window)
        # chvilku pockaj
        sdl2.SDL_Delay(10)

    # uvolni alokovane prostriedky
    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())
