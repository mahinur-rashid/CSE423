from OpenGL.GL import *  # Core OpenGL functions
from OpenGL.GLUT import *  # OpenGL Utility Toolkit for window creation and input handling
from OpenGL.GLU import *  # OpenGL Utility Library for perspective and view transformations
import random  # Used for generating random positions for raindrops

# Window dimensions and initial background color
W_width, W_height = 500, 500
bg_color = [1, 1, 1]  # White background
raindrops_arr = []  # Array to hold raindrop properties
rain_angle = 0.0  # Angle of the rain slant
import math
# Function to draw a line (used for raindrops)
def draw_lines(x, y, length, width):
    glLineWidth(width)  # Set line width
    glColor3f(0, 0, 0)  # Set color to black
    glBegin(GL_LINES)  # Start drawing a line
    glVertex2f(x, y)  # Starting point
    glVertex2f(x, y - length)  # End point
    glEnd()  # End drawing

# Function to draw the house and its components
def draw_shapes():
    global bg_color
    house_color = (1, 1, 1) if bg_color[0] < 0.2 else (0, 0, 0)  # Set house color based on background

    # House base (rectangle outline)
    glLineWidth(15)
    glColor3f(*house_color)
    glBegin(GL_LINES)
    glVertex2d(-108, -50)  # Bottom left
    glVertex2d(108, -50)  # Bottom right
    glVertex2d(105, -50)  # Connect bottom to sides
    glVertex2d(105, 80)
    glVertex2d(105, 80)  # Top right to top left
    glVertex2d(-105, 80)
    glVertex2d(-105, 80)  # Top left to bottom left
    glVertex2d(-105, -50)
    glEnd()

    # House roof (triangle outline)
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(*house_color)
    glVertex2d(-120, 80)  # Left point
    glVertex2d(120, 80)  # Right point
    glVertex2d(0, 200)  # Top point
    glEnd()

    # Roof inner color (to match background)
    glLineWidth(15)
    glBegin(GL_TRIANGLES)
    glColor3f(bg_color[0], bg_color[1], bg_color[2])
    glVertex2d(-110, 85)  # Slightly smaller triangle inside
    glVertex2d(110, 85)
    glVertex2d(0, 185)
    glEnd()

    # Door (rectangle outline)
    glLineWidth(5)
    glColor3f(*house_color)
    glBegin(GL_LINES)
    glVertex2d(-50, -50)
    glVertex2d(-10, -50)
    glVertex2d(-10, -50)
    glVertex2d(-10, 20)
    glVertex2d(-10, 20)
    glVertex2d(-50, 20)
    glVertex2d(-50, 20)
    glVertex2d(-50, -50)
    glEnd()

    # Door handle (point)
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(*house_color)
    glVertex2f(-30, -15)  # Position of the handle
    glEnd()

    # Window (rectangle with cross)
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(*house_color)
    glVertex2d(60, 20)  # Right-bottom to right-top
    glVertex2d(30, 20)
    glVertex2d(30, 20)
    glVertex2d(30, 60)
    glVertex2d(30, 60)
    glVertex2d(60, 60)
    glVertex2d(60, 60)
    glVertex2d(60, 20)

    glVertex2d(45, 20)  # Vertical middle line
    glVertex2d(45, 60)
    glVertex2d(30, 40)  # Horizontal middle line
    glVertex2d(60, 40)
    glEnd()

# Generate raindrops with random positions
def raindrops_class():    
    global raindrops_arr
    raindrops_arr = []
    for _ in range(500):  # Create 500 raindrops
        x_cor = random.randint(-W_width // 2, W_width // 2)  # Random X position
        y_cor = random.randint(-W_height // 2, W_height // 2)  # Random Y position
        rain_width = 1  # Raindrop width
        rain_length = 15  # Raindrop length
        raindrops_arr.append([x_cor, y_cor, rain_length, rain_width])

# Render raindrops and manage their movement
def make_rain():
    global raindrops_arr, rain_angle, bg_color

    raindrop_color = (1, 1, 1) if bg_color[0] < 0.2 else (0, 0, 0)  # Raindrop color based on background

    # Roof and house boundaries for collision detection
    roof_left = (-120, 80)
    roof_right = (120, 80)
    roof_top = (0, 200)

    house_left = -105
    house_right = 105
    house_bottom = -50
    house_top = 80

    # Helper functions for collision detection
    def is_inside_triangle(x, y):
        # Check if point (x, y) is inside the triangle
        def triangle_area(x1, y1, x2, y2, x3, y3):
            return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

        total_area = triangle_area(*roof_left, *roof_right, *roof_top)
        area1 = triangle_area(x, y, *roof_right, *roof_top)
        area2 = triangle_area(*roof_left, x, y, *roof_top)
        area3 = triangle_area(*roof_left, *roof_right, x, y)

        return abs(total_area - (area1 + area2 + area3)) < 0.1

    def is_inside_rectangle(x, y):
        # Check if point (x, y) is inside the rectangle
        return house_left <= x <= house_right and house_bottom <= y <= house_top

    # Update each raindrop
    for drop in raindrops_arr:
        x, y, length, width = drop
        slant_offset = math.tan(math.radians(rain_angle)) * length  # Calculate slant

        # Reset raindrop position if it collides with house or roof
        if is_inside_triangle(x, y) or is_inside_rectangle(x, y):
            drop[1] = W_height // 2
            drop[0] = random.randint(-W_width // 2, W_width // 2)
            continue

        # Draw the raindrop
        glLineWidth(width)
        glColor3f(*raindrop_color)
        glBegin(GL_LINES)
        glVertex2f(x, y)
        glVertex2f(x + slant_offset, y - length)
        glEnd()

        # Move the raindrop downwards
        drop[1] -= 1
        if drop[1] - length <= 50:  # Reset if below screen
            drop[1] = W_height // 2
            drop[0] = random.randint(-W_width // 2, W_width // 2)

# Display function to render the scene
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen
    glClearColor(bg_color[0], bg_color[1], bg_color[2], 1)  # Set background color
    glMatrixMode(GL_MODELVIEW)  # Switch to ModelView matrix
    glLoadIdentity()  # Reset transformations
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)  # Set camera position
    draw_shapes()  # Draw house
    make_rain()  # Draw raindrops
    glutSwapBuffers()  # Swap buffers for double buffering

# Gradually make the scene darker (night)
def Night():
    global bg_color       
    if bg_color[0] > 0.2:  # Prevent overly dark colors
        bg_color[0] -= 0.1
        bg_color[1] -= 0.1
        bg_color[2] -= 0.1

# Gradually make the scene brighter (day)
def Day():
    global bg_color
    if bg_color[0] < 0.99:  # Prevent overly bright colors
        bg_color[0] += 0.1
        bg_color[1] += 0.1
        bg_color[2] += 0.1

# Keyboard handler for toggling night/day
def key_N_D(key, x, y):
    if key == b'n':  # Press 'n' for night
        Night()
        glutPostRedisplay()
    elif key == b'd':  # Press 'd' for day
        Day()
        glutPostRedisplay()

# Special key handler for rain angle adjustment
def Key_LeftRight(key, x, y):
    global rain_angle, raindrops_arr
    horizontal_step = 5

    if key == GLUT_KEY_LEFT:  # Adjust angle left
        rain_angle = max(rain_angle - 5, -45)
        for drop in raindrops_arr:
            drop[0] -= horizontal_step
    elif key == GLUT_KEY_RIGHT:  # Adjust angle right
        rain_angle = min(rain_angle + 5, 45)
        for drop in raindrops_arr:
            drop[0] += horizontal_step
    glutPostRedisplay()

# Initialization function
def init():
    glClearColor(1, 1, 1, 1)  # Initial background color
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix
    glLoadIdentity()  # Reset transformations
    gluPerspective(104, 1, 1, 1000.0)  # Set perspective

# Timer function to update display
def timer(value):
    glutPostRedisplay()  # Redraw the scene
    glutTimerFunc(16, timer, 0)  # 60 FPS (1000ms / 16ms)

# Main program
glutInit()  # Initialize GLUT
glutInitWindowSize(W_width, W_height)  # Set window size
glutInitWindowPosition(0, 0)  # Set window position
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # Enable depth, double buffering, and RGB mode
wind = glutCreateWindow(b"Task01")  # Create window

init()  # Call initialization function
raindrops_class()  # Generate initial raindrops
glutDisplayFunc(display)  # Set display callback
glutKeyboardFunc(key_N_D)  # Set keyboard input callback for 'n' and 'd'
glutSpecialFunc(Key_LeftRight)  # Set special keys callback for arrow keys
glutTimerFunc(0, timer, 0)  # Start the timer for animations
glutMainLoop()  # Start the GLUT main loop
