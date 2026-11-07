# THIS FILE EXISTS FOR CLARITY :) /!\

import math
import random

WINDOW_WIDTH = 1500
WIDTH = WINDOW_WIDTH // 2
HEIGHT = 800
TURRET_X = WIDTH / 2
TURRET_Y = HEIGHT / 2
TURRET_Z = 0
BULLET_SPEED = 1000

beginning_pos = (int(WIDTH/2), int(HEIGHT/2))
beginning_x = int(WIDTH/2)
beginning_y = int(HEIGHT/2)
randbeginning_pos_x = random.randint(150,WIDTH-150)
randbeginning_pos_y = random.randint(80,HEIGHT-80)
drone_x = randbeginning_pos_x
drone_y = randbeginning_pos_y
drone_z = random.uniform(150, 300)
drone_vertical_speed = random.uniform(-30, 30)
drone_target_vertical_speed = drone_vertical_speed
drone_vertical_timer = random.uniform(1.0, 2.5)
drone_heading = random.uniform(0, 2*math.pi)
drone_target_heading = drone_heading
drone_turn_timer = 0.0
drone_speed = random.uniform(50, 400)
drone_target_speed = drone_speed
updated_pos = 0
updated_pos_x = 0
updated_pos_y = 0
targetadjx = 0
targetadjy = 0
target_posx = 0
target_posy = 0
turretadjx = 0
turretadjy = 0
setup = 1