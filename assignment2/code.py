from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import sys


width, height = 800, 600


player_x = 0
player_y = -height // 2 + 50
player_speed = 20
circles = []
bullets = [] 
score = 0
misses = 0
game_over = False
paused = False
special_circle_timer = 0
circle_count = 0  
initial_circle_speed = 4 
circle_speed = initial_circle_speed


def draw_circle_midpoint(cx, cy, radius):
    x = 0
    y = radius
    d = 1 - radius

    def draw_symmetric_points(cx, cy, x, y):
        glVertex2f(cx + x, cy + y)
        glVertex2f(cx - x, cy + y)
        glVertex2f(cx + x, cy - y)
        glVertex2f(cx - x, cy - y)
        glVertex2f(cx + y, cy + x)
        glVertex2f(cx - y, cy + x)
        glVertex2f(cx + y, cy - x)
        glVertex2f(cx - y, cy - x)

    draw_symmetric_points(cx, cy, x, y)

    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        draw_symmetric_points(cx, cy, x, y)

def draw_line_midpoint(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        glVertex2f(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_player():
    glColor3f(0.0, 0.5, 1.0)
    glBegin(GL_POINTS)

    draw_line_midpoint(player_x - 10, player_y, player_x - 10, player_y + 30)
    draw_line_midpoint(player_x + 10, player_y, player_x + 10, player_y + 30)
    draw_line_midpoint(player_x - 10, player_y, player_x + 10, player_y)
    draw_line_midpoint(player_x - 10, player_y + 30, player_x + 10, player_y + 30)
    glEnd()


    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    draw_line_midpoint(player_x - 10, player_y, player_x - 20, player_y - 10)
    draw_line_midpoint(player_x - 20, player_y - 10, player_x, player_y)
    draw_line_midpoint(player_x + 10, player_y, player_x + 20, player_y - 10)
    draw_line_midpoint(player_x + 20, player_y - 10, player_x, player_y)
    glEnd()

 
    glColor3f(1.0, 1.0, 0.0) 
    glBegin(GL_POINTS)
    draw_line_midpoint(player_x - 2, player_y, player_x - 2, player_y - 15) 
    draw_line_midpoint(player_x + 2, player_y, player_x + 2, player_y - 15)  
    glEnd()

   
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    draw_line_midpoint(player_x - 10, player_y + 30, player_x + 10, player_y + 30)
    draw_line_midpoint(player_x - 10, player_y + 30, player_x, player_y + 50)
    draw_line_midpoint(player_x + 10, player_y + 30, player_x, player_y + 50)
    glEnd()


def draw_circles():
    glBegin(GL_POINTS)
    for x, y, radius, is_special in circles:
        glColor3f(0.0, 1.0, 0.0) if is_special else glColor3f(1.0, 0.5, 0.0)
        draw_circle_midpoint(x, y, int(radius))
    glEnd()


def draw_bullets():
    glColor3f(1.0, 0.0, 0.0)  
    glBegin(GL_POINTS)
    for x, y in bullets:
        draw_circle_midpoint(x, y, 5)
    glEnd()


def draw_buttons():
    button_y = height // 2 - 50 
    button_spacing = 100  

    
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    draw_line_midpoint(-button_spacing + 50, button_y, -button_spacing - 30, button_y)
    draw_line_midpoint(-button_spacing - 30, button_y - 10, -button_spacing - 50, button_y)
    draw_line_midpoint(-button_spacing - 30, button_y + 10, -button_spacing - 50, button_y)
    draw_line_midpoint(-button_spacing - 30, button_y - 10, -button_spacing - 30, button_y + 10)
    glEnd()

    
    if paused:
        glColor3f(0.0, 1.0, 1.0) 
        glBegin(GL_POINTS)
        draw_line_midpoint(-10, button_y + 20, -10, button_y - 20)
        draw_line_midpoint(-10, button_y - 20, 20, button_y)
        draw_line_midpoint(20, button_y, -10, button_y + 20)
        glEnd()
    else:
        glColor3f(0.0, 1.0, 1.0) 
        glBegin(GL_POINTS)
        draw_line_midpoint(-10, button_y + 20, -10, button_y - 20) 
        draw_line_midpoint(10, button_y + 20, 10, button_y - 20)   
        glEnd()


    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    draw_line_midpoint(button_spacing - 20, button_y - 20, button_spacing + 20, button_y + 20)
    draw_line_midpoint(button_spacing - 20, button_y + 20, button_spacing + 20, button_y - 20)
    glEnd()




def keyboard(key, x, y):
    global player_x, bullets, game_over, paused

    if key == b'a' and not game_over and not paused:  
        player_x = max(player_x - player_speed, -width // 2 + 30)
    elif key == b'd' and not game_over and not paused: 
        player_x = min(player_x + player_speed, width // 2 - 30)
    elif key == b' ':
        if not game_over and not paused:
            bullets.append((player_x, player_y + 50))
    elif key == b'p':
        paused = not paused
    elif key == b'r':
        reset_game()
    elif key == b'q': 
        print(f"Goodbye! Final score: {score}")
        glutLeaveMainLoop()


def mouse(button, state, x, y):
    global paused, game_over

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        gl_x = x - width // 2
        gl_y = height // 2 - y

        if -150 <= gl_x <= -50:  
            reset_game()
        elif -50 <= gl_x <= 50:             
            paused = not paused
        elif 50 <= gl_x <= 150:  
            print(f"Goodbye! Final score: {score}")
            glutLeaveMainLoop()

def reset_game():
    global player_x, player_y, circles, bullets, score, misses, game_over, paused, circle_count, special_circle_timer, circle_speed

    player_x = 0
    player_y = -height // 2 + 50
    circles = []
    bullets = []
    score = 0
    misses = 0
    game_over = False
    paused = False
    circle_count = 0
    special_circle_timer = 0
    circle_speed = initial_circle_speed

    glutTimerFunc(30, update, 0)
    glutPostRedisplay()


def update(value):
    global circles, bullets, score, misses, game_over, special_circle_timer, circle_count, circle_speed

    if not game_over and not paused:
        for i, (x, y, radius, is_special) in enumerate(circles):
            circles[i] = (x, y - circle_speed, radius, is_special)
            

            if (player_x - x) ** 2 + (player_y - y) ** 2 <= (radius + 15) ** 2:
                game_over = True
                print(f"Game Over! A circle hit the rocket. Final score: {score}")
                return

            if y - radius <= -height // 2:
                misses += 1
                circles.pop(i)
                if misses >= 3:
                    game_over = True
                    print(f"Game Over! Final score: {score}")

        for i, (x, y) in enumerate(bullets):
            bullets[i] = (x, y + 10)
            if y > height // 2:
                bullets.pop(i)

        for bullet in bullets:
            for circle in circles:
                bx, by = bullet
                cx, cy, cr, is_special = circle
                if (bx - cx) ** 2 + (by - cy) ** 2 <= cr ** 2:
                    bullets.remove(bullet)
                    circles.remove(circle)
                    score += 5 if is_special else 1
                    print(f"Score: {score}")   
                    break

        if random.random() < 0.02:
            circle_count += 1
            new_circle_x = random.randint(-width // 2 + 30, width // 2 - 30)
            is_special = circle_count % 5 == 0
            circles.append((new_circle_x, height // 2 - 30, 20, is_special))

        special_circle_timer += 1
        for i, (x, y, radius, is_special) in enumerate(circles):
            if is_special:
                new_radius = 20 + 10 * math.sin(special_circle_timer * 0.1)
                circles[i] = (x, y, new_radius, is_special)

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_buttons()
    draw_player()
    draw_circles()
    draw_bullets()
    glutSwapBuffers()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-width // 2, width // 2, -height // 2, height // 2)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Shoot The Circles!")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(30, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()