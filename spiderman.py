# spiderman_gl_360_conical_torso_reversed.py

import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# — Window & state —
win_w, win_h = 800, 600
rot_x = 15.0        # pitch
rot_y = 0.0         # yaw
mouse_down = False
mouse_x = mouse_y = 0
spin_enabled = True

def init():
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [2, 5, 5, 1])
    glClearColor(0.1, 0.1, 0.1, 1.0)

def draw_head():
    r = 0.40
    glColor3f(1, 0, 0)
    glutSolidSphere(r, 32, 32)

    # webbing
    glColor3f(0, 0, 0)
    glLineWidth(1)
    glBegin(GL_LINES)
    for deg in range(0, 360, 20):
        th = math.radians(deg)
        glVertex3f(0, 0, r)
        glVertex3f(r * math.cos(th) * 0.9, r * math.sin(th) * 0.9, r)
    glEnd()
    for ring in (0.15, 0.30):
        glBegin(GL_LINE_LOOP)
        for deg in range(0, 360, 10):
            th = math.radians(deg)
            glVertex3f(ring * math.cos(th), ring * math.sin(th), r)
        glEnd()

    # eyes
    for side, angle in ((1, +35), (-1, -35)):
        glPushMatrix()
        glTranslatef(0.20 * side, 0.08, r - 0.08)
        glRotatef(angle, 0, 0, 1)
        glScalef(1.0, 0.6, 1.0)
        glColor3f(1, 1, 1)
        glutSolidSphere(0.16, 16, 16)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.20 * side, 0.08, r - 0.04)
        glRotatef(angle, 0, 0, 1)
        glScalef(0.6, 0.3, 0.6)
        glColor3f(0, 0, 0)
        glutSolidSphere(0.10, 12, 12)
        glPopMatrix()

def draw_neck():
    quad = gluNewQuadric()
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0.55, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 0.18, 0.16, 0.15, 16, 4)
    glPopMatrix()

def draw_torso_and_emblem():
    quad = gluNewQuadric()

    # lower torso (blue): waist→legs, taper from 0.35 → 0.30
    glColor3f(0, 0, 1)
    glPushMatrix()
    glTranslatef(0, -0.70, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 0.35, 0.30, 0.8, 32, 4)
    glPopMatrix()

    # upper torso (red): shoulders→waist, taper from 0.40 → 0.35
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(0, -0.10, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 0.40, 0.35, 0.6, 32, 4)
    glPopMatrix()

    # spider emblem
    glPushMatrix()
    glTranslatef(0, 0.20, 0.38)
    glColor3f(0.2, 0.2, 0.2)
    glutSolidSphere(0.05, 16, 16)
    glLineWidth(2)
    glBegin(GL_LINES)
    for dx, dy in (
        ( 0.08,  0.10), ( 0.08, -0.10),
        (-0.08,  0.10), (-0.08, -0.10),
        ( 0.12,  0.00), (-0.12,  0.00)
    ):
        glVertex3f(0, 0, 0)
        glVertex3f(dx, dy, 0)
    glEnd()
    glPopMatrix()

def draw_limbs():
    quad = gluNewQuadric()
    # arms
    for x, ang in ((-0.5, -90), (0.5, 90)):
        # upper arm (blue)
        glColor3f(0, 0, 1)
        glPushMatrix()
        glTranslatef(x, 0.3, 0)
        glutSolidSphere(0.1, 16, 16)
        glRotatef(ang, 0, 1, 0)
        gluCylinder(quad, 0.1, 0.08, 0.7, 16, 4)
        glPopMatrix()
        # glove (red)
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(x, 0.3, 0)
        glRotatef(ang, 0, 1, 0)
        glTranslatef(0, 0, 0.7)
        glutSolidSphere(0.08, 12, 12)
        glPopMatrix()

    # legs
    for x in (-0.2, 0.2):
        # thigh (blue)
        glColor3f(0, 0, 1)
        glPushMatrix()
        glTranslatef(x, -0.6, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(quad, 0.11, 0.11, 1.2, 16, 4)
        glPopMatrix()
        # boot (red)
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(x, -0.6, 0)
        glRotatef(90, 1, 0, 0)
        glTranslatef(0, 0, 1.2)
        glutSolidSphere(0.12, 12, 12)
        glPopMatrix()

def draw_spiderman():
    draw_torso_and_emblem()
    draw_limbs()
    draw_neck()
    glPushMatrix()
    glTranslatef(0, 0.55 + 0.15 + 0.40, 0)
    draw_head()
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 1.5, 4,   0, 0.3, 0,   0, 1, 0)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    draw_spiderman()
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h or 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/(h or 1), 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global rot_x, rot_y, spin_enabled
    k = key.decode('utf-8').lower()
    if k == 'w':
        rot_x -= 5.0
    elif k == 's':
        rot_x += 5.0
    elif k == 'a':
        rot_y -= 5.0
    elif k == 'd':
        rot_y += 5.0
    elif k == 'o':
        spin_enabled = not spin_enabled
    glutPostRedisplay()

def mouse(btn, state, x, y):
    global mouse_down, mouse_x, mouse_y
    if btn == GLUT_LEFT_BUTTON:
        mouse_down = (state == GLUT_DOWN)
        mouse_x, mouse_y = x, y

def motion(x, y):
    global rot_x, rot_y, mouse_x, mouse_y
    if mouse_down:
        rot_y += (x - mouse_x) * 0.5
        rot_x += (y - mouse_y) * 0.5
        mouse_x, mouse_y = x, y
        glutPostRedisplay()

def idle():
    global rot_y
    if spin_enabled:
        rot_y = (rot_y + 0.2) % 360
        glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutCreateWindow(b"3D Spiderman - Suit Style")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()









