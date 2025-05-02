from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# — Globals —
camera_pos = [0, 200, 500]
GRID_SIZE  = 600   # half-width of your city
BLOCK_SIZE = 200   # distance between avenues/cross-streets
WIN_W, WIN_H = 1000, 800

# — 3D City Elements —
def draw_streets_and_sidewalks():
    # Dark asphalt roads every BLOCK_SIZE
    glColor3f(0.05, 0.05, 0.05)
    for i in range(-3, 4):
        y = i * BLOCK_SIZE
        glBegin(GL_QUADS)
        glVertex3f(-GRID_SIZE, y-10, 0)
        glVertex3f( GRID_SIZE, y-10, 0)
        glVertex3f( GRID_SIZE, y+10, 0)
        glVertex3f(-GRID_SIZE, y+10, 0)
        glEnd()
    for i in range(-3, 4):
        x = i * BLOCK_SIZE
        glBegin(GL_QUADS)
        glVertex3f(x-10, -GRID_SIZE, 0)
        glVertex3f(x+10, -GRID_SIZE, 0)
        glVertex3f(x+10,  GRID_SIZE, 0)
        glVertex3f(x-10,  GRID_SIZE, 0)
        glEnd()

    # Sidewalks right up against the roads
    glColor3f(0.2,0.2,0.2)
    for i in range(-3,4):
        y = i*BLOCK_SIZE
        for off in (+10,-20):
            glBegin(GL_QUADS)
            glVertex3f(-GRID_SIZE, y+off,     0.01)
            glVertex3f( GRID_SIZE, y+off,     0.01)
            glVertex3f( GRID_SIZE, y+off+10,  0.01)
            glVertex3f(-GRID_SIZE, y+off+10,  0.01)
            glEnd()
    for i in range(-3,4):
        x = i*BLOCK_SIZE
        for off in (+10,-20):
            glBegin(GL_QUADS)
            glVertex3f(x+off,    -GRID_SIZE, 0.01)
            glVertex3f(x+off,     GRID_SIZE, 0.01)
            glVertex3f(x+off+10,  GRID_SIZE, 0.01)
            glVertex3f(x+off+10, -GRID_SIZE, 0.01)
            glEnd()

def draw_buildings():
    # Exactly one building per 200×200 block, between the roads:
    # 6 blocks per axis, from -600 to +600
    for i in range(-3, 3):
        for j in range(-3, 3):
            # center of the block
            cx = (i + 0.5) * BLOCK_SIZE
            cy = (j + 0.5) * BLOCK_SIZE

            w = 120
            h = random.uniform(180, 300)

            # Building block
            glPushMatrix()
            glTranslatef(cx, cy, h/2)
            glScalef(w, w, h)
            glColor3f(0.2, 0.2, 0.2)
            glutSolidCube(1.0)
            glPopMatrix()

            # Windows front/back/left/right
            glColor3f(1,1,0)
            glPointSize(2)
            glBegin(GL_POINTS)
            # front face
            for wx in range(-w//2+8, w//2-8, 16):
                for wz in range(10, int(h)-10, 30):
                    glVertex3f(cx+wx, cy - w/2 - 0.02, wz)
            # back face
            for wx in range(-w//2+8, w//2-8, 16):
                for wz in range(10, int(h)-10, 30):
                    glVertex3f(cx+wx, cy + w/2 + 0.02, wz)
            # left face
            for wy in range(-w//2+8, w//2-8, 16):
                for wz in range(10, int(h)-10, 30):
                    glVertex3f(cx - w/2 - 0.02, cy+wy, wz)
            # right face
            for wy in range(-w//2+8, w//2-8, 16):
                for wz in range(10, int(h)-10, 30):
                    glVertex3f(cx + w/2 + 0.02, cy+wy, wz)
            glEnd()

def draw_lamps_and_signs():
    for i in range(-3,4):
        for j in range(-3,4):
            x, y = i*BLOCK_SIZE-10, j*BLOCK_SIZE-10
            # lamp post
            glColor3f(0.8,0.8,0.2)
            glLineWidth(3)
            glBegin(GL_LINES)
            glVertex3f(x,y,0); glVertex3f(x,y,60)
            glEnd()
            # lamp head
            glColor3f(1,1,0)
            glPointSize(5)
            glBegin(GL_POINTS)
            glVertex3f(x,y,60)
            glEnd()
            # traffic light
            glColor3f((i+j)%2,0,0)
            glBegin(GL_QUADS)
            glVertex3f(x+15,y+15,20)
            glVertex3f(x+20,y+15,20)
            glVertex3f(x+20,y+20,30)
            glVertex3f(x+15,y+20,30)
            glEnd()

    # neon billboard
    glColor3f(0,0.8,1)
    glBegin(GL_QUADS)
    glVertex3f(-300,300,220)
    glVertex3f(-100,300,220)
    glVertex3f(-100,350,270)
    glVertex3f(-300,350,270)
    glEnd()

def draw_park():
    glColor3f(0,0.4,0)
    glBegin(GL_QUADS)
    glVertex3f(-100,-100,0)
    glVertex3f( 100,-100,0)
    glVertex3f( 100, 100,0)
    glVertex3f(-100, 100,0)
    glEnd()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(75, WIN_W/WIN_H, 1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*camera_pos, 0,0,0, 0,0,1)

def showScreen():
    glClearColor(0.0,0.0,0.05,1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    setupCamera()
    draw_streets_and_sidewalks()
    draw_buildings()
    draw_lamps_and_signs()
    draw_park()

    # UI overlay
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    gluOrtho2D(0,WIN_W,0,WIN_H)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glColor3f(0.6,0.6,0.6)
    def quad(x0,y0,x1,y1):
        glBegin(GL_QUADS)
        glVertex2f(x0,y0); glVertex2f(x1,y0)
        glVertex2f(x1,y1); glVertex2f(x0,y1)
        glEnd()
    quad(50,50,140,80)
    quad(50,100,140,130)
    glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)

    glutSwapBuffers()

def keyboardListener(key,x,y):
    step=20
    if key==b'w': camera_pos[2]-=step
    elif key==b's': camera_pos[2]+=step
    elif key==b'a': camera_pos[0]-=step
    elif key==b'd': camera_pos[0]+=step
    elif key==b'q': camera_pos[1]+=step
    elif key==b'e': camera_pos[1]-=step
    glutPostRedisplay()

def mouse_click(button,state,x,y):
    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
        yi = WIN_H - y; step=20
        if   50 < x < 140 and  50 < yi <  80: camera_pos[2]-=step
        elif 50 < x < 140 and 100 < yi < 130: camera_pos[2]+=step
        glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
    glutInitWindowSize(WIN_W,WIN_H)
    glutCreateWindow(b"Spider-Man's City")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouse_click)
    glutMainLoop()

if __name__=="__main__":
    main()
