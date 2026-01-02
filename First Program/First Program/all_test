from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


# Camera-related variables
camera_pos = (0,500,500)

fovY = 120  # Field of view
GRID_LENGTH = 100  # Length of grid lines
rand_var = 423
grid_size= 10
grid_half_size= (GRID_LENGTH* grid_size)/2
num_enemy= 5
enemies= []
boundary= 200
player_pos=[0.0, 0.0]
player_speed= 5
gun_angle= 0.0
rotate_speed= 5
bullets= []
bullet_speed= 5
bullet_height= 75
bullet_dir= [0,-1]
cos=0.9961947
sin= 0.0871557
enemy_speed= 0.1
enemy_hit_radius= 25
player_hit_radius= 25
player_life= 5
bullet_missed= 0
max_bullet_missed= 10
game_over= False
game_score= 0
first_person= False

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)



def draw_player():

    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 0)
    glRotatef(gun_angle, 0, 0, 1)
    glColor3f(0.2, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 60)
    glutSolidCube(40)
    glPopMatrix()

    glColor3f(0.0, 0.0, 1.0)
    # Left leg
    glPushMatrix()
    glTranslatef(-10, 0, 20)
    gluCylinder(gluNewQuadric(), 10, 5, 40, 16, 16)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(10, 0, 20)
    gluCylinder(gluNewQuadric(), 10, 5, 40, 16, 16)
    glPopMatrix()

    # head 
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 100)
    gluSphere(gluNewQuadric(), 15, 16, 16)
    glPopMatrix()

    glPushMatrix()
    glRotatef(0, 0, 0, 1)

    glColor3f(1.0, 0.8, 0.6)  
    shoulder_radius = 5
    upper_len = 15 
    forearm_len = 30

    # left arm
    glPushMatrix()
    glTranslatef(-20, -20, 75)
    gluSphere(gluNewQuadric(), shoulder_radius, 16, 16)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 4, upper_len, 16, 1)
    glTranslatef(0, 0, upper_len)
    gluCylinder(gluNewQuadric(), 4, 0.3, forearm_len, 16, 1)
    glPopMatrix()
    glPopMatrix()

    # right arm
    glPushMatrix()
    glTranslatef(20, -20, 75)
    gluSphere(gluNewQuadric(), shoulder_radius, 16, 16)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 4, upper_len, 16, 1)
    glTranslatef(0, 0, upper_len)
    gluCylinder(gluNewQuadric(), 4, 0.3, forearm_len, 16, 1)
    glPopMatrix()

    glPopMatrix()

    # gun
    glColor3f(0.8, 0.8, 0.8)
    glPushMatrix()
    glTranslatef(0, -20 - (upper_len + forearm_len), 75)
    glScalef(0.7, 4.0, 0.7)
    glutSolidCube(5)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()



def init_enemies():
    global enemies, num_enemy
    enemies=[]

    for i in range(num_enemy):
        # x = random.uniform(-limit, limit)
        # y = random.uniform(-limit, limit)
        enemies.append(random_enemy_pos())
    
def draw_enemies():

    for (x, y) in enemies:
        glPushMatrix()
        glTranslatef(x, y, 0)

        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0, 0, 15)
        gluSphere(gluNewQuadric(), 15, 20, 20)
        glPopMatrix()

        glColor3f(0.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0, 0, 2*15 + 7)
        gluSphere(gluNewQuadric(), 7, 20, 20)
        glPopMatrix()

        glPopMatrix()

def update_enemies():
    global enemies, player_life

    for i in enemies:
        x, y= i[0], i[1]
        dx= player_pos[0]- x
        dy= player_pos[1]- y
        distance= (dx* dx+ dy*dy)**0.5
        if distance> 0:
            step= enemy_speed
            x+= dx/ distance* step
            y+= dy/ distance* step
            i[0]= x
            i[1]= y
        
        dxp = x - player_pos[0]
        dyp = y - player_pos[1]
        if dxp*dxp + dyp*dyp <= player_hit_radius * player_hit_radius:
            player_life -= 1
            new_pos = random_enemy_pos()
            i[0], i[1] = new_pos[0], new_pos[1]

def random_enemy_pos():
    margin = 20
    limit  = grid_half_size - margin
    x = random.uniform(-limit, limit)
    y = random.uniform(-limit, limit)
    return [x, y]


def draw_boundaries():
    half = grid_half_size
    h = boundary

    glBegin(GL_QUADS)

    glColor3f(0, 1, 1)
    glVertex3f(-half,  half, 0)
    glVertex3f( half,  half, 0)
    glVertex3f( half,  half, h)
    glVertex3f(-half,  half, h)

    glColor3f(0.5, 1, 0)
    glVertex3f(-half, -half, 0)
    glVertex3f( half, -half, 0)
    glVertex3f( half, -half, h)
    glVertex3f(-half, -half, h)

    glColor3f(0, 0, 1.0)
    glVertex3f(-half, -half, 0)
    glVertex3f(-half,  half, 0)
    glVertex3f(-half,  half, h)
    glVertex3f(-half, -half, h)

    glColor3f(1, 1, 1)
    glVertex3f( half, -half, 0)
    glVertex3f( half,  half, 0)
    glVertex3f( half,  half, h)
    glVertex3f( half, -half, h)

    glEnd()

def draw_bullets():
    glColor3f(1, 0, 0)
    for i in bullets:
        x,y,z= i['pos']
        glPushMatrix()
        glTranslatef(x, y, z)
        glutSolidCube(8)
        glPopMatrix()

def fire_bullet():
    global bullets
    offset = 40.0
    bx = player_pos[0] + bullet_dir[0] * offset
    by = player_pos[1] + bullet_dir[1] * offset
    bz = bullet_height
    bullets.append({'pos': [bx, by, bz], 'dir': [bullet_dir[0], bullet_dir[1]]})

def update_bullets():

    global bullets, enemies, bullet_missed, game_over, game_score
    temp = []
    for b in bullets:
        b['pos'][0] += b['dir'][0] * bullet_speed
        b['pos'][1] += b['dir'][1] * bullet_speed

        x, y, z = b['pos']
        hit = False
        for idx, (ex, ey) in enumerate(enemies):
            dx = x - ex
            dy = y - ey
            if dx*dx + dy*dy <= enemy_hit_radius * enemy_hit_radius:
                enemies[idx] = random_enemy_pos()
                hit = True
                if not game_over:
                    game_score+=1
                break
        if hit:
            continue

        if not (-grid_half_size <= x <= grid_half_size and -grid_half_size <= y <= grid_half_size):
            if not game_over:
                bullet_missed+=1
            continue
        temp.append(b)
    bullets = temp

def check_game_over():
    global game_over
    if not game_over and (player_life <= 0 or bullet_missed >= max_bullet_missed):
        game_over = True

def reset_game():
    global player_life, bullet_missed, game_score, game_over, player_pos, gun_angle, bullets, enemies,bullet_dir
    
    player_life = 5
    bullet_missed = 0
    game_score = 0
    game_over = False
    player_pos[0] = 0.0
    player_pos[1] = 0.0
    gun_angle = 0.0
    bullet_dir[0] = 0.0
    bullet_dir[1] = -1.0
    bullets = []
    enemies = []
    init_enemies()



def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global player_pos, gun_angle, bullet_dir
    margin= 40
    limit= grid_half_size- margin

    # # Move forward (W key)
    if key == b'w':  
        # new_y= player_pos[1]- player_speed
        # player_pos[1]= max(-limit, new_y)
        step = player_speed   
        new_x = player_pos[0] + bullet_dir[0] * step
        new_y = player_pos[1] + bullet_dir[1] * step

        new_x = max(-limit, min(limit, new_x))
        new_y = max(-limit, min(limit, new_y))

        player_pos[0] = new_x
        player_pos[1] = new_y

    # # Move backward (S key)
    if key == b's':
        # new_y= player_pos[1]+ player_speed
        # player_pos[1]= min(limit, new_y)
        step = -player_speed
        new_x = player_pos[0] + bullet_dir[0] * step
        new_y = player_pos[1] + bullet_dir[1] * step

        new_x = max(-limit, min(limit, new_x))
        new_y = max(-limit, min(limit, new_y))

        player_pos[0] = new_x
        player_pos[1] = new_y

    # # Rotate gun left (A key)
    if key == b'a':
        gun_angle += rotate_speed
        dx, dy = bullet_dir
        bullet_dir[0] = dx * cos - dy * sin
        bullet_dir[1] = dx * sin + dy * cos

    # # Rotate gun right (D key)
    if key == b'd':
        gun_angle -= rotate_speed
        dx, dy = bullet_dir
        bullet_dir[0] = dx * cos + dy * sin
        bullet_dir[1] = -dx * sin + dy * cos

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    if key == b'r':
        reset_game()
        return



def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z+= 10
        if z>1200:
            z= 1200

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z-= 10
        if z< 80:
            z=80

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        # x -= 10  # Small angle decrement for smooth movement
        x1, y1 = x, y
        x = x1 * cos - y1 * sin
        y = x1 * sin + y1 * cos
    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        # x += 10  # Small angle increment for smooth movement
        x1, y1 = x, y
        x = x1 * cos + y1 * sin
        y = -x1 * sin + y1 * cos

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    global camera_pos, first_person
        # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()

        # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person= not first_person
        if not first_person:
            camera_pos= (0, 500, 500)


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    global camera_pos, first_person
    if first_person:
        cam_x = player_pos[0]
        cam_y = player_pos[1]
        cam_z = bullet_height + 5

        look_x = cam_x + bullet_dir[0] * 100
        look_y = cam_y + bullet_dir[1] * 100
        look_z = cam_z

        camera_pos = (cam_x, cam_y, cam_z)
        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 0, 1)

    else:
        x, y, z = camera_pos
        # Position the camera and set its orientation
        gluLookAt(x, y, z,  # Camera position
                0, 0, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    if not game_over:
        update_bullets()
        update_enemies()
        check_game_over()
        
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    
    # Draw the grid (game floor)
    grid_size= 10
    start= -(grid_size* GRID_LENGTH)/2

    glBegin(GL_QUADS)
    for i in range(grid_size):
        for j in range(grid_size):
            x1= start+ j*GRID_LENGTH
            x2= x1+ GRID_LENGTH
            y1= start+ i* GRID_LENGTH
            y2= y1+ GRID_LENGTH
            
            if (i+j)% 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()
    
    # Display game info text at a fixed screen position
    
    if game_over:
        draw_text(10, 740, "GAME OVER. PRESS 'R' To Restart The Game")
        draw_text(10, 710, f"Total Score: {game_score}")
    else:
        draw_text(10, 770, f"Player Life:{player_life}")
        draw_text(10, 740, f"Bullet Missed: {bullet_missed}")
        draw_text(10, 710, f"Game Score: {game_score}")

    draw_player()
    draw_boundaries()

    draw_enemies()
    draw_bullets()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    init_enemies()
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()