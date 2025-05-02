from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
# — Globals —
GRID_SIZE = 600  # half-width of your city
BLOCK_SIZE = 200  # distance between avenues/cross-streets
WIN_W, WIN_H = 1000, 800
camera_angle = 0        # horizontal orbit angle (degrees)
camera_radius = 900     # distance from center
camera_height = 700     # height above ground
city_rotation = 0  # degrees
# Global variable to control car movement
car_position = -GRID_SIZE  # Starting position on the x-axis


# Predefined building heights for each block
building_heights = [[0 for _ in range(6)] for _ in range(6)]
for i in range(6):
    for j in range(6):
        # Create a pattern of heights - taller buildings in center, shorter at edges
        distance_from_center = max(abs(i - 2.5), abs(j - 2.5))
        base_height = 100 + (3 - distance_from_center) * 60
        # Add some random variation
        building_heights[i][j] = base_height + random.uniform(-20, 20)


# — 3D City Elements —
def draw_streets_and_sidewalks():
    # Dark asphalt roads every BLOCK_SIZE
    glColor3f(0.05, 0.05, 0.05)
    for i in range(-3, 4):
        y = i * BLOCK_SIZE
        glBegin(GL_QUADS)
        glVertex3f(-GRID_SIZE, y - 15, 0)
        glVertex3f(GRID_SIZE, y - 15, 0)
        glVertex3f(GRID_SIZE, y + 15, 0)
        glVertex3f(-GRID_SIZE, y + 15, 0)
        glEnd()
    for i in range(-3, 4):
        x = i * BLOCK_SIZE
        glBegin(GL_QUADS)
        glVertex3f(x - 15, -GRID_SIZE, 0)
        glVertex3f(x + 15, -GRID_SIZE, 0)
        glVertex3f(x + 15, GRID_SIZE, 0)
        glVertex3f(x - 15, GRID_SIZE, 0)
        glEnd()

    # Green grass areas between roads and buildings
    glColor3f(0.06, 0.2, 0.1)  # Bright green grass color
    for i in range(-3, 3):
        for j in range(-3, 3):
            # Draw grass in the middle of each block
            cx = (i + 0.5) * BLOCK_SIZE
            cy = (j + 0.5) * BLOCK_SIZE
            size = BLOCK_SIZE - 30  # Leave space for sidewalks

            glBegin(GL_QUADS)
            glVertex3f(cx - size / 2, cy - size / 2, 0.001)
            glVertex3f(cx + size / 2, cy - size / 2, 0.001)
            glVertex3f(cx + size / 2, cy + size / 2, 0.001)
            glVertex3f(cx - size / 2, cy + size / 2, 0.001)
            glEnd()

    # Sidewalks right up against the roads
    glColor3f(0.4, 0.4, 0.4)  # Lighter gray for sidewalks
    for i in range(-3, 4):
        y = i * BLOCK_SIZE
        for off in (+15, -25):  # Adjusted offsets
            glBegin(GL_QUADS)
            glVertex3f(-GRID_SIZE, y + off, 0.01)
            glVertex3f(GRID_SIZE, y + off, 0.01)
            glVertex3f(GRID_SIZE, y + off + 10, 0.01)
            glVertex3f(-GRID_SIZE, y + off + 10, 0.01)
            glEnd()
    for i in range(-3, 4):
        x = i * BLOCK_SIZE
        for off in (+15, -25):  # Adjusted offsets
            glBegin(GL_QUADS)
            glVertex3f(x + off, -GRID_SIZE, 0.01)
            glVertex3f(x + off, GRID_SIZE, 0.01)
            glVertex3f(x + off + 10, GRID_SIZE, 0.01)
            glVertex3f(x + off + 10, -GRID_SIZE, 0.01)
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
            h = building_heights[i + 3][j + 3]  # Use predefined height

            # Building block
            glPushMatrix()
            glTranslatef(cx, cy, h / 2)
            glScalef(w, w, h)

            # Different colors for different height ranges
            if h < 150:
                glColor3f(0.3, 0.3, 0.4)  # Blue-gray for shorter buildings
            elif h < 220:
                glColor3f(0.4, 0.3, 0.3)  # Reddish for medium buildings
            else:
                glColor3f(0.15, 0.2, 0.2)  # Dark for tall buildings

            glutSolidCube(1.0)
            glPopMatrix()

            # Windows front/back/left/right
            window_color = (1, 1, 0.9) if h > 180 else (1, 1, 0.9)
            glColor3f(*window_color)
            glPointSize(2)
            glBegin(GL_POINTS)
            # front face
            for wx in range(-w // 2 + 8, w // 2 - 8, 16):
                for wz in range(10, int(h) - 10, 30):
                    glVertex3f(cx + wx, cy - w / 2 - 0.02, wz)
            # back face
            for wx in range(-w // 2 + 8, w // 2 - 8, 16):
                for wz in range(10, int(h) - 10, 30):
                    glVertex3f(cx + wx, cy + w / 2 + 0.02, wz)
            # left face
            for wy in range(-w // 2 + 8, w // 2 - 8, 16):
                for wz in range(10, int(h) - 10, 30):
                    glVertex3f(cx - w / 2 - 0.02, cy + wy, wz)
            # right face
            for wy in range(-w // 2 + 8, w // 2 - 8, 16):
                for wz in range(10, int(h) - 10, 30):
                    glVertex3f(cx + w / 2 + 0.02, cy + wy, wz)
            glEnd()



def draw_car(x, y):
    # Car body (a simple cube)
    glColor3f(0.8, 0.2, 0.2)  # Red color for the car body
    glPushMatrix()
    glTranslatef(x, y, 10)  # Position the car above the ground
    glScalef(1, 1, 0.5)  # Make the car flatter
    glutSolidCube(30)  # Body of the car
    glPopMatrix()

    # Wheels (four simple cylinders)
    wheel_radius = 8
    wheel_offset = 12

    glColor3f(0, 0, 0)  # Black for the wheels

    # Draw wheels
    for dx in [-wheel_offset, wheel_offset]:
        for dy in [-wheel_offset, wheel_offset]:
            glPushMatrix()
            glTranslatef(x + dx, y + dy, 5)  # Position the wheel
            gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, 5, 16, 16)  # Draw the wheel
            glPopMatrix()

# Update car position over time (this function is called every frame)
def update_car_position():
    global car_position
    car_position += 0.5  # Speed of the car
    if car_position > GRID_SIZE:  # If the car moves past the right side, reset to the left
        car_position = -GRID_SIZE

def draw_lamps_and_signs():
    for i in range(-3, 4):
        for j in range(-3, 4):
            x, y = i * BLOCK_SIZE - 10, j * BLOCK_SIZE - 10
            # lamp post
            glColor3f(0.8, 0.8, 0.6)
            glLineWidth(3)
            glBegin(GL_LINES)
            glVertex3f(x, y, 0);
            glVertex3f(x, y, 60)
            glEnd()
            # lamp head
            glColor3f(1, 1, 0)
            glPointSize(5)
            glBegin(GL_POINTS)
            glVertex3f(x, y, 60)
            glEnd()
            # traffic light
            glColor3f((i + j) % 2, 0, 0)
            glBegin(GL_QUADS)
            glVertex3f(x + 15, y + 15, 20)
            glVertex3f(x + 20, y + 15, 20)
            glVertex3f(x + 20, y + 20, 30)
            glVertex3f(x + 15, y + 20, 30)
            glEnd()




def draw_park():
    glColor3f(0, 0.5, 0)
    glBegin(GL_QUADS)
    glVertex3f(-100, -100, 0)
    glVertex3f(100, -100, 0)
    glVertex3f(100, 100, 0)
    glVertex3f(-100, 100, 0)
    glEnd()


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(75, WIN_W / WIN_H, 1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    rad = math.radians(camera_angle)
    eye_x = camera_radius * math.sin(rad)
    eye_y = camera_radius * math.cos(rad)
    eye_z = camera_height

    gluLookAt(eye_x, eye_y, eye_z, 0, 0, 0, 0, 0, 1)

def showScreen():
    # Changed sky color to a darker blue
    glClearColor(0, 0.05, 0.25, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setupCamera()
    draw_streets_and_sidewalks()
    draw_buildings()
    draw_lamps_and_signs()
    draw_park()

    # Draw and animate the car
    draw_car(car_position, 0)  # Move the car along the x-axis (on the main road)

    # Update car position
    update_car_position()

    # UI overlay
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0.6, 0.6, 0.6)

    def quad(x0, y0, x1, y1):
        glBegin(GL_QUADS)
        glVertex2f(x0, y0)
        glVertex2f(x1, y0)
        glVertex2f(x1, y1)
        glVertex2f(x0, y1)
        glEnd()

    quad(50, 50, 140, 80)
    quad(50, 100, 140, 130)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glutSwapBuffers()


def keyboardListener(key, x, y):
    global camera_angle, camera_height
    angle_step = 5
    height_step = 20

    if key == b'a':
        camera_angle = (camera_angle - angle_step) % 360
    elif key == b'd':
        camera_angle = (camera_angle + angle_step) % 360
    elif key == b'w':
        camera_height = min(camera_height + height_step, 1500)  # limit max height
    elif key == b's':
        camera_height = max(camera_height - height_step, 100)   # limit min height

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global camera_radius, camera_angle
    radius_step = 50
    angle_step = 5

    if key == GLUT_KEY_LEFT:
        camera_angle = (camera_angle - angle_step) % 360
    elif key == GLUT_KEY_RIGHT:
        camera_angle = (camera_angle + angle_step) % 360
    elif key == GLUT_KEY_UP:
        camera_radius = max(camera_radius - radius_step, 200)  # don't zoom too close
    elif key == GLUT_KEY_DOWN:
        camera_radius = min(camera_radius + radius_step, 1500)  # don't zoom too far

    glutPostRedisplay()


def mouse_click(button, state, x, y):
    pass


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Spider-Man's City")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)  # ← added here
    glutMouseFunc(mouse_click)
    glutMainLoop()


if __name__ == "__main__":
    main()

