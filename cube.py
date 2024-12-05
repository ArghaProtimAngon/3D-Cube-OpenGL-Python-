from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import numpy as np
import time
import numpy as np

angle = 0.0  # Initial rotation angle


def draw_points(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def findZone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):
        if dx >= 0:
            if dy >= 0:
                return x0, y0, x1, y1, 0
            else:
                return x0, -y0, x1, -y0, 7
        else:
            if dy >= 0:
                return -x0, y0, -x1, y1, 3
            else:
                return -x0, -y0, -x1, -y1, 4
    else:
        if dx >= 0:
            if dy >= 0:
                return y0, x0, y1, x1, 1
            else:
                return -y0, x0, -y1, x1, 6
        else:
            if dy >= 0:
                return y0, -x0, y1, -x1, 2
            else:
                return -y0, -x0, -y1, -x1, 5


def draw(x, y, zone):
    glPointSize(2)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    if zone == 0:
        glVertex2f(x, y)
    if zone == 1:
        glVertex2f(y, x)
    if zone == 2:
        glVertex2f(-y, x)
    if zone == 3:
        glVertex2f(-x, y)
    if zone == 4:
        glVertex2f(-x, -y)
    if zone == 5:
        glVertex2f(-y, -x)
    if zone == 6:
        glVertex2f(y, -x)
    if zone == 7:
        glVertex2f(x, -y)

    glEnd()


def draw_line(x0, y0, x1, y1):
    x0, y0, x1, y1, zone = findZone(x0, y0, x1, y1)
    dy = y1 - y0
    dx = x1 - x0
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x0
    y = y0
    draw(x, y, zone)
    while x <= x1:
        if d <= 0:
            x += 1
            d += dE
        else:
            x += 1
            y += 1
            d += dNE
        draw(x, y, zone)


def projection_plane_coordinate(given, Q, zp):
    matrix = np.array([[1, 0, -(Q[0] / Q[2]), zp * (Q[0] / Q[2])],
                       [0, 1, -(Q[1] / Q[2]), zp * (Q[1] / Q[2])],
                       [0, 0, -(zp / Q[2]), zp * (1 + (zp / Q[2]))],
                       [0, 0, -(1 / Q[2]), (1 + (zp / Q[2]))]])
    given = np.array(given)
    result = np.dot(matrix, given)
    x = result[0] / result[3]
    y = result[1] / result[3]
    z = result[2] / result[3]

    return (x, y, z)


def draw_cube(A, B, C, D, E, F, G, H):
    print(A, B, C, D, E, F, G, H)
    draw_line(A[0]+250, A[1]+250, B[0]+250, B[1]+250)
    draw_line(B[0]+250, B[1]+250, C[0]+250, C[1]+250)
    draw_line(C[0]+250, C[1]+250, D[0]+250, D[1]+250)
    draw_line(D[0], D[1], A[0], A[1])

    draw_line(A[0]+250, A[1]+250, E[0]+250, E[1]+250)
    draw_line(B[0]+250, B[1]+250, F[0]+250, F[1]+250)
    draw_line(C[0]+250, C[1]+250, G[0]+250, G[1]+250)
    draw_line(D[0]+250, D[1]+250, H[0]+250, H[1]+250)

    draw_line(E[0]+250, E[1]+250, F[0]+250, F[1]+250)
    draw_line(F[0]+250, F[1]+250, G[0]+250, G[1]+250)
    draw_line(G[0]+250, G[1]+250, H[0]+250, H[1]+250)
    draw_line(H[0]+250, H[1]+250, E[0]+250, E[1]+250)


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    A = (40, -40, 100, 1)
    B = (40, 40, 100, 1)
    C = (-40, 40, 100, 1)
    D = (-40, 40, 100, 1)
    E = (40, -40, 100, 1)
    F = (40, 40, 100, 1)
    G = (-40, 40, 100, 1)
    H = (-40, 40, 100, 1)
    Q = (20, 20, -50, 1)
    A = projection_plane_coordinate(A, Q, 0)
    B = projection_plane_coordinate(B, Q, 0)
    C = projection_plane_coordinate(C, Q, 0)
    D = projection_plane_coordinate(D, Q, 0)
    E = projection_plane_coordinate(E, Q, 0)
    F = projection_plane_coordinate(F, Q, 0)
    G = projection_plane_coordinate(G, Q, 0)
    H = projection_plane_coordinate(H, Q, 0)

    draw_cube(A, B, C, D, E, F, G, H)

    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutMainLoop()
