from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# ==========================================
# GLOBAL STATE & CONFIGURATION
# ==========================================

GAME_STATE_MENU = 0
GAME_STATE_SELECT = 4
GAME_STATE_PLAYING = 1
GAME_STATE_PAUSED = 2
GAME_STATE_GAMEOVER = 3
current_state = GAME_STATE_MENU

# Player Settings
LANE_WIDTH = 25
PLAYER_SPEED_BASE = 0.05
MAX_SPEED = 2.0

# Physics
JUMP_FORCE = 2.8   
GRAVITY = 0.04     

# Player Variables
player_pos = [0, 0, 0] 
player_lane = 0 
target_x = 0
y_velocity = 0
is_jumping = False
is_sliding = False
slide_timer = 0
anim_time = 0
run_speed = PLAYER_SPEED_BASE

# Stats
score = 0
lives = 3 
coins = 0

# Powerup States
powerup_shield = False
powerup_magnet = False
powerup_invis = False
magnet_timer = 0
invis_timer = 0

# === SPAWN TIMING ===
last_powerup_spawn_time = 0 

# === STUMBLE MECHANIC ===
stumble_mode = False
stumble_timer = 0

# Start Perks
start_immunity_timer = 0 
bombs_available = 0      

# === BOMB PROJECTILE STATE ===
# [x, y, z, active]
active_bomb = {'x': 0, 'y': 0, 'z': 0, 'active': False}

# Environment 
ENV_ROAD = 0
ENV_TUNNEL = 1
ENV_WATER = 2   
current_env = ENV_ROAD

# Objects
obstacles = [] 
coins_list = [] 
particles = [] 

# Camera
camera_z_offset = 50
camera_y_offset = 30
fov_val = 60

# ==========================================
# DRAWING FUNCTIONS
# ==========================================

def draw_text(x, y, text, r=1, g=1, b=1, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(r, g, b)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_cube(sx, sy, sz):
    glPushMatrix()
    glScalef(sx, sy, sz)
    glutSolidCube(1)
    glPopMatrix()

def draw_character():
    global player_pos, anim_time, is_jumping, is_sliding
    global powerup_shield, powerup_invis, start_immunity_timer
    global stumble_mode, current_env
    
    x, y, z = player_pos
    
    glPushMatrix()
    glTranslatef(x, y, z)
    
    tilt = 0
    if current_env == ENV_WATER:
        tilt = -90 
        glTranslatef(0, -2, 0)
    else:
        if is_sliding: 
            tilt = 90
        elif is_jumping: 
            tilt = 10
        else: 
            tilt = 10
        
    glRotatef(tilt, 1, 0, 0) 

    # Color Logic
    if powerup_invis:
        glColor4f(0.8, 0.8, 0.8, 0.4) 
    elif stumble_mode:
        if int(time.time() * 5) % 2 == 0:
            glColor3f(1.0, 0.0, 0.0) 
        else:
            glColor3f(0.2, 0.6, 1.0) 
    else:
        glColor3f(0.2, 0.6, 1.0) 

    # Body
    glPushMatrix()
    glTranslatef(0, 3, 0)
    if is_sliding and current_env != ENV_WATER:
        glScalef(1, 0.5, 1) 
    draw_cube(4, 6, 2)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 7, 0)
    if powerup_invis:
        glColor4f(0.8, 0.8, 0.8, 0.4)
    else:
        glColor3f(1, 0.8, 0.6) 
    glutSolidSphere(2, 16, 16)
    glPopMatrix()
    
    # Limbs 
    if not powerup_invis and not stumble_mode:
        glColor3f(0.1, 0.1, 0.8)

    leg_swing = math.sin(anim_time) * 10
    arm_swing = math.sin(anim_time) * 10
    
    if current_env == ENV_WATER:
        leg_swing = math.sin(anim_time * 2) * 10
        arm_swing = math.cos(anim_time * 2) * 30
    elif is_jumping:
        leg_swing = -10 
        arm_swing = -30 
    elif is_sliding:
        leg_swing = 10 

    glPushMatrix() # Left Leg
    glTranslatef(-1.5, 0, 0)
    glRotatef(leg_swing, 1, 0, 0)
    glTranslatef(0, -3, 0)
    draw_cube(1.5, 6, 1.5)
    glPopMatrix()

    glPushMatrix() # Right Leg
    glTranslatef(1.5, 0, 0)
    glRotatef(-leg_swing, 1, 0, 0)
    glTranslatef(0, -3, 0)
    draw_cube(1.5, 6, 1.5)
    glPopMatrix()

    glPushMatrix() # Arms
    glTranslatef(-3, 4, 0)
    glRotatef(-arm_swing, 1, 0, 0)
    glTranslatef(0, -2.5, 0)
    draw_cube(1.5, 5, 1.5)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(3, 4, 0)
    glRotatef(arm_swing, 1, 0, 0)
    glTranslatef(0, -2.5, 0)
    draw_cube(1.5, 5, 1.5)
    glPopMatrix()

    # --- SHIELD VISUAL ---
    is_start_immune = time.time() < start_immunity_timer
    if powerup_shield or is_start_immune:
        if is_start_immune: 
            glColor4f(1, 0.8, 0, 0.3) 
        else: glColor4f(0, 1, 1, 0.3) 
        glutSolidSphere(9, 20, 20)

    glPopMatrix()

def draw_thrown_bomb():
    """ Draws the bomb projectile moving forward """
    global active_bomb
    if not active_bomb['active']:
        return

    glPushMatrix()
    glTranslatef(active_bomb['x'], active_bomb['y'], active_bomb['z'])
    
    # Bomb Body (Black Sphere)
    glColor3f(0.1, 0.1, 0.1)
    glutSolidSphere(6, 15, 15)
    
    # Fuse (Red)
    glColor3f(1, 0, 0)
    glTranslatef(0, 5, 0)
    draw_cube(2, 4, 2)
    
    # Spark
    glColor3f(1, 1, 0)
    glTranslatef(0, 3, 0)
    glutSolidSphere(2, 8, 8)
    
    glPopMatrix()

def draw_environment():
    global player_pos, current_env
    
    start_z = int(player_pos[2] / 100) * 100 + 200
    end_z = start_z - 1000 

    dist = abs(player_pos[2])
    env_cycle = (dist // 3000) % 3
    if env_cycle == 0: current_env = ENV_ROAD
    elif env_cycle == 1: current_env = ENV_TUNNEL
    else: current_env = ENV_WATER

    for z in range(start_z, end_z, -100):
        glPushMatrix()
        glTranslatef(0, 0, z)
        
        if current_env == ENV_TUNNEL: 
            # Road
            glColor3f(0.2, 0.2, 0.2)
            glPushMatrix()
            glTranslatef(0, -5, 0) 
            glScalef(LANE_WIDTH * 3.5, 1, 100)
            glutSolidCube(1)
            glPopMatrix()

            # Cylinder Ring
            ring_radius = 50
            num_segments = 12
            if (abs(z) // 100) % 2 == 0: glColor3f(0.35, 0.35, 0.4)
            else: glColor3f(0.3, 0.3, 0.35)

            for i in range(num_segments):
                glPushMatrix()
                glRotatef(i * (360 / num_segments), 0, 0, 1)
                glTranslatef(0, ring_radius, 0)
                glScalef(20, 2, 100)
                glutSolidCube(1)
                glPopMatrix()

        elif current_env == ENV_WATER:
            # Water Colors
            if (abs(z)//100) % 2 == 0: glColor4f(0.0, 0.6, 1.0, 0.8)
            else: glColor4f(0.0, 0.5, 0.9, 0.8)
            
            # Floor
            glPushMatrix()
            glScalef(LANE_WIDTH * 3.5, 1, 100)
            glTranslatef(0, -5, 0.5)
            glutSolidCube(1)
            glPopMatrix()
            
            # Walls
            glColor4f(0.5, 0.8, 1.0, 0.3)
            glPushMatrix()
            glTranslatef(-LANE_WIDTH * 1.8, 5, 0)
            glScalef(2, 20, 100)
            glutSolidCube(1)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(LANE_WIDTH * 1.8, 5, 0)
            glScalef(2, 20, 100)
            glutSolidCube(1)
            glPopMatrix()

        else: # ENV_ROAD
            if (abs(z)//100) % 2 == 0: glColor3f(0.4, 0.4, 0.4)
            else: glColor3f(0.35, 0.35, 0.35)
            glScalef(LANE_WIDTH * 3.5, 1, 100)
            glTranslatef(0, -5, 0.5)
            glutSolidCube(1)
            
        glPopMatrix()

def draw_obstacles():
    global obstacles, player_pos
    for obs in obstacles:
        if obs['z'] > player_pos[2] + 20: continue
        if obs['z'] < player_pos[2] - 600: continue

        glPushMatrix()
        glTranslatef(obs['x'], obs['y'], obs['z'])
        
        if obs['type'] == 'JUMP': 
            glColor3f(1.0, 0.0, 0.0) 
            draw_cube(20, 5, 5) 
            glTranslatef(0, 2.6, 0)
            glColor3f(1, 1, 0)
            draw_cube(20, 0.5, 5)
        elif obs['type'] == 'SLIDE': 
            glColor3f(0.6, 0.0, 1.0)
            glPushMatrix()
            glTranslatef(0, 14, 0) 
            draw_cube(22, 10, 5)
            glPopMatrix()
            glColor3f(0.3, 0.3, 0.3)
            glPushMatrix()
            glTranslatef(-10, 5, 0)
            draw_cube(1, 20, 1)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(10, 5, 0)
            draw_cube(1, 20, 1)
            glPopMatrix()
        elif obs['type'] == 'FULL': 
            glColor3f(0.2, 0.2, 0.2)
            draw_cube(22, 30, 10)
            glColor3f(1, 0, 0)
            glPushMatrix()
            glTranslatef(0, 10, 5.1)
            glScalef(10, 1, 1)
            glutSolidCube(1)
            glPopMatrix()
        elif obs['type'] == 'SMALL':
            glColor3f(1.0, 0, 0.0) 
            glutSolidSphere(5, 20, 20) 

        glPopMatrix()

def draw_items():
    global coins_list, anim_time, player_pos
    for item in coins_list:
        if not item['active']: continue
        if item['z'] > player_pos[2] + 20: continue
        if item['z'] < player_pos[2] - 600: continue

        glPushMatrix()
        glTranslatef(item['x'], item['y'] + 5, item['z'])
        if item['type'] == 'COIN':
            glColor3f(1, 1, 0); glutSolidSphere(4,20,20)
        elif item['type'] == 'SHIELD':
            glColor3f(0, 1, 1); glutSolidCube(4)
        elif item['type'] == 'INVIS':
            glColor3f(0.9, 0.9, 0.9); glutSolidSphere(3, 10, 10)
        elif item['type'] == 'MAGNET':
            glColor3f(0, 1, 0); glutSolidSphere(4,20,20)
        glPopMatrix()

def draw_particles():
    global particles
    for p in particles:
        glPushMatrix()
        glTranslatef(p['x'], p['y'], p['z'])
        glColor3f(1, 0.5, 0) 
        glutSolidCube(p['size'])
        glPopMatrix()

# ==========================================
# LOGIC & PHYSICS
# ==========================================

def trigger_bomb():
    """ Spawns the bomb projectile """
    global obstacles, player_pos, bombs_available, active_bomb
    
    # Can only fire one at a time, and need ammo
    if bombs_available <= 0 or active_bomb['active']: 
        return
    
    bombs_available -= 1
    
    # Spawn bomb at player position
    active_bomb['active'] = True
    active_bomb['x'] = player_pos[0]
    active_bomb['y'] = player_pos[1] + 5
    active_bomb['z'] = player_pos[2] - 10 # slightly in front

    print("BOMB THROWN!")

def spawn_objects():
    global player_pos, obstacles, coins_list, last_powerup_spawn_time, current_env
    
    spawn_z = player_pos[2] - 800
    if len(obstacles) > 0 and obstacles[-1]['z'] < spawn_z + 150: return

    lanes = [-LANE_WIDTH, 0, LANE_WIDTH]
    chosen_lane = random.choice(lanes)
    r = random.random()
    current_time = time.time()
    
    # Powerups
    if current_time - last_powerup_spawn_time > 20:
        item_lane = random.choice(lanes)
        ptype = random.choice(['SHIELD', 'INVIS', 'MAGNET'])
        coins_list.append({'x': item_lane, 'y': 0, 'z': spawn_z, 'active': True, 'type': ptype})
        last_powerup_spawn_time = current_time
    else:
        if random.random() < 0.3: 
            item_lane = random.choice(lanes)
            if abs(item_lane - chosen_lane) > 1: 
                coins_list.append({'x': item_lane, 'y': 0, 'z': spawn_z, 'active': True, 'type': 'COIN'})

    # Obstacles
    if current_env == ENV_WATER:
        if r < 0.5: obstacles.append({'x': chosen_lane, 'y': 10, 'z': spawn_z, 'type': 'FULL'})
        else: obstacles.append({'x': chosen_lane, 'y': 0, 'z': spawn_z, 'type': 'SMALL'})     
    else:
        if r < 0.3: 
            obstacles.append({'x': chosen_lane, 'y': 2.5, 'z': spawn_z, 'type': 'JUMP'})
            coins_list.append({'x': chosen_lane, 'y': 15, 'z': spawn_z, 'active': True, 'type': 'COIN'})
        elif r < 0.6: 
            obstacles.append({'x': chosen_lane, 'y': 0, 'z': spawn_z, 'type': 'SLIDE'})
            coins_list.append({'x': chosen_lane, 'y': 0, 'z': spawn_z, 'active': True, 'type': 'COIN'})
        elif r < 0.8: obstacles.append({'x': chosen_lane, 'y': 0, 'z': spawn_z, 'type': 'SMALL'})
        else: obstacles.append({'x': chosen_lane, 'y': 10, 'z': spawn_z, 'type': 'FULL'})

def check_collisions():
    global player_pos, obstacles, coins_list, lives, current_state, particles, score, coins
    global powerup_shield, powerup_magnet, powerup_invis, start_immunity_timer
    global magnet_timer, invis_timer, stumble_mode, stumble_timer
    
    px, py, pz = player_pos
    player_width = 8
    
    for item in coins_list:
        if item['active']:
            if powerup_magnet and item['type'] == 'COIN':
                dist = math.sqrt((item['x'] - px)**2 + (item['z'] - pz)**2)
                if dist < 150:
                    item['x'] += (px - item['x']) * 0.15
                    item['y'] += (py - item['y']) * 0.15
                    item['z'] += (pz - item['z']) * 0.15

            dx = px - item['x']; dz = pz - item['z']; dy = py - item['y']
            if math.sqrt(dx*dx + dy*dy + dz*dz) < 15:
                item['active'] = False
                if item['type'] == 'COIN': 
                    score += 10; coins += 1
                    if coins >= 20: coins = 0; lives += 1; print("EXTRA LIFE EARNED!")      
                elif item['type'] == 'SHIELD': powerup_shield = True
                elif item['type'] == 'MAGNET': powerup_magnet = True; magnet_timer = time.time() + 10 
                elif item['type'] == 'INVIS': powerup_invis = True; invis_timer = time.time() + 10 

    if powerup_invis: return 
    if time.time() < start_immunity_timer: return 

    for obs in obstacles:
        dz = abs(pz - obs['z'])
        if dz < 6: 
            dx = abs(px - obs['x'])
            if dx < player_width:
                collision = False
                hit_type = obs['type']
                
                if hit_type == 'JUMP':
                    if py < 5: collision = True
                elif hit_type == 'SLIDE':
                    if not is_sliding: collision = True
                elif hit_type == 'FULL': collision = True
                elif hit_type == 'SMALL': collision = True

                if collision:
                    if hit_type == 'SMALL':
                        obs['z'] = 100 
                        if not stumble_mode: stumble_mode = True; stumble_timer = time.time() + 15
                        else:
                            if powerup_shield: powerup_shield = False
                            else: lives -= 1
                    else:
                        if powerup_shield: powerup_shield = False; obs['z'] = 100 
                        else:
                            lives -= 1; obs['z'] = 100 
                            for _ in range(20):
                                particles.append({'x': px, 'y': py+5, 'z': pz, 'vx': random.uniform(-2,2), 'vy': random.uniform(1,5), 'vz': random.uniform(-2,2), 'size': random.uniform(1,3)})
                    
                    if lives <= 0: current_state = GAME_STATE_GAMEOVER

def idle():
    global player_pos, target_x, y_velocity, is_jumping, is_sliding, slide_timer
    global anim_time, run_speed, score, current_state, lives, particles
    global powerup_magnet, magnet_timer, powerup_invis, invis_timer
    global stumble_mode, stumble_timer, current_env
    global active_bomb, obstacles
    
    if current_state != GAME_STATE_PLAYING:
        glutPostRedisplay()
        return

    # Update Environment
    dist = abs(player_pos[2])
    env_cycle = (dist // 3000) % 3
    if env_cycle == 0: current_env = ENV_ROAD
    elif env_cycle == 1: current_env = ENV_TUNNEL
    else: current_env = ENV_WATER

    # Movement
    target_speed = PLAYER_SPEED_BASE + (score / 50000.0)
    run_speed += (target_speed - run_speed) * 0.01
    player_pos[2] -= run_speed * 10
    score = abs(int(player_pos[2] / 10))
    player_pos[0] += (target_x - player_pos[0]) * 0.2
    
    # Gravity
    if is_jumping:
        player_pos[1] += y_velocity
        y_velocity -= GRAVITY 
        if player_pos[1] <= 0: player_pos[1] = 0; is_jumping = False

    if current_env == ENV_WATER and player_pos[1] > 0:
         player_pos[1] = 0; is_jumping = False
            
    if is_sliding:
        slide_timer -= 1
        if slide_timer <= 0: is_sliding = False
            
    anim_time += 0.2
    now = time.time()
    if powerup_magnet and now > magnet_timer: powerup_magnet = False
    if powerup_invis and now > invis_timer: powerup_invis = False
    if stumble_mode and now > stumble_timer: stumble_mode = False

    # === BOMB PROJECTILE LOGIC ===
    if active_bomb['active']:
        # Move bomb forward (faster than player)
        active_bomb['z'] -= 5 
        
        # Check if bomb is too far away
        if active_bomb['z'] < player_pos[2] - 1000:
            active_bomb['active'] = False
        
        # Check collision with obstacles
        for obs in obstacles:
            # Check Z distance
            if abs(obs['z'] - active_bomb['z']) < 25:
                # Explosion Effect!
                obs['z'] = 100 # Move obstacle away (destroy)
                
                # Spawn Particles at obstacle location
                for _ in range(10):
                    particles.append({
                        'x': obs['x'], 'y': 10, 'z': obs['z'],
                        'vx': random.uniform(-10, 10), 
                        'vy': random.uniform(5, 20), 
                        'vz': random.uniform(-10, 10),
                        'size': random.uniform(2, 4)
                    })

    # Particles
    for p in particles:
        p['x'] += p['vx']; p['y'] += p['vy']; p['z'] += p['vz']
        p['vy'] -= GRAVITY; p['size'] *= 0.9
        
    spawn_objects()
    check_collisions()
    
    if len(obstacles) > 0 and obstacles[0]['z'] > player_pos[2] + 100: obstacles.pop(0)
    coins_list[:] = [c for c in coins_list if c['z'] < player_pos[2] + 100 or c['z'] > player_pos[2] - 800]
    
    glutPostRedisplay()

# ==========================================
# INPUTS
# ==========================================

def keyboardListener(key, x, y):
    global player_lane, target_x, is_jumping, is_sliding, y_velocity, slide_timer
    global current_state, lives, score, coins, player_pos, obstacles, run_speed, coins_list
    global powerup_magnet, powerup_shield, powerup_invis, current_env
    global bombs_available, start_immunity_timer, stumble_mode, last_powerup_spawn_time
    global active_bomb
    
    if current_state == GAME_STATE_PLAYING:
        if key == b'a': 
            if player_lane > -1: player_lane -= 1; target_x = player_lane * LANE_WIDTH
        if key == b'd': 
            if player_lane < 1: player_lane += 1; target_x = player_lane * LANE_WIDTH
        
        if current_env != ENV_WATER :
            if key == b'w' and not is_jumping: 
                if current_env == 1: return # Limit jump in tunnel?
                is_jumping = True; y_velocity = JUMP_FORCE; is_sliding = False 
            if key == b's' and not is_jumping: 
                is_sliding = True; slide_timer = 120 
        
        if key == b'f': trigger_bomb()
        if key == b'p': current_state = GAME_STATE_PAUSED

    if current_state == GAME_STATE_MENU:
        if key == b' ': current_state = GAME_STATE_SELECT

    if current_state == GAME_STATE_SELECT:
        if key == b'1':
            start_immunity_timer = time.time() + 10; bombs_available = 0
            last_powerup_spawn_time = time.time(); current_state = GAME_STATE_PLAYING
        elif key == b'2':
            start_immunity_timer = 0; bombs_available = 3
            last_powerup_spawn_time = time.time(); current_state = GAME_STATE_PLAYING

    if key == b'r': 
        current_state = GAME_STATE_SELECT
        score = 0; lives = 3; coins = 0
        player_pos = [0,0,0]
        obstacles = []; coins_list = []
        is_jumping = False; target_x = 0; player_lane = 0; run_speed = PLAYER_SPEED_BASE
        powerup_magnet = False; powerup_shield = False; powerup_invis = False; stumble_mode = False
        bombs_available = 0; start_immunity_timer = 0
        active_bomb['active'] = False
        last_powerup_spawn_time = time.time() 

    if key == b'q': glutLeaveMainLoop()

def mouseListener(button, state, x, y):
    pass 

def setupCamera():
    global player_pos, camera_z_offset, camera_y_offset, fov_val
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    gluPerspective(fov_val, 800/600, 1, 3000)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    px, py, pz = player_pos
    cam_y = py + camera_y_offset
    cam_z = pz + camera_z_offset
    gluLookAt(0, cam_y, cam_z, 0, py + 10, pz - 100, 0, 1, 0)

def showScreen():
    global score, lives, coins, current_state
    global bombs_available, start_immunity_timer, stumble_mode, stumble_timer
    global current_env
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    if current_state == GAME_STATE_MENU:
        draw_text(300, 350, "ENDLESS RUNNER 3D", 1, 1, 0)
        draw_text(280, 300, "Press SPACE to Continue", 1, 1, 1)
        glutSwapBuffers()
        return

    if current_state == GAME_STATE_SELECT:
        draw_text(280, 400, "CHOOSE YOUR STARTING PERK:", 0, 1, 1)
        draw_text(250, 350, "[1] STARTING SHIELD", 1, 0.8, 0)
        draw_text(270, 330, "(Invincible for first 10 seconds)", 0.8, 0.8, 0.8)
        draw_text(250, 280, "[2] BOMBS", 1, 0, 0)
        draw_text(270, 260, "(Start with 3 Bombs. Press F to Clear Screen)", 0.8, 0.8, 0.8)
        glutSwapBuffers()
        return

    setupCamera()
    draw_environment()
    
    if current_state == GAME_STATE_PLAYING or current_state == GAME_STATE_PAUSED:
        draw_character()
        draw_thrown_bomb() # Draw the projectile
        
    draw_obstacles()
    draw_items() 
    draw_particles() 
        
    draw_text(10, 570, f"SCORE: {score}")
    draw_text(10, 540, f"LIVES: {lives}")
    draw_text(10, 510, f"COINS: {coins}", 1, 1, 0)
    
    y_off = 570
    if bombs_available > 0:
        draw_text(600, y_off, f"BOMBS (F): {bombs_available}", 1, 0, 0)
        y_off -= 30
    
    time_left = start_immunity_timer - time.time()
    if time_left > 0: draw_text(550, 50, f"START IMMUNITY: {int(time_left)}s", 1, 0.8, 0)

    if stumble_mode:
        draw_text(350, 400, "!!!", 1, 0, 0)
        draw_text(350, 380, f"{int(stumble_timer - time.time())}s", 1, 0, 0)

    if current_env == ENV_WATER:
         draw_text(320, 100, "WATER SLIDE!", 0, 1, 1)
         draw_text(300, 80, "No Jumping - Dodge Left/Right", 0.8, 0.8, 1)

    if powerup_shield: draw_text(600, y_off, "SHIELD ACTIVE", 0, 1, 1); y_off -= 30
    if powerup_magnet: draw_text(600, y_off, f"MAGNET: {int(magnet_timer - time.time())}s", 1, 0, 0); y_off -= 30
    if powerup_invis: draw_text(600, y_off, f"INVISIBLE: {int(invis_timer - time.time())}s", 0.8, 0.8, 0.8)

    if current_state == GAME_STATE_PAUSED: draw_text(350, 300, "PAUSED", 1, 1, 0)
    if current_state == GAME_STATE_GAMEOVER:
        draw_text(320, 350, "GAME OVER", 1, 0, 0)
        draw_text(280, 320, "Press R to Restart", 1, 1, 1)
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    wind = glutCreateWindow(b"3D Runner - Projectile Bomb")
    
    glClearColor(0.05, 0.1, 0.2, 1.0) 
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    main()