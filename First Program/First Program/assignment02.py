
from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLUT import *    # GLUT library for window and input handling
from OpenGL.GLU import *     # OpenGL Utility library

import random


# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
r, g, b= random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)
diamond_x= random.randint(-245, 245)
diamond_y= 220
speed= 0.07
catcher_x, catcher_y= -50, -240 
catcher_speed= 3
game_over= False
score= 0
paused= False
cheat= False


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


#zone_finding:
def find_zone(x1, y1, x2, y2):
    dx= x2- x1
    dy= y2- y1
    if dx>= 0 and dy>= 0:
        if abs(dx) >= abs(dy):
            return 0
        else:
            return 1
    elif dx< 0 and dy>= 0:
        if abs(dx) >= abs(dy):
            return 3
        else:
            return 2
    elif dx< 0 and dy< 0:
        if abs(dx) >= abs(dy):
            return 4
        else:
            return 5
    else:
        if abs(dx) >= abs(dy):
            return 7
        else:
            return 6

#any zone-> zone 0
def to_zone0(x, y, zone):
    if zone== 0:
        return x, y
    elif zone== 1:
        return y, x
    elif zone== 2:
        return y, -x
    elif zone== 3:
        return -x, y
    elif zone== 4:
        return -x, -y
    elif zone== 5:
        return -y, -x
    elif zone== 6:
        return -y, x
    else:
        return x, -y
    
#zone 0-> any zone
def from_zone0(x, y, zone):
    if zone== 0:
        return x, y
    elif zone== 1:
        return y, x
    elif zone== 2:
        return -y, x
    elif zone== 3:
        return -x, y
    elif zone== 4:
        return -x, -y
    elif zone== 5:
        return -y, -x
    elif zone== 6:
        return y, -x
    else:
        return x, -y



def drawline(x1, y1, x2, y2, zone):
    dx= x2- x1
    dy= y2- y1
    di= 2*dy- dx
    incE= 2*dy
    incNE= 2*(dy- dx)
    y= y1
    x= x1
    while x<= x2:
        px, py= from_zone0(x, y, zone)
        writePixel(px, py)
        if di> 0:
            di= di+ incNE
            y+=1
        else:
            di= di+incE
        x+= 1

def writePixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def any_drawline(x1, y1, x2, y2):
    zone= find_zone(x1, y1, x2, y2)
    x11, y11= to_zone0(x1, y1, zone)
    x22, y22= to_zone0(x2, y2, zone)
    if x11> x22:
        x11, x22= x22, x11
        y11, y22= y22, y11
    drawline(x11, y11, x22, y22, zone)

def diamond():
    global r, g, b, diamond_x, diamond_y
    size= 10
    glColor3f(r, g, b)
    any_drawline(diamond_x, diamond_y, diamond_x-size, diamond_y-size)
    any_drawline(diamond_x, diamond_y, diamond_x+size, diamond_y-size)
    any_drawline(diamond_x+size, diamond_y-size, diamond_x, diamond_y-size-size)
    any_drawline(diamond_x-size, diamond_y-size, diamond_x, diamond_y-size-size)

def catcher():
    global catcher_x, catcher_y, game_over
    h=10
    w=100
    if game_over:
        glColor3f(1, 0, 0)
    else:
        glColor3f(1, 1, 1)
    any_drawline(catcher_x, catcher_y, catcher_x, catcher_y-h)
    any_drawline(catcher_x+w, catcher_y-h, catcher_x, catcher_y-h)
    any_drawline(catcher_x, catcher_y, catcher_x+w, catcher_y)
    # any_drawline(catcher_x+w, catcher_y, catcher_x, -250)
    any_drawline(catcher_x+w, catcher_y, catcher_x+w, catcher_y-h)


def restart_game():
    global diamond_x, diamond_y, speed, score, game_over, r,g,b, catcher_x, catcher_y
    r, g, b= random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)
    diamond_x= random.randint(-245, 245)
    diamond_y= 220
    speed= 0.07
    catcher_x, catcher_y= -50, -240 
    game_over= False
    score= 0
    print(f"Starting Over: ")


# ===== Keyboard & Mouse Interaction =====
def keyboard_listener(key, x, y):
    """Handles normal keyboard inputs."""
    global catcher_x, catcher_speed, cheat
    w= 100
    if game_over or paused:
        return 
    
    if key == b'a':  
        catcher_x-= catcher_speed
        if catcher_x< -250:
            catcher_x= -250
    elif key == b'd': 
        catcher_x+=catcher_speed
        if catcher_x+w> 250:
            catcher_x= 250-w
    
    elif key == b'c':
        cheat= not cheat
        if cheat:
            print("Cheat Mode Activate")
        else:
            print("Cheat Mode Deactivate")


    glutPostRedisplay()



def mouse_listener(button, state, x, y):
    global paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        new_x, new_y = convert_coordinate(x, y)
        if -240<= new_x<= -220 and 220 <=new_y <= 240:
            restart_game()

        if -15<= new_x<= 15 and 225 <=new_y <= 245:
            paused= not paused

        if 220<= new_x<= 240 and 220 <=new_y <= 240:
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()
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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    # draw_axes()
    # draw_shapes()
    # draw_point(ball_x, ball_y, ball_size)

    #draw left arrow button
    glColor3f(0, 1, 1)
    any_drawline(-240, 230, -220, 230)
    any_drawline(-240, 230, -230, 240)
    any_drawline(-240, 230, -230, 220)

    #draw pause/play button
    glColor3f(1, 1, 0)
    if not paused:
        any_drawline(-5, 225, -5, 245)
        any_drawline(5, 225, 5, 245)
    else :
        any_drawline(-5, 225, -5, 245)
        any_drawline(-5, 245, 10, 235)
        any_drawline(-5, 225, 10, 235)
    
    #draw exit button
    glColor3f(1, 0, 0)
    any_drawline(220, 220, 240, 240)
    any_drawline(220, 240, 240, 220)
    

    diamond()
    catcher()

    glutSwapBuffers()


def animate():
    global diamond_x, diamond_y, speed, r, g, b, score, game_over, catcher_x, catcher_y, cheat

    if game_over:
        glutPostRedisplay()
        return
    
    if paused:
        glutPostRedisplay()
        return

    diamond_y -= speed  
    size = 10
    w = 100
    if cheat:
        if catcher_x+ w/2 < diamond_x:
            catcher_x+= catcher_speed*0.01
        elif catcher_x+ w/2 > diamond_x:
            catcher_x-= catcher_speed*0.01

    if diamond_y <= catcher_y + size:
        if catcher_x <= diamond_x <= catcher_x + w:
            score += 1
            print(f"Score: {score}")

            diamond_y = 220
            diamond_x = random.randint(-245, 245)
            r, g, b = random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)
            speed += 0.01

        else:
            game_over = True
            print(f"Game Over! Final Score: {score}")


    # if diamond_y < -250:
    #     diamond_y= 220
    #     diamond_x= random.randint(-245, 245)
    #     r, g, b= random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)
    # speed+= 0.000001

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
    # glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()
