#!/usr/bin/python3

"""18_1-opengl_kreslenie.py: Priklad prace s OpenGL kniznicou - vykreslenie zakladnych tvarov v orthographic premietani"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

# jedno z:
#   apt-get install python3-opengl
#   pip3 install PyOpenGL
# windows:
#   https://stackoverflow.com/questions/65699670/pyopengl-opengl-error-nullfunctionerror-attempt-to-call-an-undefined-functio
#   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl

# import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def kresli():
    # vymaz obrazovku
    glClear(GL_COLOR_BUFFER_BIT)

    # kresli par bodiek
    glBegin(GL_POINTS)
    glVertex2i(10, 10)
    glVertex2i(100, 50)
    glVertex3f(130.0, 100.0, 0.0)
    glEnd()

    # kresli dake modre ciary
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex2i(10, 10)
    glVertex2i(100, 50)
    glVertex2i(100, 50)
    glVertex3f(130.0, 100.0, 0.0)
    glEnd()

    # kresli cerveny trojuholnik
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2i(30, 90)
    glVertex2i(130, 120)
    glVertex2i(80, 200)
    glEnd()

    # vyprazdni vsetky buffre
    glFlush()


# inicializacia
glutInit(sys.argv)
glutInitWindowSize(320, 240)
glutCreateWindow(b'Priklad kreslenia')
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)  # nechceme double buffering a chceme farby
glutDisplayFunc(kresli)  # nastav funkciu, ktora sa zavola pri potrebe kreslenia

# nastav parametre kreslenia
glClearColor(1.0, 1.0, 1.0, 0.0)
glColor3f(0.0, 0.0, 0.0)
glPointSize(4.0)

# nastavenie premietania (ako to vsetko bude pouzivatel vidiet)
glMatrixMode(GL_PROJECTION)  # nastav projection matrix mode (dalsia praca s maticami sa bude tykat premietania)
glLoadIdentity()  # nastav ako aktualnu maticu jednotkovu maticu
gluOrtho2D(0.0, 320.0, 0.0, 240.0)  # nastav Orthographic premietanie

# spusti main loop
glutMainLoop()
