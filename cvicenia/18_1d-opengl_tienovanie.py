#!/usr/bin/python3

"""18_4-opengl_tienovanie.py: OpenGL - vykreslenie vytienovanej 3D kocky, pouzitie depth buffera"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

# TODO nefunguje

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Bod:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Hrana:
    def __init__(self, bod1, bod2):
        if bod1.y < bod2.y:  # ideme od hora dole
            self.bod1 = bod1
            self.bod2 = bod2
        else:
            self.bod1 = bod2
            self.bod2 = bod1


class Trojuholnik:
    def __init__(self, hrana1, hrana2, hrana3, farba):
        self.hrany = [hrana1, hrana2, hrana3]
        self.farba = farba


class Plocha:
    def __init__(self, v1, v2, v3, farba):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.farba = farba


class Objekt:
    vrcholy = []
    plochy = []

    def pridaj_vrchol(self, v):
        self.vrcholy.append(v)

    def pridaj_plochu(self, p):
        self.plochy.append(p)


def normala(plocha):
    # vypocitaj normalu plochy
    a = model.vrcholy[plocha.v2] - model.vrcholy[plocha.v1]
    b = model.vrcholy[plocha.v3] - model.vrcholy[plocha.v2]
    n = np.array([a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]])
    return n


def kresli_model():
    glFrontFace(
        GL_CCW)  # plochy s poradim vrcholov v protismere hodinovych ruciciek (CCW) su brane ako predne (viditelne)
    for plocha in model.plochy:
        # vrcholy_plochy, normaly_plochy = plocha
        glBegin(GL_POLYGON)
        n = normala(plocha)
        # vrchol 1
        glNormal3fv(n)
        glVertex3i(*model.vrcholy[plocha.v1][0:3])
        # vrchol 2
        glNormal3fv(n)
        glVertex3i(*model.vrcholy[plocha.v2][0:3])
        # vrchol 3
        glNormal3fv(n)
        glVertex3i(*model.vrcholy[plocha.v3][0:3])
        # for i in range(len(vrcholy_plochy)):
        #    if normaly_plochy[i] > 0:
        #        glNormal3fv(normaly[normaly_plochy[i] - 1])
        #    glVertex3fv(vrcholy[vrcholy_plochy[i] - 1])
        glEnd()


# glBegin(GL_LINES)
#    for hrana in hrany:
#        for vrchol in hrana:
#            glVertex3fv(vrcholy[vrchol])
#    glEnd()

def kresli():
    # vymaz obrazovku a depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # cely model najprv otocme a potom posunme
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)
    glRotatef(35.0, 1.0, 0.0, 0.0);

    # kresli model
    kresli_model()

    # vyprazdni vsetky buffre
    glFlush()


# inicializacia
glutInit(sys.argv)
glutInitWindowSize(640, 480)
glutCreateWindow(b'Priklad vytienovanej kocky')
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)  # nechceme double buffering a chceme farby
glutDisplayFunc(kresli)  # nastav funkciu, ktora sa zavola pri potrebe kreslenia
glShadeModel(GL_SMOOTH)  # nastav sposob tienovania
glEnable(GL_DEPTH_TEST)  # zapni depth buffer
glDepthFunc(GL_LESS)  # sposob prace s depth bufferom
glEnable(GL_COLOR_MATERIAL)  # povol farbu ako material

# nastav parametre svetla
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLight(GL_LIGHT0, GL_POSITION, (100, 100, 0, 1))
glLight(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 0.4))
glLight(GL_LIGHT0, GL_DIFFUSE, (0.4, 0.4, 0.4, 0.4))
glLight(GL_LIGHT0, GL_SPECULAR, (0.4, 0.4, 0.4, 0.4))

# nastav parametre kreslenia
glClearColor(1.0, 1.0, 1.0, 0.0)
glColor3f(1.0, 0.0, 0.0)
glPointSize(4.0)

# nastavenie premietania (ako to vsetko bude pouzivatel vidiet)
glMatrixMode(GL_PROJECTION)  # nastav projection matrix (aby sme mohli nastavit projection)
glLoadIdentity()  # nastav ako aktualnu maticu jednotkovu maticu
gluPerspective(45.0, float(640) / 480, 1.0, 1000.0);  # field of view, aspect ratio, zNear, zFar

# priprav model kocky
model = Objekt()
model.pridaj_vrchol(np.array([-50, -50, 100, 1]))
model.pridaj_vrchol(np.array([50, -50, 100, 1]))
model.pridaj_vrchol(np.array([50, 50, 100, 1]))
model.pridaj_vrchol(np.array([-50, 50, 100, 1]))
model.pridaj_vrchol(np.array([-50, -50, 150, 1]))
model.pridaj_vrchol(np.array([50, -50, 150, 1]))
model.pridaj_vrchol(np.array([50, 50, 150, 1]))
model.pridaj_vrchol(np.array([-50, 50, 150, 1]))
model.pridaj_plochu(Plocha(0, 1, 2, (255, 255, 255)))
model.pridaj_plochu(Plocha(0, 2, 3, (255, 255, 255)))
model.pridaj_plochu(Plocha(0, 5, 1, (255, 255, 255)))
model.pridaj_plochu(Plocha(0, 4, 5, (255, 255, 255)))
model.pridaj_plochu(Plocha(3, 6, 7, (255, 255, 255)))
model.pridaj_plochu(Plocha(3, 2, 6, (255, 255, 255)))
model.pridaj_plochu(Plocha(0, 7, 4, (255, 255, 255)))
model.pridaj_plochu(Plocha(0, 3, 7, (255, 255, 255)))
model.pridaj_plochu(Plocha(1, 5, 6, (255, 255, 255)))
model.pridaj_plochu(Plocha(1, 6, 2, (255, 255, 255)))
model.pridaj_plochu(Plocha(4, 6, 5, (255, 255, 255)))
model.pridaj_plochu(Plocha(4, 7, 6, (255, 255, 255)))

# spusti main loop
glutMainLoop()
