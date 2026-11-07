# THIS FILE IS THE SIMULATION PHYSICS (TRAJECTORIES AND PREDICTIONS) /!\

import math
import random

def start(x, y, heading, speed, target_speed, time_delta, target_heading, turn_timer, lenght, height, z, vertical_speed, target_vertical_speed, vertical_timer, turret_x, turret_y, turret_z, bullet_speed):

    # TARGET HANDLING
    turn_timer -= time_delta
    if turn_timer <= 0:
        target_heading = heading + random.uniform(-0.8, 0.8)
        turn_timer = random.uniform(0.2, 1)
        target_speed = random.uniform(40, 700)

    if x < 270 or x > lenght - 270 or y < 270 or y > height - 270:
        target_heading = math.atan2(height / 3 - y, lenght / 3 - x)

    # ALTITUDE
    vertical_timer -= time_delta
    if vertical_timer <= 0:
        target_vertical_speed = random.uniform(-30, 30)
        vertical_timer = random.uniform(1.0, 2.5)

    vertical_speed += (target_vertical_speed - vertical_speed) * min(1.0, time_delta * 0.8)
    z += vertical_speed * time_delta

    if z < 80:
        z = 80
        vertical_speed = max(0, vertical_speed)
        target_vertical_speed = max(0, target_vertical_speed)
    elif z > 400:
        z = 400
        vertical_speed = min(0, vertical_speed)
        target_vertical_speed = min(0, target_vertical_speed)
        
    angle_diff = math.atan2(math.sin(target_heading - heading), math.cos(target_heading - heading))
    turn_factor = 1 - 0.5 * min(abs(angle_diff) / (math.pi / 2), 1.0)
    desired_speed = target_speed * turn_factor
    max_turn = 2 * time_delta
    turn_step = max(-max_turn, min(angle_diff, max_turn))
    heading += turn_step
    speed += (desired_speed - speed) * min(1.0, time_delta * 0.5)

    x += math.cos(heading) * speed * time_delta
    y += math.sin(heading) * speed * time_delta

    # TURRET HANDLING
    distance = math.sqrt((x - turret_x) ** 2 + (y - turret_y) ** 2 + (z - turret_z) ** 2)
    flight_time = distance / bullet_speed
        
    turretadjx = math.cos(heading) * speed * flight_time
    turretadjy = math.sin(heading) * speed * flight_time

    return x, y, heading, target_heading, turn_timer, speed, target_speed, z, vertical_speed, target_vertical_speed, vertical_timer, turretadjx, turretadjy, flight_time