#!/usr/bin/env python3
"""
multi_control_full.py  –  CARLA multi-vehicle controller + HUD + minimap

Tested on CARLA 0.9.15 / 0.10 quick build with Python 3.8-3.10
Requires:  pip install pygame
"""

import carla, pygame, random, math, time
from collections import deque

# ──────────────────────────────── Config ──────────────────────────────── #
NUM_VEHICLES   = 8              # how many to spawn (<= spawn points)
WINDOW_W, H    = 1280, 720
MINIMAP_SIZE   = 220            # px (square)
MINIMAP_MARGIN = 10
BIRDS_EYE_Z    = 60             # initial height (m)
# ──────────────────────────────────────────────────────────────────────── #

client = carla.Client('localhost', 2000); client.set_timeout(5.0)
world  = client.get_world()
bp_lib = world.get_blueprint_library().filter('vehicle.*')
spawn_pts = world.get_map().get_spawn_points()
random.shuffle(spawn_pts)

# spawn vehicles
vehicles = []
for i in range(min(NUM_VEHICLES, len(spawn_pts))):
    v = world.spawn_actor(random.choice(bp_lib), spawn_pts[i])
    v.set_autopilot(False)
    vehicles.append(v)
print(f"Spawned {len(vehicles)} vehicles")

# pygame init
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WINDOW_W, H))
pygame.display.set_caption("CARLA – Multi-vehicle controller")
font  = pygame.font.SysFont("consolas", 16)
clock = pygame.time.Clock()

# camera / spectator state
spectator = world.get_spectator()
cam_mode  = 0          # 0 bird's-eye, 1 chase, 2 driver
cam_yaw   = 0
cam_zoom  = BIRDS_EYE_Z

def set_camera(target):
    global cam_mode, cam_yaw, cam_zoom
    tf = target.get_transform()
    loc = tf.location; rot = tf.rotation
    if cam_mode == 0:                              # bird’s-eye
        location  = carla.Location(loc.x, loc.y, cam_zoom)
        rotation  = carla.Rotation(pitch=-90, yaw=cam_yaw, roll=0)
    elif cam_mode == 1:                            # chase
        back_vec  = tf.get_forward_vector() * -8   # 8 m behind
        location  = loc + back_vec + carla.Location(z=3)
        rotation  = carla.Rotation(pitch=-15, yaw=rot.yaw, roll=0)
    else:                                          # driver (dash)
        location  = loc + tf.get_forward_vector()*0.5 + carla.Location(z=1.2)
        rotation  = carla.Rotation(pitch=2, yaw=rot.yaw, roll=0)
    spectator.set_transform(carla.Transform(location, rotation))

# map bounds for minimap scaling
xs, ys = zip(*[(sp.location.x, sp.location.y) for sp in spawn_pts])
min_x, max_x = min(xs), max(xs); min_y, max_y = min(ys), max(ys)
map_w = max_x - min_x; map_h = max_y - min_y
scale = (MINIMAP_SIZE-20) / max(map_w, map_h)

def draw_minimap():
    surf = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
    surf.fill((30, 30, 30))
    # border
    pygame.draw.rect(surf, (200,200,200), surf.get_rect(), 1)
    for v in vehicles:
        p = v.get_location()
        mx = int((p.x - min_x) * scale) + 10
        my = int((p.y - min_y) * scale)
        my = MINIMAP_SIZE - (my + 10)              # invert Y for screen
        color = (255,50,50) if v.id == current.id else (50,200,255)
        pygame.draw.circle(surf, color, (mx, my), 4)
    screen.blit(surf, (MINIMAP_MARGIN, H - MINIMAP_SIZE - MINIMAP_MARGIN))

# vehicle control state
current_idx = 0
current     = vehicles[current_idx]
ctrl        = carla.VehicleControl()
switch_debounce = 0

print("Controls: WASD throttle/steer | C switch car | V switch cam | ESC quit")

running = True
while running:
    dt = clock.tick(60) / 1000.0
    switch_debounce = max(0, switch_debounce - dt)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE: running = False
            if ev.key == pygame.K_c and switch_debounce==0:
                current_idx = (current_idx + 1) % len(vehicles)
                current = vehicles[current_idx]; switch_debounce=0.2
            if ev.key == pygame.K_v and switch_debounce==0:
                cam_mode = (cam_mode + 1) % 3; switch_debounce=0.2
            if ev.key == pygame.K_SPACE:
                current.set_hand_brake(not current.get_control().hand_brake)
        if ev.type == pygame.MOUSEBUTTONDOWN and cam_mode==0:
            if ev.button==4: cam_zoom = max(15, cam_zoom-3)
            if ev.button==5: cam_zoom = min(120, cam_zoom+3)
        if ev.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and cam_mode==0:
            dx = ev.rel[0]; cam_yaw = (cam_yaw + dx*0.2) % 360

    # keys
    keys = pygame.key.get_pressed()
    ctrl.throttle = 1.0 if keys[pygame.K_w] else 0.0
    ctrl.brake    = 1.0 if keys[pygame.K_s] else 0.0
    steer = (-1 if keys[pygame.K_a] else 1 if keys[pygame.K_d] else 0)
    ctrl.steer = steer * 0.7
    current.apply_control(ctrl)

    # update camera
    set_camera(current)

    # draw HUD
    screen.fill((0,0,0))
    speed = 3.6 * current.get_velocity().length()
    hud_lines = [
        f"Vehicle ID : {current.id}",
        f"Speed      : {speed:5.1f} km/h",
        f"Camera     : {['Bird','Chase','Driver'][cam_mode]}",
        "Switch car : C   |  Camera mode : V"
    ]
    for i,l in enumerate(hud_lines):
        txt = font.render(l, True, (255,255,255))
        screen.blit(txt, (10, 10+i*18))

    # minimap
    draw_minimap()
    pygame.display.flip()

pygame.quit()
for v in vehicles: v.destroy()

