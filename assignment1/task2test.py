from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random

# Window dimensions
W_width, W_height = 500, 500

# Global variables
points_list = []  # List to store the points
blink_time = []  # Track blinking time for points
blink_mode = []  # Track if a point is in blink mode
frozen_scrn = False  # Boolean to freeze/unfreeze the screen
bg_color = [0.0, 0.0, 0.0]  # Background color

# Class to represent individual points
class Points:
    def __init__(self, x, y, dx, dy, color):
        self.x = x  # x-coordinate
        self.y = y  # y-coordinate
        self.dx = dx  # x-direction speed
        self.dy = dy  # y-direction speed
        self.color = color  # Current color of the point
        self.original_color = color  # Original color for blinking restoration

# Function to draw a point
def create_point_func(point, size):
    glPointSize(size)  # Set the size of the point
    glBegin(GL_POINTS)  # Start drawing points
    glColor3f(*point.color)  # Set the color of the point
    glVertex2f(point.x, point.y)  # Specify the point's position
    glEnd()

# Function to update positions of points
def update_position():
    global frozen_scrn
    if frozen_scrn:
        return  # Do not update if the screen is frozen

    for point in points_list:
        point.x += point.dx  # Update x-coordinate
        point.y += point.dy  # Update y-coordinate

        # Check boundaries and reverse direction if necessary
        if point.x >= W_width / 2 or point.x <= -W_width / 2:
            point.dx *= -1
        if point.y >= W_height / 2 or point.y <= -W_height / 2:
            point.dy *= -1

# Function to create a new point on mouse click
def create_new_point(x, y):
    global frozen_scrn
    if frozen_scrn:
        return  # Do not create new points if the screen is frozen

    dx = random.choice([-5, 5])  # Random x-direction speed
    dy = random.choice([-5, 5])  # Random y-direction speed
    color = [random.random() for _ in range(3)]  # Random RGB color

    # Create and add the new point
    point = Points(x, y, dx, dy, color)
    points_list.append(point)
    blink_mode.append(False)  # Initial blink mode is False
    blink_time.append(0)  # Initial blink time is 0

# Function to handle blinking of points
def point_blinker():
    global frozen_scrn
    if frozen_scrn:
        return  # Do not blink if the screen is frozen

    current_time = time.time()
    for i, point in enumerate(points_list):
        if blink_mode[i]:  # If the point is in blink mode
            if current_time - blink_time[i] >= 0.5:  # If 0.5 seconds have passed
                point.color = point.original_color  # Restore original color
                blink_mode[i] = False  # Turn off blink mode

# Convert mouse coordinates from screen to OpenGL coordinates
def screen_mouse_coordinates(x, y):
    mouse_x = x - (W_width / 2)
    mouse_y = (W_height / 2) - y
    return mouse_x, mouse_y

# Initialize OpenGL settings
def init():
    glClearColor(*bg_color, 1)  # Set the background color
    glEnable(GL_BLEND)  # Enable blending
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blending function
    glMatrixMode(GL_PROJECTION)  # Set projection mode
    glLoadIdentity()  # Reset projection matrix
    gluPerspective(104, 1, 1, 1000.0)  # Set perspective view

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
    glClearColor(*bg_color, 1)  # Set the background color
    glMatrixMode(GL_MODELVIEW)  # Set model-view mode
    glLoadIdentity()  # Reset transformations
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)  # Set the camera position

    # Draw all points
    for point in points_list:
        create_point_func(point, 10)

    glutSwapBuffers()  # Swap buffers for double buffering

# Mouse click handler
def mouse_keys(button, frozen_state, x, y):
    global frozen_scrn
    if frozen_scrn:
        return  # Do not handle mouse clicks if the screen is frozen

    if button == GLUT_RIGHT_BUTTON and frozen_state == GLUT_DOWN:
        new_x, new_y = screen_mouse_coordinates(x, y)  # Convert mouse coordinates
        create_new_point(new_x, new_y)  # Create a new point
    elif button == GLUT_LEFT_BUTTON and frozen_state == GLUT_DOWN:
        # Handle blinking for all points
        for i, point in enumerate(points_list):
            if not blink_mode[i]:  # If the point is not blinking
                point.color = [0, 0, 0]  # Set color to black
                blink_mode[i] = True  # Enable blink mode
                blink_time[i] = time.time()  # Record blink start time

# Keyboard handler for arrow keys
def keyboard_UpDown(key, x, y):
    global frozen_scrn
    if frozen_scrn:
        return  # Do not handle keyboard inputs if the screen is frozen

    if key == GLUT_KEY_UP:  # Speed up points
        for point in points_list:
            point.dx *= 2
            point.dy *= 2
    elif key == GLUT_KEY_DOWN:  # Slow down points
        for point in points_list:
            point.dx /= 2
            point.dy /= 2

# Keyboard handler for space key
def keyboard_keys(key, x, y):
    global frozen_scrn
    if key == b' ':  # Toggle freeze/unfreeze with spacebar
        frozen_scrn = not frozen_scrn

# Timer function for updating and redrawing
def time_update(value):
    global frozen_scrn
    if frozen_scrn:
        glutTimerFunc(16, time_update, 0)
        return  # Skip updates if the screen is frozen

    update_position()  # Update point positions
    point_blinker()  # Update blinking points
    glutPostRedisplay()  # Request redisplay
    glutTimerFunc(16, time_update, 0)  # Repeat timer every 16ms (~60 FPS)

# Main program
glutInit()  # Initialize GLUT
glutInitWindowSize(W_width, W_height)  # Set window size
glutInitWindowPosition(0, 0)  # Set window position
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # Depth, double buffering, RGB
window = glutCreateWindow(b"Task02")  # Create window

init()  # Initialize OpenGL settings
glutDisplayFunc(display)  # Set display callback
glutKeyboardFunc(keyboard_keys)  # Set keyboard input callback for spacebar
glutSpecialFunc(keyboard_UpDown)  # Set keyboard input callback for arrow keys
glutMouseFunc(mouse_keys)  # Set mouse input callback
glutTimerFunc(0, time_update, 0)  # Start timer for updates
glutMainLoop()  # Start GLUT main loop
