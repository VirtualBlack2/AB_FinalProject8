

import arcade
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 50
VEHICLE_SIZE = 50
TURTLE_SIZE = 50
SAFE_ZONE_HEIGHT = 100

# Function to initialize vehicles
def create_vehicles(direction, count):
    vehicles = arcade.SpriteList()
    for _ in range(count):
        vehicle = arcade.Sprite("vehicle.png", 0.1)  # Updated to use vehicles.png
        vehicle.center_x = random.randint(0, WINDOW_WIDTH)
        vehicle.center_y = random.randint(SAFE_ZONE_HEIGHT, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT)
        vehicle.change_x = direction * 5  # Update to set the direction
        vehicles.append(vehicle)
    return vehicles

# Function to initialize turtles
def create_turtles(direction, count):
    turtles = arcade.SpriteList()
    for _ in range(count):
        turtle = arcade.Sprite("turtle.png", 0.1)  # Updated to use turtle.png
        turtle.center_x = random.randint(0, WINDOW_WIDTH)
        turtle.center_y = random.randint(SAFE_ZONE_HEIGHT, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT)
        turtle.change_x = direction * 3  # Update to set the direction
        turtles.append(turtle)
    return turtles

# Function to initialize player
def create_player():
    player = arcade.Sprite("frog.png", 0.1)  # Updated to use frog.png
    player.center_x = WINDOW_WIDTH // 2
    player.center_y = SAFE_ZONE_HEIGHT // 2
    return player
