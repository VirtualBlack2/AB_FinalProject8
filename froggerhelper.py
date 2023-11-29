import arcade
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 50
VEHICLE_SIZE = 50
TURTLE_SIZE = 50
SAFE_ZONE_HEIGHT = 100


# Function to initialize vehicles
def create_vehicles():
    vehicles = arcade.SpriteList()
    for _ in range(5):
        vehicle = arcade.Sprite(":resources:images/enemies/fishGreen.png", 0.3)
        vehicle.center_x = random.randint(0, WINDOW_WIDTH)
        vehicle.center_y = random.randint(SAFE_ZONE_HEIGHT, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT)
        vehicles.append(vehicle)
    return vehicles


# Function to initialize turtles
def create_turtles():
    turtles = arcade.SpriteList()
    for _ in range(5):
        turtle = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.3)
        turtle.center_x = random.randint(0, WINDOW_WIDTH)
        turtle.center_y = random.randint(SAFE_ZONE_HEIGHT, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT)
        turtles.append(turtle)
    return turtles


# Function to initialize player
def create_player():
    player = arcade.Sprite("frog.png", 0.1)
    player.center_x = WINDOW_WIDTH // 2
    player.center_y = SAFE_ZONE_HEIGHT // 2
    return player
