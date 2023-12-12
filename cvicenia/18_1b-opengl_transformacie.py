#!/usr/bin/python3

"""18_2-opengl_transformacie.py: OpenGL - vykreslenie otoceneho polygonu v perspektive"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def kresli():
    # vymaz obrazovku
    glClear(GL_COLOR_BUFFER_BIT)

    # cely "model" najprv otocme a potom posunme (ide to v opacnom poradi!)
    glMatrixMode(GL_MODELVIEW)  # nastav modelview matrix mode (dalsia praca s maticami sa bude tykat modelu a nasho pohladu nan)
    glLoadIdentity()  # pri kazdom dalsom vykreslovani chceme zacinat transformacie odznova (aby sme dostali vysledok) => nastav jednotkovu maticu
    glTranslatef(0.0, 0.0, -10.0)  # prenasob aktualnu maticu maticou posunutia
    glRotatef(45.0, 0.0, 0.0, 1.0);  # uhol, x, y, z
    glRotatef(35.0, 1.0, 0.0, 0.0);  # uhol, x, y, z

    # kresli polygon
    glBegin(GL_POLYGON)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(-1.0, 1.0, 0.0);
    glVertex3f(-1.0, -1.0, 0.0);
    glVertex3f(1.0, -1.0, 0.0);
    glEnd()

    # vyprazdni vsetky buffre
    glFlush()


# inicializacia
glutInit(sys.argv)
glutInitWindowSize(640, 480)
glutCreateWindow(b'Priklad transformacie')
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

# spusti main loop
glutMainLoop()
