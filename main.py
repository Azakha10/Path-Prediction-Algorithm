import pygame as pg
import pygame_gui as pggui
import pygame.gfxdraw
import math
import physics
import variables as v

pg.init()
icon = pg.image.load("icon.png")
pg.display.set_icon(icon)
pg.display.set_caption("Path Prediction")
screen = pg.display.set_mode((v.WINDOW_WIDTH, v.HEIGHT))
manager = pggui.UIManager((v.WINDOW_WIDTH, v.HEIGHT), "theme.json")
clock = pg.time.Clock()
running = True
start = False
start_button = pggui.elements.UIButton(relative_rect = pg.Rect(v.WINDOW_WIDTH-110, v.HEIGHT-60, 100, 50), text = "START", manager = manager)
font = pg.font.Font(None, 20)
font2 = pg.font.Font(None, 5)
bullets = []
hitmarks = []
HITMARK_DURATION = 0.5
fire_timer = 0.0
FIRE_INTERVAL = 0.25

def project_ground(x, y): # RETURNS ROUNDED COORDONATES
    offset_x = x - v.WIDTH / 2
    offset_y = y - v.HEIGHT / 2
    screen_x = v.WIDTH + v.WIDTH / 2 + (offset_x - offset_y) * 0.35
    ground_y = v.HEIGHT / 2 + (offset_x + offset_y) * 0.2
    return round(screen_x), round(ground_y)
        
while running:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if (event.type == pg.QUIT) | (keys[pg.K_ESCAPE]):
            running = False

        manager.process_events(event)

        if event.type == pggui.UI_BUTTON_PRESSED and event.ui_element == start_button and start == 0:
            print('-------------------------\n| INITIATING PREDICTION |\n-------------------------')
            start = True
            start_button.set_text("CLOSE")
        elif event.type == pggui.UI_BUTTON_PRESSED and event.ui_element == start_button and start == 1:
            print('----------------------\n| SIMULATION STOPPED |\n----------------------')
            running = False

    time_delta = clock.tick(100) / 1000.0
    manager.update(time_delta)
    screen.fill((7, 7, 7))
    manager.draw_ui(screen)
    pg.draw.line(screen, (80, 80, 80), (v.WIDTH, 0), (v.WIDTH, v.HEIGHT), 2)

# RENDERING ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    if (v.setup == 1):
        turret1 = pg.gfxdraw.aacircle(screen, v.beginning_x, v.beginning_y, 20, (15,200,15))
        turret2 = pg.draw.circle(screen, (15,200,15), v.beginning_pos, 2, 2)

    if (start == True):
        target_posx, target_posy, v.drone_heading, v.drone_target_heading, v.drone_turn_timer, v.drone_speed, v.drone_target_speed, v.drone_z, v.drone_vertical_speed, v.drone_target_vertical_speed, v.drone_vertical_timer, turretadjx, turretadjy, flight_time = physics.start(
            v.drone_x, v.drone_y, v.drone_heading, v.drone_speed, v.drone_target_speed, time_delta, v.drone_target_heading, v.drone_turn_timer, v.WIDTH, v.HEIGHT, v.drone_z, v.drone_vertical_speed, v.drone_target_vertical_speed, v.drone_vertical_timer, v.TURRET_X, v.TURRET_Y, v.TURRET_Z, v.BULLET_SPEED)
        v.drone_x = target_posx
        v.drone_y = target_posy
        target = pg.draw.circle(screen, (200,15,15), (round(target_posx), round(target_posy)), 10)
        v.setup = 0

    if (v.setup == 0):
        
        # LEFT WINDOW
        target = pg.draw.circle(screen, (200,15,15), (round(target_posx), round(target_posy)), 10)
        turret1 = pg.gfxdraw.aacircle(screen, round(target_posx) + round(turretadjx), round(target_posy) + round(turretadjy), 20, (15,200,15))
        turret2 = pg.draw.circle(screen, (15,200,15), (round(target_posx) + round(turretadjx), round(target_posy) + round(turretadjy)), 2, 2)
        #screen.blit(font.render("X", True, (15,120,15)), ((round(target_posx) + round(turretadjx)) - 8, (round(target_posy) + round(turretadjy)) - 8))

        # RIGHT WINDOW
        ground_corners = [project_ground(0, 0),project_ground(v.WIDTH, 0),project_ground(v.WIDTH, v.HEIGHT),project_ground(0, v.HEIGHT)]
        pg.draw.polygon(screen, (45, 150, 45), ground_corners, 2)
        turret_ground = project_ground(v.TURRET_X, v.TURRET_Y)
        pg.draw.circle(screen, (15, 200, 15), turret_ground, 4)
        screen_x, ground_y = project_ground(target_posx, target_posy)
        view3d_y = ground_y - (v.drone_z - 240) * 0.5
        pg.draw.line(screen, (15,120,15), (round(screen_x), round(ground_y)), (round(screen_x), round(view3d_y)), 4)
        pg.draw.circle(screen, (200, 15, 15), (round(screen_x), round(view3d_y)), 10)
        flight_text = font.render(f"Temps projectile : {flight_time:.2f} s",True,(180, 180, 180))
        drone_text = font.render(f"Drone : x={target_posx:.1f}, y={target_posy:.1f}, z={v.drone_z:.1f}", True, (180, 180, 180))
        screen.blit(drone_text, (v.WIDTH + 10, 35))
        
        # BULLETS VISUALIZATION
        aim_x = target_posx + math.cos(v.drone_heading) * v.drone_speed * flight_time
        aim_y = target_posy + math.sin(v.drone_heading) * v.drone_speed * flight_time
        aim_z = v.drone_z + v.drone_vertical_speed * flight_time
        
        fire_timer += time_delta
        while fire_timer >= FIRE_INTERVAL:
            fire_timer -= FIRE_INTERVAL
            bullets.append({
                "start": (v.TURRET_X, v.TURRET_Y, v.TURRET_Z),
                "end": (aim_x, aim_y, aim_z), "elapsed": 0.0, "duration": flight_time})
            
        active_bullets = []

        for bullet in bullets:
            bullet["elapsed"] += time_delta

            start_x, start_y, start_z = bullet["start"]
            end_x, end_y, end_z = bullet["end"]

            if bullet["elapsed"] >= bullet["duration"]:
                impact_distance = math.sqrt(
                    (end_x - target_posx) ** 2
                    + (end_y - target_posy) ** 2
                    + (end_z - v.drone_z) ** 2
                )
                if impact_distance <= 20:
                    hitmarks.append({
                        "position": (target_posx, target_posy, v.drone_z),
                        "elapsed": 0.0,
                    })
                continue

            progress = bullet["elapsed"] / bullet["duration"]
            start_x, start_y, start_z = bullet["start"]
            end_x, end_y, end_z = bullet["end"]

            bullet_x = start_x + (end_x - start_x) * progress
            bullet_y = start_y + (end_y - start_y) * progress
            bullet_z = start_z + (end_z - start_z) * progress

            end_screen_x, end_ground_y = project_ground(end_x, end_y)
            end_screen_y = end_ground_y - (end_z - 240) * 0.5

            bullet_screen_x = round(
                turret_ground[0] + (end_screen_x - turret_ground[0]) * progress)
            bullet_screen_y = round(
                turret_ground[1] + (end_screen_y - turret_ground[1]) * progress)

            pg.draw.circle(
                screen,
                (255, 230, 80),
                (bullet_screen_x, round(bullet_screen_y)),
                3,
            )
            active_bullets.append(bullet)

        bullets = active_bullets
        
        active_hitmarks = []

        for hitmark in hitmarks:
            hitmark["elapsed"] += time_delta
            if hitmark["elapsed"] >= HITMARK_DURATION:
                continue

            hit_x, hit_y, hit_z = hitmark["position"]

            # 2D VIEW BULLET
            pg.draw.line(
                screen, (255, 220, 40),
                (round(hit_x) - 6, round(hit_y) - 6),
                (round(hit_x) + 6, round(hit_y) + 6), 2
            )
            pg.draw.line(
                screen, (255, 220, 40),
                (round(hit_x) - 6, round(hit_y) + 6),
                (round(hit_x) + 6, round(hit_y) - 6), 2
            )

            # 3D VIEW BULLET
            mark_x, mark_ground_y = project_ground(hit_x, hit_y)
            mark_y = round(mark_ground_y - (hit_z - 240) * 0.5)
            pg.draw.line(screen, (255, 220, 40),
                         (mark_x - 6, mark_y - 6),
                         (mark_x + 6, mark_y + 6), 2)
            pg.draw.line(screen, (255, 220, 40),
                         (mark_x - 6, mark_y + 6),
                         (mark_x + 6, mark_y - 6), 2)

            active_hitmarks.append(hitmark)

        hitmarks = active_hitmarks
        
        aim_screen_x, aim_ground_y = project_ground(aim_x, aim_y)
        aim_screen_y = aim_ground_y - (aim_z - 240) * 0.5
        aim_point = (aim_screen_x, round(aim_screen_y))
        pg.draw.line(screen, (220, 200, 30), turret_ground, aim_point, 2)
        pg.draw.circle(screen, (220, 200, 30), aim_point, 6, 2)
        pg.draw.circle(screen, (15, 200, 15), turret_ground, 8)
    
        screen.blit(flight_text, (v.WIDTH + 10, 10))

    fps = round(clock.get_fps())
    screen.blit(font.render(f"FPS : {fps}", True, (120,120,120)), (7,7))
    pg.display.flip()

pg.quit()