from cmu_graphics import *

# Define constants
WIDTH = 800
HEIGHT = 600
TANK_SIZE = 40
BULLET_SIZE = (4, 6)
BRICK_SIZE = 20

# Tank properties
tank_x = WIDTH // 2
tank_y = HEIGHT // 2
tank_speed = 5

# Bullet properties
bullet_x = -10
bullet_y = -10
bullet_speed = 8
bullet_active = False

# Wall properties
wall_x = WIDTH // 2
wall_y = HEIGHT // 3
wall_width = 200
wall_height = 100
wall_visible = True

def draw():
    global tank_x, tank_y, bullet_x, bullet_y, bullet_active, wall_x, wall_y, wall_visible

    # Draw tank
    draw_rect(tank_x - TANK_SIZE // 2, tank_y - TANK_SIZE // 2, TANK_SIZE, TANK_SIZE, "green")

    # Draw bullet if active
    if bullet_active:
        draw_rect(bullet_x - BULLET_SIZE[0] // 2, bullet_y - BULLET_SIZE[1] // 2, BULLET_SIZE[0], BULLET_SIZE[1], "red")

    # Draw wall if visible
    if wall_visible:
        draw_rect(wall_x - wall_width // 2, wall_y - wall_height // 2, wall_width, wall_height, "blue")

def update():
    global tank_x, tank_y, bullet_x, bullet_y, bullet_active, wall_visible

    # Move the bullet if it's active
    if bullet_active:
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_active = False

        # Check bullet collision with wall
        if wall_visible and (
            wall_x - wall_width // 2 < bullet_x < wall_x + wall_width // 2
            and wall_y - wall_height // 2 < bullet_y < wall_y + wall_height // 2
        ):
            bullet_active = False
            wall_visible = False
            # Implement wall explosion animation here

    # Handle user input and prevent tank from going through the wall
    if is_key_pressed("w") and tank_y > TANK_SIZE // 2:
        tank_y -= tank_speed
    elif is_key_pressed("s") and tank_y < HEIGHT - TANK_SIZE // 2:
        tank_y += tank_speed
    elif is_key_pressed("a") and tank_x > TANK_SIZE // 2:
        tank_x -= tank_speed
    elif is_key_pressed("d") and tank_x < WIDTH - TANK_SIZE // 2:
        tank_x += tank_speed

start_graphics(draw, update, width=WIDTH, height=HEIGHT)
