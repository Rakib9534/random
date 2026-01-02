# ====== PyOpenGL Interactive Example ======
# Features:
#   - Draws coordinate axes, triangle, and square
#   - Displays a moving point ("ball")
#   - Left-click to reposition ball
#   - Right-click to create an extra point
#   - Use UP/DOWN arrow keys to change ball speed
#   - Use W/S keys to increase/decrease ball size
#
#   Author: Abid Jahan Apon
# ===========================================

from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLUT import *    # GLUT library for window and input handling
from OpenGL.GLU import *     # OpenGL Utility library
import math
import random

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
r,g,b = 0.0, 0.0, 0.

rain_drop_point=[]
num_drops= 100
rain_speed= 0.2
direction= 0.0

def draw_shapes():
    """Draws a triangle and a square with color gradients."""
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 0)
    glVertex2d(-250, -250)
    glColor3f(1, 1, 0)
    glVertex2d(250, -250)
    glColor3f(1, 1, 0)
    glVertex2d(250, 00)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 0)
    glVertex2d(-250, 0)
    glColor3f(1, 1, 0)
    glVertex2d(-250, -250)
    glColor3f(1, 1, 0)
    glVertex2d(250, 00)
    glEnd()

    # Triangle
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)
    glVertex2d(-100, -50)
    glColor3f(1, 0, 0)
    glVertex2d(100, -50)
    glColor3f(1, 0, 0)
    glVertex2d(100, 50)
    glEnd()

    # Triangle_New
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)
    glVertex2d(-100, -50)
    glColor3f(1, 0, 0)
    glVertex2d(-100, 50)
    glColor3f(1, 0, 0)
    glVertex2d(100, 50)
    glEnd()

    # Triangle_shed
    glBegin(GL_TRIANGLES)
    glColor3f(0, 0, 1)
    glVertex2d(-110, 50)
    glColor3f(0, 0, 1)
    glVertex2d(110, 50)
    glColor3f(0, 0, 1)
    glVertex2d(0, 100)
    glEnd()

    # Triangle_door
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 1)
    glVertex2d(-20, -50)
    glColor3f(0, 1, 1)
    glVertex2d(-20, 0)
    glColor3f(0, 1, 1)
    glVertex2d(20, 0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 1)
    glVertex2d(-20, -50)
    glColor3f(0, 1, 1)
    glVertex2d(20, -50)
    glColor3f(0, 1, 1)
    glVertex2d(20, 0)
    glEnd()

    # Triangle_windows
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 1)
    glVertex2d(-70, 0)
    glColor3f(0, 1, 1)
    glVertex2d(-70, -20)
    glColor3f(0, 1, 1)
    glVertex2d(-30, 0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 1)
    glVertex2d(-30, 0)
    glColor3f(0, 1, 1)
    glVertex2d(-30, -20)
    glColor3f(0, 1, 1)
    glVertex2d(-70, -20)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 1)
    glVertex2d(70, 0)
    glColor3f(0, 1, 1)
    glVertex2d(30, -20)
    glColor3f(0, 1, 1)
    glVertex2d(30, 0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 1)
    glVertex2d(70, 0)
    glColor3f(0, 1, 1)
    glVertex2d(30, -20)
    glColor3f(0, 1, 1)
    glVertex2d(70, -20)
    glEnd()


def rain():
    global rain_drop_point, num_drops,direction
    rain_drop_point= [(random.randint(-250, 250), random.randint(-250, 250)) for i in range(num_drops)]
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 1.0)
    for i,j in rain_drop_point:
        glVertex2f(i, j)
        glVertex2f(i+direction,j-20)
    glEnd() 





# ===== Keyboard & Mouse Interaction =====
def keyboard_listener(key, x, y):
    """Handles normal keyboard inputs."""
    global r, g, b
    if key == b'w':  # Increase size
        r+= 0.1
        g+= 0.1
        b+= 0.1
        print("Increasing")
    elif key == b's':  # Decrease size
        r-= 0.1
        g-= 0.1
        b-= 0.1
        print("Decreasing")
    glutPostRedisplay()


def special_key_listener(key, x, y):
    """Handles special keys (arrows, F-keys, etc.)."""
    global direction
    if key == GLUT_KEY_LEFT:
        direction -= 0.5
        print("moving to left")
        print(direction)
    elif key == GLUT_KEY_RIGHT:
        direction += 0.5
        print("moving to right")
        print(direction)

    glutPostRedisplay()




# ===== Projection Setup =====
def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)


# ===== Display & Animation =====
def display():
    """Main display callback for rendering each frame."""
    glClearColor(r, g, b, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    draw_shapes()
    rain()
    
    glutSwapBuffers()


def animate():
    """Continuously moves the ball diagonally."""
    global rain_speed, rain_drop_point, direction
    for i in range(len(rain_drop_point)):
        x,y=rain_drop_point[i]
        y=y-rain_speed
        x=x-direction



        if y<-250:
            y=250
            x=random.randint(-250,250)
    
    rain_drop_point.append((x,y))


    glutPostRedisplay()


# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL Interactive Animation")

    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    # glutMouseFunc(mouse_listener)

    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()
