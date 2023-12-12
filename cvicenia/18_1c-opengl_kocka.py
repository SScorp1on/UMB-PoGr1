#!/usr/bin/python3

"""18_3-opengl_kocka.py: OpenGL - vykreslenie 3D kocky"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def kresli_model():
    glBegin(GL_LINES)
    for hrana in hrany:
        for vrchol in hrana:
            glVertex3fv(vrcholy[vrchol])
    glEnd()


def kresli():
    # vymaz obrazovku
    glClear(GL_COLOR_BUFFER_BIT)

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
glutCreateWindow(b'Priklad kocky')
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)  # nechceme double buffering a chceme farby
glutDisplayFunc(kresli)  # nastav funkciu, ktora sa zavola pri potrebe kreslenia

# nastav parametre kreslenia
glClearColor(1.0, 1.0, 1.0, 0.0)
glColor3f(1.0, 0.0, 0.0)
glPointSize(4.0)

# nastavenie premietania (ako to vsetko bude pouzivatel vidiet)
glMatrixMode(GL_PROJECTION)  # nastav projection matrix (aby sme mohli nastavit projection)
glLoadIdentity()  # nastav ako aktualnu maticu jednotkovu maticu
gluPerspective(45.0, float(640) / 480, 1.0, 1000.0);  # field of view, aspect ratio, zNear, zFar

# priprav model kocky
vrcholy = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)
hrany = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

# spusti main loop
glutMainLoop()
