#!/usr/bin/python3

"""18_2k-opengl_kamera.py: OpenGL v3.3 - kamera, posuvanie sa klavesnicou, otacanie sa mysou, zoomovanie kolieskom"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

import sys

import glfw
import numpy as np
import pyrr
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image

SIRKA = 800
VYSKA = 600
KAMERA_RYCHLOST = 2.5
KAMERA_CITLIVOST = 0.1

def klavesnica_callback(okno, key, scancode, action, mode):
    global deltaFrame
    global kameraPoz, kameraDopredu, kameraHore
    stlacene = False
    if glfw.get_key(okno, glfw.KEY_W) == glfw.PRESS:
        kameraPoz += kameraDopredu * (KAMERA_RYCHLOST * deltaFrame)
        stlacene = True
    if glfw.get_key(okno, glfw.KEY_S) == glfw.PRESS:
        kameraPoz -= kameraDopredu * (KAMERA_RYCHLOST * deltaFrame)
        stlacene = True
    if glfw.get_key(okno, glfw.KEY_A) == glfw.PRESS:
        kameraPoz -= pyrr.vector.normalise(pyrr.vector3.cross(kameraDopredu, kameraHore)) * (KAMERA_RYCHLOST * deltaFrame)
        stlacene = True
    if glfw.get_key(okno, glfw.KEY_D) == glfw.PRESS:
        kameraPoz += pyrr.vector.normalise(pyrr.vector3.cross(kameraDopredu, kameraHore)) * (KAMERA_RYCHLOST * deltaFrame)
        stlacene = True
    if stlacene:
        kamera = pyrr.matrix44.create_look_at(kameraPoz, kameraPoz + kameraDopredu, kameraHore)
        kameraPrem = glGetUniformLocation(shader, "kamera")
        glUniformMatrix4fv(kameraPrem, 1, GL_FALSE, kamera)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:             # klavesa Esc
        # zatvor okno
        glfw.set_window_should_close(okno, True)

def mys_pohyb_callback(okno, xpos, ypos):
    global lastX, lastY
    global yaw, pitch
    global kameraPoz, kameraDopredu, kameraHore

    if lastX is None:
        lastX = xpos
    if lastY is None:
        lastY = ypos

    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos

    xoffset *= KAMERA_CITLIVOST
    yoffset *= KAMERA_CITLIVOST

    yaw   += xoffset
    pitch += yoffset

    if pitch > 89.0:
        pitch =  89.0
    if pitch < -89.0:
        pitch = -89.0

    smer = pyrr.Vector3([0.0, 0.0, 3.0])
    smer.x = np.cos(np.radians(yaw)) * np.cos(np.radians(pitch));
    smer.y = np.sin(np.radians(pitch));
    smer.z = np.sin(np.radians(yaw)) * np.cos(np.radians(pitch));

    kameraDopredu = pyrr.vector.normalise(smer)

    kamera = pyrr.matrix44.create_look_at(kameraPoz, kameraPoz + kameraDopredu, kameraHore)
    kameraPrem = glGetUniformLocation(shader, "kamera")
    glUniformMatrix4fv(kameraPrem, 1, GL_FALSE, kamera)

def mys_koliecko_callback(okno, xoffset, yoffset):
    global fov
    fov -= yoffset
    if fov < 1.0:
        fov = 1.0
    if fov > 45.0:
        fov = 45.0
    premietanie = pyrr.matrix44.create_perspective_projection_matrix(fov, SIRKA/VYSKA, 0.1, 100)
    premietaniePrem = glGetUniformLocation(shader, "premietanie")
    glUniformMatrix4fv(premietaniePrem, 1, GL_FALSE, premietanie)


# inicializacia glfw
if not glfw.init():
    sys.exit(1)

# profil
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
#glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)              # Mac OS X

# vytvor a zobraz okno
okno = glfw.create_window(SIRKA, VYSKA, "Priklad Opengl GLFW okna", None, None)
if not okno:
    glfw.terminate()
    sys.exit(1)
glfw.make_context_current(okno)

# nastav callback na klavesnicu
glfw.set_key_callback(okno, klavesnica_callback)

# nastav callback na mys
glfw.set_cursor_pos_callback(okno, mys_pohyb_callback)
glfw.set_scroll_callback(okno, mys_koliecko_callback)
glfw.set_input_mode(okno, glfw.CURSOR, glfw.CURSOR_DISABLED)        # skry kurzor mysi
lastX, lastY = None, None
yaw = -90.0
pitch = 0.0

# nastav velkost okna pre OpenGL
glViewport(0, 0, SIRKA, VYSKA)


# definuj shadre
vertex_src = """
# version 330 core
//in vec3 suradnica;
//in vec3 farba;
//in vec2 textura;
layout(location = 0) in vec3 suradnica;
layout(location = 1) in vec3 farba;
layout(location = 2) in vec2 textura;
out vec3 farba2;
out vec2 textura2;
uniform mat4 model;
uniform mat4 kamera;
uniform mat4 premietanie;
void main() {
    gl_Position = premietanie * kamera * model * vec4(suradnica, 1.0);
    farba2 = farba;
    textura2 = textura;
}
"""

fragment_src = """
# version 330 core
out vec4 vysledna_farba;
in vec3 farba2;
in vec2 textura2;
uniform sampler2D texturaSampler;
void main() {
    //vysledna_farba = vec4(farba2, 1.0);
    //vysledna_farba = texture(texturaSampler, textura2);
    vysledna_farba = texture(texturaSampler, textura2) * vec4(farba2, 1.0);
}
"""
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# priprav model a nahraj ho na GPU
#                   pozicia         farba           textura
vrcholy = np.array([ 0.5,  0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0,   # 0
                     0.5, -0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0,   # 1
                    -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 0.0,   # 2
                    -0.5,  0.5, -0.5, 1.0, 0.0, 1.0, 0.0, 1.0,   # 3
                     0.5,  0.5,  0.5, 1.0, 0.0, 0.0, 1.0, 1.0,   # 4
                     0.5, -0.5,  0.5, 0.0, 1.0, 0.0, 1.0, 0.0,   # 5
                    -0.5, -0.5,  0.5, 0.0, 0.0, 1.0, 0.0, 0.0,   # 6
                    -0.5,  0.5,  0.5, 1.0, 0.0, 1.0, 0.0, 1.0    # 7
                    ], dtype=np.float32)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vrcholy.nbytes, vrcholy, GL_STATIC_DRAW)

indexy = np.array([ 0, 1, 3,
                    1, 2, 3,
                    4, 5, 7,
                    5, 6, 7
                  ], dtype=np.uint32)
ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexy.nbytes, indexy, GL_STATIC_DRAW)

# priprav VAO a nastav strukturu dat
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

suradnicaPrem = 0#glGetAttribLocation(shader, "suradnica")
glVertexAttribPointer(suradnicaPrem, 3, GL_FLOAT, GL_FALSE, 8*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
glEnableVertexAttribArray(suradnicaPrem)

farbaPrem = 1#glGetAttribLocation(shader, "farba")
glVertexAttribPointer(farbaPrem, 3, GL_FLOAT, GL_FALSE, 8*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3*ctypes.sizeof(ctypes.c_float)))
glEnableVertexAttribArray(farbaPrem)

texturaPrem = 2#glGetAttribLocation(shader, "textura")
glVertexAttribPointer(texturaPrem, 2, GL_FLOAT, GL_FALSE, 8*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(6*ctypes.sizeof(ctypes.c_float)))
glEnableVertexAttribArray(texturaPrem)

# textura
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)        # wrap param s
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)        # wrap param t
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)    # filter param
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)    # filter param
image = Image.open("../images/circle30.png")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()
# img_data = np.array(image.getdata(), np.uint8) # second way of getting the raw image data
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
#glGenerateMipmap(GL_TEXTURE_2D)

# transformacia suradnic
glUseProgram(shader)
# model matrix - umiestnenie modelu vo svete
model = pyrr.Matrix44.from_x_rotation(np.radians(55))
# view matrix - posunutie kamery dozadu = posunutie sveta dopredu
kameraPoz = pyrr.Vector3([0.0, 0.0, 3.0])
kameraDopredu = pyrr.Vector3([0, 0, -1])
kameraHore = pyrr.Vector3([0, 1, 0])
kamera = pyrr.matrix44.create_look_at(kameraPoz, kameraPoz + kameraDopredu, kameraHore)
# projection matrix - premietanu
#premietanie = pyrr.matrix44.create_orthogonal_projection_matrix(0, 1280, 0, 720, -1000, 1000)
fov = 45.0
premietanie = pyrr.matrix44.create_perspective_projection_matrix(fov, SIRKA/VYSKA, 0.1, 100)
# nastav matice do vertex shadera
modelPrem = glGetUniformLocation(shader, "model")
glUniformMatrix4fv(modelPrem, 1, GL_FALSE, model)
kameraPrem = glGetUniformLocation(shader, "kamera")
glUniformMatrix4fv(kameraPrem, 1, GL_FALSE, kamera)
premietaniePrem = glGetUniformLocation(shader, "premietanie")
glUniformMatrix4fv(premietaniePrem, 1, GL_FALSE, premietanie)

objekty = [ pyrr.Vector3([0, 0, -3]), pyrr.Vector3([3, 0, -4]), pyrr.Vector3([-1, 0, -2.5]) ]

# povol z-buffer
glEnable(GL_DEPTH_TEST)

# sposob kreslenia
#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)   # GL_FILL

aktualnyFrame, predoslyFrame = 0.1, 0.0

# event loop
while not glfw.window_should_close(okno):
    # vymaz obrazovku
    glClearColor(0.2, 0.3, 0.3, 1.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # sprav viac kopii objektu (vykresli ho viac krat na roznych suradniciach)
    for o in objekty:
        model = pyrr.matrix44.multiply(pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time()), pyrr.matrix44.create_from_translation(o))
        modelPrem = glGetUniformLocation(shader, "model")
        glUniformMatrix4fv(modelPrem, 1, GL_FALSE, model)
        # kresli
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glDrawElements(GL_TRIANGLES, len(indexy), GL_UNSIGNED_INT, None)
    # refreshni doublebuffer
    glfw.swap_buffers(okno)
    # sleduj udalosti a volaj nastavene callback funkcie
    glfw.poll_events()
    # casovanie
    aktualnyFrame = glfw.get_time()
    deltaFrame = aktualnyFrame - predoslyFrame
    predoslyFrame = aktualnyFrame

# uvolni alokovane zdroje
glfw.terminate()

