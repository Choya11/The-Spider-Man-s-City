from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Villain state
villain_pos = [300, 0, 300]  # x, y, z
villain_alive = True
villain_speed = 2.0
attack_range = 200
bullet_active = False
bullet_pos = [0, 0, 0]
bullet_speed = 4.0

def reset_villain():
    global villain_pos, villain_alive
    villain_pos = [300, 0, 300]
    villain_alive = True

def draw_villain():
    if not villain_alive:
        return

    glPushMatrix()
    glColor3f(1, 0, 1)  # Purple villain
    glTranslatef(*villain_pos)
    glutSolidCube(40)
    glPopMatrix()

    if bullet_active:
        draw_bullet()

def update_villain(spiderman_pos):
    global villain_pos, bullet_active, bullet_pos

    if not villain_alive:
        return

    dx = spiderman_pos[0] - villain_pos[0]
    dz = spiderman_pos[2] - villain_pos[2]
    distance = math.sqrt(dx ** 2 + dz ** 2)

    # Chase Spider-Man
    if distance < 400 and distance > 50:
        angle = math.atan2(dz, dx)
        villain_pos[0] += math.cos(angle) * villain_speed
        villain_pos[2] += math.sin(angle) * villain_speed

    # Attack Spider-Man
    if distance <= attack_range and not bullet_active:
        bullet_pos[0] = villain_pos[0]
        bullet_pos[1] = villain_pos[1]
        bullet_pos[2] = villain_pos[2]
        fire_bullet(spiderman_pos)

def fire_bullet(target_pos):
    global bullet_active, bullet_dir
    bullet_active = True
    dx = target_pos[0] - bullet_pos[0]
    dz = target_pos[2] - bullet_pos[2]
    length = math.sqrt(dx ** 2 + dz ** 2)
    bullet_dir = [dx / length, dz / length]

def draw_bullet():
    global bullet_pos
    glPushMatrix()
    glColor3f(1, 0.5, 0)
    glTranslatef(bullet_pos[0], bullet_pos[1], bullet_pos[2])
    glutSolidSphere(8, 10, 10)
    glPopMatrix()

def update_bullet():
    global bullet_pos, bullet_active
    if not bullet_active:
        return
    bullet_pos[0] += bullet_dir[0] * bullet_speed
    bullet_pos[2] += bullet_dir[1] * bullet_speed

    # Deactivate bullet if out of bounds
    if abs(bullet_pos[0]) > 600 or abs(bullet_pos[2]) > 600:
        bullet_active = False

def villain_hit_by_web(web_pos):
    global villain_alive
    dx = web_pos[0] - villain_pos[0]
    dz = web_pos[2] - villain_pos[2]
    if math.sqrt(dx ** 2 + dz ** 2) < 30:
        villain_alive = False
