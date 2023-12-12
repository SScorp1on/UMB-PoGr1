#!/usr/bin/python3

"""18_2a-opengl_okno.py: Priklad prace s OpenGL v3.3 - vytvorenie okna"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

# jedno z:
#   apt-get install python3-opengl glfw
#   pip3 install PyOpenGL

import sys
import glfw
from OpenGL.GL import *


# inicializacia glfw
if not glfw.init():
    sys.exit(1)

# profil
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
#glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)              # Mac OS X

# vytvor a zobraz okno
okno = glfw.create_window(800, 600, "Priklad Opengl GLFW okna", None, None)
if not okno:
    glfw.terminate()
    sys.exit(1)
glfw.make_context_current(okno)

# nastav velkost okna pre OpenGL
glViewport(0, 0, 800, 600)

# event loop
while not glfw.window_should_close(okno):
    # kresli (vymaz obrazovku)
    glClearColor(0.2, 0.3, 0.3, 1.0);
    glClear(GL_COLOR_BUFFER_BIT)
    # refreshni doublebuffer
    glfw.swap_buffers(okno)
    # sleduj udalosti a volaj nastavene callback funkcie
    glfw.poll_events()

# uvolni alokovane zdroje
glfw.terminate()

