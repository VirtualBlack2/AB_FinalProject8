import random

import arcade

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 50
VEHICLE_SIZE = 50
TURTLE_SIZE = 50
SAFE_ZONE_HEIGHT = 100


def load_image(file_path, scale):
    return arcade.load_texture(file_path, scale=scale)

# Function to initialize vehicles
def create_vehicles():
    vehicles = arcade.SpriteList()
    for _ in range(5):
        vehicle = arcade.Sprite("vehicle.png", 0.5)
        vehicle.center_x = random.randint(0, WINDOW_WIDTH)
        vehicle.center_y = random.randint(SAFE_ZONE_HEIGHT, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT)
        vehicles.append(vehicle)
    return vehicles

# Function to initialize turtles
def create_turtles():
    turtles = arcade.SpriteList()
    for _ in range(5):
        turtle = arcade.Sprite("turtle.png", 0.5)
        turtle.center_x = random.randint(0, WINDOW_WIDTH)
        turtle.center_y = random.randint(SAFE_ZONE_HEIGHT, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT)
        turtles.append(turtle)
    return turtles

# Function to initialize player
def create_player():
    player = arcade.Sprite("frog.png", 0.5)
    player.center_x = WINDOW_WIDTH // 2
    player.center_y = SAFE_ZONE_HEIGHT // 2
    return player

player = create_player()
vehicles_left_to_right = create_vehicles()
vehicles_right_to_left = create_vehicles()
turtles_left_to_right = create_turtles()
turtles_right_to_left = create_turtles()

