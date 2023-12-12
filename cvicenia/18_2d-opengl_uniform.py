#!/usr/bin/python3

"""18_2d-opengl_uniform.py: OpenGL v3.3 - nastavovanie farby kreslenia vo fragment shaderi prostrednictvom uniform premennej"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

import sys
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


def klavesnica_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:                 # klavesa Esc
        # zatvor okno
        glfw.set_window_should_close(window, True)


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

# nastav callback na klavesnicu
glfw.set_key_callback(okno, klavesnica_callback)

# nastav velkost okna pre OpenGL
glViewport(0, 0, 800, 600)


# definuj shadre
vertex_src = """
# version 330 core
in vec3 suradnica;
void main() {
    gl_Position = vec4(suradnica, 1.0);
}
"""

fragment_src = """
# version 330 core
out vec4 vysledna_farba;
uniform vec4 nasa_farba;
void main() {
    vysledna_farba = nasa_farba;
}
"""
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# priprav model a nahraj ho na GPU
vrcholy = np.array([ 0.5,  0.5, 0.0,
                     0.5, -0.5, 0.0,
                    -0.5, -0.5, 0.0,
                    -0.5,  0.5, 0.0], dtype=np.float32)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vrcholy.nbytes, vrcholy, GL_STATIC_DRAW)

indexy = np.array([ 0, 1, 3,    # 1. trojuholnik
                    1, 2, 3     # 2. trojuholnik
                  ], dtype=np.uint32)
ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexy.nbytes, indexy, GL_STATIC_DRAW)

# priprav VAO a nastav strukturu dat
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

suradnicaPrem = glGetAttribLocation(shader, "suradnica")
glVertexAttribPointer(suradnicaPrem, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
glEnableVertexAttribArray(suradnicaPrem)

nasaFarbaPrem = glGetUniformLocation(shader, "nasa_farba");
glUseProgram(shader)
glUniform4f(nasaFarbaPrem, 0.0, 0.5, 0.0, 1.0);

# sposob kreslenia
#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)   # GL_FILL

# event loop
while not glfw.window_should_close(okno):
    # vymaz obrazovku
    glClearColor(0.2, 0.3, 0.3, 1.0);
    glClear(GL_COLOR_BUFFER_BIT)
    # kresli
    glUseProgram(shader)
    #glBindVertexArray(vao)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glDrawElements(GL_TRIANGLES, len(indexy), GL_UNSIGNED_INT, None)
    # refreshni doublebuffer
    glfw.swap_buffers(okno)
    # sleduj udalosti a volaj nastavene callback funkcie
    glfw.poll_events()

# uvolni alokovane zdroje
glfw.terminate()

