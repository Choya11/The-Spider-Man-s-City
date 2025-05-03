from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

GRID_SIZE = 600
BLOCK_SIZE = 220
WIN_W, WIN_H = 1000, 800

# Spider-Man variables
spiderman_pos = [0, 0, 20]  # Starting position on ground
spiderman_angle = 0
spiderman_scale = 1.0
spiderman_walking = False
spiderman_walk_cycle = 0
spiderman_arm_angle = 0
spiderman_leg_angle = 0

# Camera state
camera_modes = ["overhead", "first_person", "follow_spiderman"]
current_camera_mode = 0
use_first_person = False
fp_pos = [0.0, 0.0, 15.0]  # x, y, z
fp_angle = 0.0  # Horizontal rotation
camera_angle = 0
camera_radius = 900
camera_height = 700

# City elements
car_positions = [(-GRID_SIZE + random.uniform(0, 200)) for _ in range(7)]

building_heights = [[0 for _ in range(6)] for _ in range(6)]
for i in range(6):
    for j in range(6):
        distance_from_center = max(abs(i - 2.5), abs(j - 2.5))
        base_height = 100 + (3 - distance_from_center) * 60
        building_heights[i][j] = base_height + random.uniform(-20, 20)

helicopter_angle = 0
max_height = 0
heli_pos = (0, 0, 0)
for i in range(6):
    for j in range(6):
        h = building_heights[i][j]
        if h > max_height:
            max_height = h
            heli_pos = ((i - 2.5) * BLOCK_SIZE, (j - 2.5) * BLOCK_SIZE, h)

planes = []
for _ in range(3):
    plane = {
        'x': random.uniform(-GRID_SIZE, GRID_SIZE),
        'y': random.uniform(-GRID_SIZE, GRID_SIZE),
        'z': random.uniform(300, 600),
        'dx': random.uniform(-1, 1) * 2,
        'dy': random.uniform(-1, 1) * 2
    }
    planes.append(plane)


def draw_streets_and_sidewalks():
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

    glColor3f(0.06, 0.2, 0.1)
    for i in range(-3, 3):
        for j in range(-3, 3):
            cx = (i + 0.5) * BLOCK_SIZE
            cy = (j + 0.5) * BLOCK_SIZE
            size = BLOCK_SIZE - 30
            glBegin(GL_QUADS)
            glVertex3f(cx - size / 2, cy - size / 2, 0.001)
            glVertex3f(cx + size / 2, cy - size / 2, 0.001)
            glVertex3f(cx + size / 2, cy + size / 2, 0.001)
            glVertex3f(cx - size / 2, cy + size / 2, 0.001)
            glEnd()

    glColor3f(0.4, 0.4, 0.4)
    for i in range(-3, 4):
        y = i * BLOCK_SIZE
        for off in (+15, -25):
            glBegin(GL_QUADS)
            glVertex3f(-GRID_SIZE, y + off, 0.01)
            glVertex3f(GRID_SIZE, y + off, 0.01)
            glVertex3f(GRID_SIZE, y + off + 10, 0.01)
            glVertex3f(-GRID_SIZE, y + off + 10, 0.01)
            glEnd()
    for i in range(-3, 4):
        x = i * BLOCK_SIZE
        for off in (+15, -25):
            glBegin(GL_QUADS)
            glVertex3f(x + off, -GRID_SIZE, 0.01)
            glVertex3f(x + off, GRID_SIZE, 0.01)
            glVertex3f(x + off + 10, GRID_SIZE, 0.01)
            glVertex3f(x + off + 10, -GRID_SIZE, 0.01)
            glEnd()


def draw_buildings():
    for i in range(-3, 3):
        for j in range(-3, 3):
            cx = (i + 0.5) * BLOCK_SIZE
            cy = (j + 0.5) * BLOCK_SIZE
            w = 120
            h = building_heights[i + 3][j + 3]

            glPushMatrix()
            glTranslatef(cx, cy, h / 2)
            glScalef(w, w, h)

            if h < 150:
                glColor3f(0.3, 0.3, 0.4)
            elif h < 220:
                glColor3f(0.4, 0.3, 0.3)
            else:
                glColor3f(0.15, 0.2, 0.2)

            glutSolidCube(1.0)

            glPopMatrix()

            window_color = (1, 1, 0.9)
            glColor3f(*window_color)
            glPointSize(2)
            glBegin(GL_POINTS)
            for wx in range(-w // 2 + 8, w // 2 - 8, 16):
                for wz in range(10, int(h) - 10, 30):
                    glVertex3f(cx + wx, cy - w / 2 - 0.02, wz)
                    glVertex3f(cx + wx, cy + w / 2 + 0.02, wz)
            for wy in range(-w // 2 + 8, w // 2 - 8, 16):
                for wz in range(10, int(h) - 10, 30):
                    glVertex3f(cx - w / 2 - 0.02, cy + wy, wz)
                    glVertex3f(cx + w / 2 + 0.02, cy + wy, wz)
            glEnd()

            glColor3f(0.7, 0.7, 0.7)
            glBegin(GL_LINES)
            floor_gap = 20  # height between each floor marking
            for z in range(floor_gap, int(h), floor_gap):
                # Front face
                glVertex3f(cx - w / 2, cy - w / 2, z)
                glVertex3f(cx + w / 2, cy - w / 2, z)
                # Back face
                glVertex3f(cx - w / 2, cy + w / 2, z)
                glVertex3f(cx + w / 2, cy + w / 2, z)
                # Left face
                glVertex3f(cx - w / 2, cy - w / 2, z)
                glVertex3f(cx - w / 2, cy + w / 2, z)
                # Right face
                glVertex3f(cx + w / 2, cy - w / 2, z)
                glVertex3f(cx + w / 2, cy + w / 2, z)
            glEnd()


def draw_car(x, y):
    glColor3f(0.8, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(x, y, 8)
    glScalef(0.5, 0.3, 0.2)
    glutSolidCube(30)
    glPopMatrix()


def update_car_positions():
    global car_positions
    for i in range(7):
        if i % 2 == 0:
            car_positions[i] += 0.5
            if car_positions[i] > GRID_SIZE:
                car_positions[i] = -GRID_SIZE
        else:
            car_positions[i] -= 0.5
            if car_positions[i] < -GRID_SIZE:
                car_positions[i] = GRID_SIZE


def draw_lamps_and_signs():
    for i in range(-3, 4):
        for j in range(-3, 4):
            x, y = i * BLOCK_SIZE - 10, j * BLOCK_SIZE - 10
            glColor3f(0.8, 0.8, 0.6)
            glLineWidth(3)
            glBegin(GL_LINES)
            glVertex3f(x, y, 0)
            glVertex3f(x, y, 60)
            glEnd()
            glColor3f(1, 1, 0)
            glPointSize(5)
            glBegin(GL_POINTS)
            glVertex3f(x, y, 60)
            glEnd()
            glColor3f((i + j) % 2, 0, 0)
            glBegin(GL_QUADS)
            glVertex3f(x + 15, y + 15, 20)
            glVertex3f(x + 20, y + 15, 20)
            glVertex3f(x + 20, y + 20, 30)
            glVertex3f(x + 15, y + 20, 30)
            glEnd()


def draw_spiderman_head():
    r = 0.40 * spiderman_scale
    glColor3f(1, 0, 0)  # Red
    glutSolidSphere(r, 32, 32)

    # Webbing pattern
    glColor3f(0, 0, 0)  # Black
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

    # Eyes
    for side, angle in ((1, +35), (-1, -35)):
        glPushMatrix()
        glTranslatef(0.20 * side * spiderman_scale, 0.08 * spiderman_scale, r - 0.08 * spiderman_scale)
        glRotatef(angle, 0, 0, 1)
        glScalef(1.0, 0.6, 1.0)
        glColor3f(1, 1, 1)  # White
        glutSolidSphere(0.16 * spiderman_scale, 16, 16)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.20 * side * spiderman_scale, 0.08 * spiderman_scale, r - 0.04 * spiderman_scale)
        glRotatef(angle, 0, 0, 1)
        glScalef(0.6, 0.3, 0.6)
        glColor3f(0, 0, 0)  # Black
        glutSolidSphere(0.10 * spiderman_scale, 12, 12)
        glPopMatrix()


def draw_spiderman_torso():
    quad = gluNewQuadric()

    # Lower torso (blue)
    glColor3f(0, 0, 1)
    glPushMatrix()
    glTranslatef(0, -0.70 * spiderman_scale, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad,
                0.35 * spiderman_scale,
                0.30 * spiderman_scale,
                0.8 * spiderman_scale, 32, 4)
    glPopMatrix()

    # Upper torso (red)
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(0, -0.10 * spiderman_scale, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad,
                0.40 * spiderman_scale,
                0.35 * spiderman_scale,
                0.6 * spiderman_scale, 32, 4)
    glPopMatrix()

    # Spider emblem
    glPushMatrix()
    glTranslatef(0, 0.20 * spiderman_scale, 0.38 * spiderman_scale)
    glColor3f(0.2, 0.2, 0.2)
    glutSolidSphere(0.05 * spiderman_scale, 16, 16)
    glLineWidth(2)
    glBegin(GL_LINES)
    for dx, dy in (
            (0.08, 0.10), (0.08, -0.10),
            (-0.08, 0.10), (-0.08, -0.10),
            (0.12, 0.00), (-0.12, 0.00)
    ):
        glVertex3f(0, 0, 0)
        glVertex3f(dx * spiderman_scale, dy * spiderman_scale, 0)
    glEnd()
    glPopMatrix()


def draw_spiderman_limbs():
    quad = gluNewQuadric()

    # Arms
    arm_angle = spiderman_arm_angle if spiderman_walking else 0
    for side, ang in ((-1, -90), (1, 90)):
        # Upper arm (blue)
        glColor3f(0, 0, 1)
        glPushMatrix()
        glTranslatef(0.5 * side * spiderman_scale, 0.3 * spiderman_scale, 0)
        glutSolidSphere(0.1 * spiderman_scale, 16, 16)
        glRotatef(ang + side * arm_angle, 0, 1, 0)
        gluCylinder(quad,
                    0.1 * spiderman_scale,
                    0.08 * spiderman_scale,
                    0.7 * spiderman_scale, 16, 4)
        glPopMatrix()

        # Glove (red)
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(0.5 * side * spiderman_scale, 0.3 * spiderman_scale, 0)
        glRotatef(ang + side * arm_angle, 0, 1, 0)
        glTranslatef(0, 0, 0.7 * spiderman_scale)
        glutSolidSphere(0.08 * spiderman_scale, 12, 12)
        glPopMatrix()

    # Legs
    leg_angle = spiderman_leg_angle if spiderman_walking else 0
    for side in (-1, 1):
        # Thigh (blue)
        glColor3f(0, 0, 1)
        glPushMatrix()
        glTranslatef(0.2 * side * spiderman_scale, -0.6 * spiderman_scale, 0)
        glRotatef(90 + side * leg_angle, 1, 0, 0)
        gluCylinder(quad,
                    0.11 * spiderman_scale,
                    0.11 * spiderman_scale,
                    1.2 * spiderman_scale, 16, 4)
        glPopMatrix()

        # Boot (red)
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(0.2 * side * spiderman_scale, -0.6 * spiderman_scale, 0)
        glRotatef(90 + side * leg_angle, 1, 0, 0)
        glTranslatef(0, 0, 1.2 * spiderman_scale)
        glutSolidSphere(0.12 * spiderman_scale, 12, 12)
        glPopMatrix()


def draw_spiderman_neck():
    quad = gluNewQuadric()
    glColor3f(1, 0, 0)  # Red
    glPushMatrix()
    glTranslatef(0, 0.55 * spiderman_scale, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad,
                0.18 * spiderman_scale,
                0.16 * spiderman_scale,
                0.15 * spiderman_scale, 16, 4)
    glPopMatrix()


def draw_spiderman():
    glPushMatrix()
    glTranslatef(*spiderman_pos)
    glRotatef(spiderman_angle, 0, 0, 1)
    glScalef(15, 15, 15)  # Scale up to match city size

    draw_spiderman_torso()
    draw_spiderman_limbs()
    draw_spiderman_neck()

    # Head
    glPushMatrix()
    glTranslatef(0, 0.55 * spiderman_scale + 0.15 * spiderman_scale + 0.40 * spiderman_scale, 0)
    draw_spiderman_head()
    glPopMatrix()

    glPopMatrix()

    # Update walking animation
    if spiderman_walking:
        spiderman_walk_cycle = (spiderman_walk_cycle + 1) % 60
        spiderman_arm_angle = 30 * math.sin(math.radians(spiderman_walk_cycle * 6))
        spiderman_leg_angle = 20 * math.sin(math.radians(spiderman_walk_cycle * 6))


def update_spiderman():
    global spiderman_pos, spiderman_angle, spiderman_walking

    # Simple AI - move toward center of park
    target_x, target_y = 0, 0
    dx = target_x - spiderman_pos[0]
    dy = target_y - spiderman_pos[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance > 20:  # If far from center, move toward it
        spiderman_walking = True
        speed = 1.5
        angle = math.degrees(math.atan2(dy, dx))
        spiderman_angle = angle
        spiderman_pos[0] += speed * math.cos(math.radians(angle))
        spiderman_pos[1] += speed * math.sin(math.radians(angle))
    else:
        spiderman_walking = False
        # Randomly turn if not walking
        if random.random() < 0.02:
            spiderman_angle = (spiderman_angle + random.uniform(-45, 45)) % 360

def draw_park():
    glColor3f(0, 0.5, 0)
    glBegin(GL_QUADS)
    glVertex3f(-100, -100, 0)
    glVertex3f(100, -100, 0)
    glVertex3f(100, 100, 0)
    glVertex3f(-100, 100, 0)
    glEnd()


def draw_helicopter():
    global helicopter_angle
    x, y, z = heli_pos

    glPushMatrix()
    glTranslatef(x, y, z + 20)
    glColor3f(0.1, 0.1, 0.6)
    glPushMatrix()
    glScalef(30, 15, 10)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-20, 0, 0)
    glScalef(20, 5, 5)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.8, 0.8, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 7)
    glRotatef(helicopter_angle, 0, 0, 1)
    glBegin(GL_LINES)
    glVertex3f(-20, 0, 0)
    glVertex3f(20, 0, 0)
    glVertex3f(0, -20, 0)
    glVertex3f(0, 20, 0)
    glEnd()
    glPopMatrix()

    glPopMatrix()


def update_helicopter():
    global helicopter_angle
    helicopter_angle = (helicopter_angle + 10) % 360


def draw_plane(plane):
    glPushMatrix()
    glTranslatef(plane['x'], plane['y'], plane['z'])
    glColor3f(0.9, 0.9, 0.9)

    glPushMatrix()
    glScalef(10, 3, 3)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 5, 0)
    glScalef(15, 1, 3)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -5, 0)
    glScalef(15, 1, 3)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(5, 0, 0)
    glScalef(2, 1, 2)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(5, 0, 0)
    glColor3f(0.6, 0.6, 0.6)
    glutSolidSphere(0.5, 10, 10)
    glPopMatrix()
    glPopMatrix()


def update_planes():
    for plane in planes:
        plane['x'] += plane['dx']
        plane['y'] += plane['dy']
        if plane['x'] > GRID_SIZE:
            plane['x'] = -GRID_SIZE
        elif plane['x'] < -GRID_SIZE:
            plane['x'] = GRID_SIZE
        if plane['y'] > GRID_SIZE:
            plane['y'] = -GRID_SIZE
        elif plane['y'] < -GRID_SIZE:
            plane['y'] = GRID_SIZE

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(75, WIN_W / WIN_H, 1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_modes[current_camera_mode] == "first_person":
        rad = math.radians(fp_angle)
        look_x = fp_pos[0] + math.sin(rad) * 50
        look_y = fp_pos[1] + math.cos(rad) * 50
        look_z = fp_pos[2]
        gluLookAt(fp_pos[0], fp_pos[1], fp_pos[2], look_x, look_y, look_z, 0, 0, 1)
    elif camera_modes[current_camera_mode] == "follow_spiderman":
        # Third-person view following Spider-Man
        follow_distance = 100
        follow_height = 50
        rad = math.radians(spiderman_angle + 180)  # Look from behind
        eye_x = spiderman_pos[0] + math.sin(rad) * follow_distance
        eye_y = spiderman_pos[1] + math.cos(rad) * follow_distance
        eye_z = spiderman_pos[2] + follow_height
        gluLookAt(eye_x, eye_y, eye_z, spiderman_pos[0], spiderman_pos[1], spiderman_pos[2] + 15, 0, 0, 1)
    else:  # overhead view
        rad = math.radians(camera_angle)
        eye_x = camera_radius * math.sin(rad)
        eye_y = camera_radius * math.cos(rad)
        eye_z = camera_height
        gluLookAt(eye_x, eye_y, eye_z, 0, 0, 0, 0, 0, 1)

def showScreen():
    glClearColor(0, 0.05, 0.25, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setupCamera()
    draw_streets_and_sidewalks()
    draw_buildings()
    draw_lamps_and_signs()
    draw_park()
    for i, car_x in enumerate(car_positions):
        y_pos = (i - 3) * BLOCK_SIZE
        draw_car(car_x, y_pos)
    draw_helicopter()
    for plane in planes:
        draw_plane(plane)
    draw_spiderman()
    update_car_positions()
    update_helicopter()
    update_planes()
    update_spiderman()
    glutSwapBuffers()


def keyboardListener(key, x, y):
    global current_camera_mode, fp_pos, fp_angle, camera_angle, camera_height, camera_radius, use_first_person

    key = key.decode('utf-8').lower()

    if key == 'c':  # Cycle camera modes
        current_camera_mode = (current_camera_mode + 1) % len(camera_modes)
        use_first_person = (camera_modes[current_camera_mode] == "first_person")

    elif key == 'r':  # Reset Spider-Man position
        global spiderman_pos, spiderman_angle
        spiderman_pos = [0, 0, 20]
        spiderman_angle = 0

    # First-person camera controls
    elif camera_modes[current_camera_mode] == "first_person":
        speed = 10
        rad = math.radians(fp_angle)
        if key == 'w':
            fp_pos[0] += math.sin(rad) * speed
            fp_pos[1] += math.cos(rad) * speed
        elif key == 's':
            fp_pos[0] -= math.sin(rad) * speed
            fp_pos[1] -= math.cos(rad) * speed
        elif key == 'a':
            fp_angle = (fp_angle - 5) % 360
        elif key == 'd':
            fp_angle = (fp_angle + 5) % 360
        elif key == 'q':
            fp_pos[2] += 10
        elif key == 'e':
            fp_pos[2] = max(1, fp_pos[2] - 10)

    # Overhead camera controls
    elif camera_modes[current_camera_mode] == "overhead":
        if key == 'a':
            camera_angle = (camera_angle - 5) % 360
        elif key == 'd':
            camera_angle = (camera_angle + 5) % 360
        elif key == 'w':
            camera_height = min(camera_height + 20, 1500)
        elif key == 's':
            camera_height = max(camera_height - 20, 100)

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global camera_radius, camera_angle

    if camera_modes[current_camera_mode] == "overhead":
        if key == GLUT_KEY_LEFT:
            camera_angle = (camera_angle - 5) % 360
        elif key == GLUT_KEY_RIGHT:
            camera_angle = (camera_angle + 5) % 360
        elif key == GLUT_KEY_UP:
            camera_radius = max(camera_radius - 50, 200)
        elif key == GLUT_KEY_DOWN:
            camera_radius = min(camera_radius + 50, 1500)

    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Spider-Man's City")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMainLoop()


if __name__ == "__main__":
    main()
