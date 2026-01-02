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
ball_x, ball_y = 0, 0        # Ball coordinates (in OpenGL space)
ball_speed = 0.01            # Ball movement speed
ball_size = 5                # Ball size (GL point size)
freeze = False            # Whether a new point is created on right-click
bg= False
ball_set=[]

# ===== Coordinate Conversion =====
def convert_coordinate(x, y):
    """
    Converts mouse (screen) coordinates to OpenGL (Cartesian) coordinates.
    Top-left of the window is (0,0) in screen space,
    but OpenGL center is (0,0).
    """
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b


# ===== Draw Functions =====
def draw_point(x, y, size):
    """Draws a single point at (x, y) with given size."""
    # global r, g, b, ball_set
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# # ===== Keyboard & Mouse Interaction =====
# def keyboard_listener(key, x, y):
#     """Handles normal keyboard inputs."""
#     global freeze
#     if key == b' ':
        
#     elif key == b's':  # Decrease size
#         ball_size = max(1, ball_size - 1)
#         print("Ball size decreased")
#     glutPostRedisplay()


def special_key_listener(key, x, y):
    """Handles special keys (arrows, F-keys, etc.)."""
    global ball_speed, ball_set, bg
    if key == GLUT_KEY_UP:
        ball_speed *= 2
        for i in range(len(ball_set)):
            ball_set[i][2]*= 2
            ball_set[i][3]*= 2
        print("Speed increased")
    elif key == GLUT_KEY_DOWN:
        ball_speed /= 2
        for i in range(len(ball_set)):
            ball_set[i][2]/= 2
            ball_set[i][3]/= 2
        print("Speed decreased")
    
    # elif key == GLUT_KEY_LEFT:
    #     # for i in range(100):
    #     #     display()
    #     bg= True

    glutPostRedisplay()



def mouse_listener(button, state, x, y):
    """
    Handles mouse clicks.
    Left-click: Move ball.
    Right-click: Create a new point.
    """
    global ball_set

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        x1, y1 = convert_coordinate(x, y)
        px= random.choice([-1,1])*ball_speed
        py= random.choice([-1,1])*ball_speed
        r, g, b= random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)
        ball_set.append([x1, y1, px, py, r, g, b])


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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()


    for x, y, px, py, r, g, b in ball_set:
        glColor3f(r, g, b)
        draw_point(x, y, ball_size)
    # if bg:
    #     glColor3f(0, 0, 0)
    #     draw_point(0.0, 0.0, ball_size)

    
    glutSwapBuffers()


def animate():
    """Continuously moves the ball diagonally."""
    global ball_set

    for i in range(len(ball_set)):
        x, y, px, py, r, g, b= ball_set[i]
        x+= px
        y+= py
        if x>250 or x<-250:
            px*= -1
        if y>250 or y<-250:
            py*= -1
        ball_set[i]= [x, y, px, py, r,g,b]


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
    # glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()
