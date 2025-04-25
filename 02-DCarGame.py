from ursina import *
from panda3d.core import loadPrcFileData
import random

# Config window
loadPrcFileData('', 'win-size 400 600')
loadPrcFileData('', 'window-title 2D Car Game')
loadPrcFileData('', 'fullscreen false')

app = Ursina()

# Camera setup
camera.orthographic = True
camera.fov = 20
window.color = color.black

# Scrolling road background using two quads
road1 = Entity(model='quad', texture='road.png', scale=(16, 20), y=0, z=1)
road2 = Entity(model='quad', texture='road.png', scale=(16, 20), y=20, z=1)

# Car
car = Entity(model='quad', texture='car.png', scale=(1.5, 3), rotation_z=0, y=-8, collider='box')

# Booster Flames
booster_red = Entity(model='quad', color=color.red, scale=(0.5, 1), position=(0, -9.5), enabled=False)
booster_yellow = Entity(model='quad', color=color.yellow, scale=(0.3, 0.8), position=(0, -9.8), enabled=False)

# Enemy
enemy = Entity(model='quad', texture='enemy.png', scale=(1.5, 3), rotation_z=0, y=8, collider='box')

# Health bar
max_health = 3
health = max_health
health_bar = Entity(model='quad', color=color.green, scale=(max_health, 0.5), position=(0, 9))

# Game over text
game_over_text = Text(text='GAME OVER', scale=2, color=color.red, origin=(0, 0), visible=False)

# Speed variables
normal_scroll_speed = 2
boosted_scroll_speed = 6
scroll_speed = normal_scroll_speed

# Reset enemy position
def reset_enemy():
    enemy.x = random.uniform(-7, 7)
    enemy.y = 9

reset_enemy()

# Game logic
def update():
    global health, scroll_speed

    if health <= 0:
        return

    # Car movement
    if held_keys['left arrow'] and car.x > -7:
        car.x -= 5 * time.dt
    if held_keys['right arrow'] and car.x < 7:
        car.x += 5 * time.dt

    # Boost effect
    if held_keys['up arrow']:
        scroll_speed = boosted_scroll_speed
        booster_red.enabled = True
        booster_yellow.enabled = True
        booster_red.x = booster_yellow.x = car.x
    else:
        scroll_speed = normal_scroll_speed
        booster_red.enabled = False
        booster_yellow.enabled = False

    # Enemy movement
    enemy.y -= 4 * time.dt
    if enemy.y < -9:
        reset_enemy()

    # Collision check
    if car.intersects(enemy).hit:
        health -= 1
        health_bar.scale_x = max(0, health)
        reset_enemy()
        if health <= 0:
            game_over_text.visible = True
            health_bar.color = color.red

    # Scroll road
    road1.y -= scroll_speed * time.dt
    road2.y -= scroll_speed * time.dt

    # Reset roads to loop infinitely
    if road1.y <= -20:
        road1.y = 20
    if road2.y <= -20:
        road2.y = 20

# Screenshot
def input(key):
    if key == 's':
        screenshot('car_model.png')
        print("Screenshot saved as car_model.png")

app.run()
# opengl = translation +rotation 
#percetive = 3 d perceptive 
#2d game =panning