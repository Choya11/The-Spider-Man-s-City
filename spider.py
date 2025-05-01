import random
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Camera-related variables
camera_pos = [0, 200, 500]  # Adjust camera position for better visibility
web_pos = None  # Position where the web hits
web_active = False  # Whether the web is active or not
spiderman_health = 100  # 10 lives
dodge_active = False  # Dodge state

GRID_LENGTH = 600  # Length of grid lines

# Villain Class
class Villain:
    def __init__(self, x, y, z, villain_type):
        self.position = (x, y, z)
        self.health = 100
        self.villain_type = villain_type  # 'basic' or 'powerful'
        self.is_fleeing = False

    def move(self):
        """Random movement logic based on villain type"""
        if self.is_fleeing:
            self.position = (self.position[0] + random.randint(-10, 10),
                             self.position[1] + random.randint(-10, 10),
                             self.position[2])
        else:
            self.position = (self.position[0] + random.randint(-2, 2),
                             self.position[1] + random.randint(-2, 2),
                             self.position[2])

    def attack(self, target):
        """Villain attacks if close enough"""
        dist = math.sqrt((self.position[0] - target[0]) ** 2 + 
                         (self.position[1] - target[1]) ** 2 + 
                         (self.position[2] - target[2]) ** 2)
        if dist < 50:  # Attack range
            return True
        return False

    def special_attack(self, target):
        """Powerful villains have special attacks"""
        if self.villain_type == 'powerful':
            dist = math.sqrt((self.position[0] - target[0]) ** 2 + 
                             (self.position[1] - target[1]) ** 2 + 
                             (self.position[2] - target[2]) ** 2)
            if dist < 100:  # Special attack range
                return True
        return False

    def damage(self, amount):
        """Villain takes damage"""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """Villain dies and is removed from the game"""
        self.position = None  # Placeholder for removal
        self.health = 0


# Crime Event Generator
def generate_crime_event():
    """Generate a random, more complex crime event in the city"""
    events = ['car_chase', 'robbery', 'gang_fight', 'hostage_situation', 'bank_robbery']
    event = random.choice(events)
    x, y = random.randint(-500, 500), random.randint(-500, 500)
    print(f"A new crime event has occurred: {event} at location ({x}, {y})")
    return event, x, y

# Crime Event Handling
def handle_crime_event(event_type, x, y):
    """Handle the crime event when Spider-Man intervenes"""
    print(f"Spider-Man is responding to the {event_type} event.")
    if event_type == 'hostage_situation':
        villain = Villain(x, y, 0, 'basic')  # Villain holding hostages
        print("Villain holding hostages! Spider-Man must save them.")
    elif event_type == 'bank_robbery':
        villain = Villain(x, y, 0, 'basic')  # Villain robbing the bank
        print("Villain is robbing the bank! Stop them!")
    else:
        villain = Villain(x, y, 0, 'basic')  # Basic villain encounter for other crimes
    villain.move()
    return villain

# Spider-Man Movement and Web-Shooting
def setupCamera():
    """Configures the camera's projection and view settings."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Adjust the field of view (FOV) and near/far clipping planes to get a better perspective
    gluPerspective(90, 1.25, 10, 1000)  # Increased the near plane to avoid clipping
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    x, y, z = camera_pos
    gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)  # Adjusted up vector to ensure correct camera orientation

def draw_spiderman():
    """Draw Spider-Man with the reference cartoonish design."""
    glPushMatrix()
    glTranslatef(0, 100, 0)
    glColor3f(1, 0, 0)  # Red for Spider-Man's suit
    glutSolidCube(40)  # Body
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 150, 0)
    glColor3f(1, 1, 1)  # White eyes
    glutSolidSphere(20, 20, 20)
    glPopMatrix()

def draw_mysterio():
    """Draw Mysterio villain with the reference design."""
    glPushMatrix()
    glTranslatef(300, 100, 0)
    glColor3f(0, 1, 0)  # Green for Mysterio's suit
    glutSolidCube(50)  # Body
    glPopMatrix()

    # Glass Sphere Helmet
    glPushMatrix()
    glTranslatef(300, 150, 0)
    glColor3f(1, 1, 1)  # Glass helmet (white)
    glutSolidSphere(25, 20, 20)
    glPopMatrix()

def draw_buildings():
    """Generate the city buildings with more appropriate scaling and spacing."""
    building_spacing = 200  # Adjust spacing between buildings

    # Loop through grid and place buildings with proper spacing
    for i in range(-5, 5):
        for j in range(-5, 5):
            glPushMatrix()
            # Place each building with enough spacing
            glTranslatef(i * building_spacing, j * building_spacing, 0)  # Position each building
            building_height = random.randint(80, 250)  # Height of the building between 80 and 250
            glColor3f(0.5, 0.5, 0.5)  # Color for buildings (light gray)
            glutSolidCube(building_height)  # Draw building with the correct size
            glPopMatrix()

def draw_web():
    """Draw the web between Spider-Man and the target."""
    if web_pos:
        glLineWidth(2)
        glColor3f(1, 1, 1)  # White web color
        glBegin(GL_LINES)
        glVertex3f(camera_pos[0], camera_pos[1], camera_pos[2])  # Spider-Man's position
        glVertex3f(web_pos[0], web_pos[1], web_pos[2])  # Target web position
        glEnd()

def shoot_web():
    """Shoot a web to a target position."""
    global web_pos, web_active
    web_pos = (camera_pos[0] + 100, camera_pos[1] + 100, camera_pos[2] - 100)  # Target point in the air
    web_active = True

def swing():
    """Simulate Spider-Man swinging to the web."""
    global web_active, web_pos, camera_pos  # Declare as global
    if web_active and web_pos:
        direction_x = web_pos[0] - camera_pos[0]
        direction_y = web_pos[1] - camera_pos[1]
        direction_z = web_pos[2] - camera_pos[2]
        distance = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
        if distance > 1:
            camera_pos[0] += (direction_x / distance) * 5
            camera_pos[1] += (direction_y / distance) * 5
            camera_pos[2] += (direction_z / distance) * 5
        else:
            web_pos = None
            web_active = False
    return camera_pos

def showScreen():
    """Display function to render the game scene."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Set up the camera

    # Render the city grid
    glBegin(GL_QUADS)
    glColor3f(0.7, 0.7, 0.7)  # Grid color (light gray)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glEnd()

    # Draw buildings as placeholders for city environment
    draw_buildings()

    # Draw Spider-Man and Mysterio
    draw_spiderman()
    draw_mysterio()

    # If web is active, draw the web
    draw_web()

    # Swing Spider-Man if the web is active
    swing()

    glutSwapBuffers()

# Keyboard and Camera Controls
def keyboardListener(key, x, y):
    global camera_pos, web_pos, web_active, spiderman_health, dodge_active
    x, y, z = camera_pos

    if key == b'w':  # Move camera forward
        z -= 10
    elif key == b's':  # Move camera backward
        z += 10
    elif key == b'a':  # Move camera left
        x -= 10
    elif key == b'd':  # Move camera right
        x += 10
    elif key == b'q':  # Move camera up
        y += 10
    elif key == b'e':  # Move camera down
        y -= 10
    elif key == b'c':  # Switch to combat mode
        villain = handle_combat()
        print(f"Villain position: {villain.position}")
    elif key == b'r':  # Reset the game if web is not active
        web_pos = None
        web_active = False
        x, y, z = (0, 500, 500)  # Reset Spider-Man's position
    elif key == b' ':  # Dodge (spacebar)
        dodge()
    elif key == b'e':  # Counter-attack (e key)
        if counter_attack():
            print("Villain is stunned by the counter-attack!")

    camera_pos = [x, y, z]
    glutPostRedisplay()

# Mouse click controls (For On-Screen Buttons)
def mouse_click(button, state, x, y):
    """Map mouse clicks to move the camera based on buttons"""
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 50 < x < 150 and 50 < y < 100:
            camera_pos[2] -= 10  # Move forward
        elif 50 < x < 150 and 150 < y < 200:
            camera_pos[2] += 10  # Move backward
        elif 150 < x < 250 and 50 < y < 100:
            camera_pos[0] -= 10  # Move left
        elif 150 < x < 250 and 150 < y < 200:
            camera_pos[0] += 10  # Move right
        elif 250 < x < 350 and 50 < y < 100:
            camera_pos[1] += 10  # Move up
        elif 250 < x < 350 and 150 < y < 200:
            camera_pos[1] -= 10  # Move down
        glutPostRedisplay()

# Draw On-Screen Buttons
def draw_buttons():
    """Draw the on-screen buttons for camera controls"""
    glColor3f(0.7, 0.7, 0.7)  # Button color

    # "Move Forward" button
    glBegin(GL_QUADS)
    glVertex2f(50, 50)
    glVertex2f(150, 50)
    glVertex2f(150, 100)
    glVertex2f(50, 100)
    glEnd()

    # "Move Backward" button
    glBegin(GL_QUADS)
    glVertex2f(50, 150)
    glVertex2f(150, 150)
    glVertex2f(150, 200)
    glVertex2f(50, 200)
    glEnd()

    # "Move Left" button
    glBegin(GL_QUADS)
    glVertex2f(150, 50)
    glVertex2f(250, 50)
    glVertex2f(250, 100)
    glVertex2f(150, 100)
    glEnd()

    # "Move Right" button
    glBegin(GL_QUADS)
    glVertex2f(150, 150)
    glVertex2f(250, 150)
    glVertex2f(250, 200)
    glVertex2f(150, 200)
    glEnd()

    # "Move Up" button
    glBegin(GL_QUADS)
    glVertex2f(250, 50)
    glVertex2f(350, 50)
    glVertex2f(350, 100)
    glVertex2f(250, 100)
    glEnd()

    # "Move Down" button
    glBegin(GL_QUADS)
    glVertex2f(250, 150)
    glVertex2f(350, 150)
    glVertex2f(350, 200)
    glVertex2f(250, 200)
    glEnd()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Spider-Man's City")

    glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouse_click)
    glutMainLoop()

if __name__ == "__main__":
    main()







