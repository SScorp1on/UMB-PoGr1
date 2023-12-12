#!/usr/bin/python3

"""18_5-opengl_wavefront.py: OpenGL - nacitanie 3D modelu zo suboru formatu wavefront"""
__author__ = "Michal Vagac"
__email__ = "michal.vagac@gmail.com"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def nacitaj_wavefront(nazov):
    vrcholy = []
    normaly = []
    plochy = []
    for riadok in open(nazov, "r"):
        if riadok.startswith('#'):
            continue
        hodnoty = riadok.split()
        if not hodnoty:
            continue
        if hodnoty[0] == 'v':
            v = list(map(float, hodnoty[1:4]))
            vrcholy.append(v)
        elif hodnoty[0] == 'vn':
            v = list(map(float, hodnoty[1:4]))
            normaly.append(v)
        elif hodnoty[0] == 'f':
            plocha = []
            normala = []
            for v in hodnoty[1:]:
                w = v.split('/')
                plocha.append(int(w[0]))
                if len(w) >= 3 and len(w[2]) > 0:
                    normala.append(int(w[2]))
                else:
                    normala.append(0)
            plochy.append((plocha, normala))
    return vrcholy, normaly, plochy


def kresli():
    # vymaz obrazovku a depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # cely model najprv otocme a potom posunme
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, -15.0, -70.0)
    glRotatef(35.0, 1.0, 1.0, 0.0);

    # kresli model (ulozeny ako list)
    glCallList(model)

    # vyprazdni vsetky buffre
    glFlush()


# inicializacia
glutInit(sys.argv)
glutInitWindowSize(640, 480)
glutCreateWindow(b'Priklad WaveFront objektu')
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
glColor3f(1.0, 1.0, 0.0)
glPointSize(4.0)

# nastavenie premietania (ako to vsetko bude pouzivatel vidiet)
glMatrixMode(GL_PROJECTION)  # nastav projection matrix (aby sme mohli nastavit projection)
glLoadIdentity()  # nastav ako aktualnu maticu jednotkovu maticu
gluPerspective(45.0, float(640) / 480, 1.0, 100.0);  # field of view, aspect ratio, zNear, zFar

# priprav model
vrcholy, normaly, plochy = nacitaj_wavefront('data/kos.obj')
model = glGenLists(1)  # vytvot novy model
glNewList(model, GL_COMPILE)  # len priprav, este nespustaj (GL prikazy)
glFrontFace(GL_CCW)  # plochy s poradim vrcholov v protismere hodinovych ruciciek (CCW) su brane ako predne (viditelne)
for plocha in plochy:
    vrcholy_plochy, normaly_plochy = plocha
    glBegin(GL_POLYGON)
    for i in range(len(vrcholy_plochy)):
        if normaly_plochy[i] > 0:
            glNormal3fv(normaly[normaly_plochy[i] - 1])
        glVertex3fv(vrcholy[vrcholy_plochy[i] - 1])
    glEnd()
glEndList()

# spusti main loop
glutMainLoop()
