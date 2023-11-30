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
        vehicle = arcade.Sprite("vehicle.png", 0.1)
        if direction == -1:
            vehicle.center_x = random.randint(WINDOW_WIDTH // 2, WINDOW_WIDTH)
        else:
            vehicle.center_x = random.randint(0, WINDOW_WIDTH // 2)
        vehicle.center_y = random.randint(SAFE_ZONE_HEIGHT, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT)
        vehicles.append(vehicle)
    return vehicles


# Function to initialize turtles
def create_turtles(direction, count):
    turtles = arcade.SpriteList()
    for _ in range(count):
        turtle = arcade.Sprite("turtle.png", 0.1)
        if direction == -1:
            turtle.center_x = random.randint(WINDOW_WIDTH // 2, WINDOW_WIDTH)
        else:
            turtle.center_x = random.randint(0, WINDOW_WIDTH // 2)
        turtle.center_y = random.randint(SAFE_ZONE_HEIGHT, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT)
        turtles.append(turtle)
    return turtles

# Function to initialize player
def create_player():
    player = arcade.Sprite("frog.png", 0.1)
    player.center_x = WINDOW_WIDTH // 2
    player.center_y = SAFE_ZONE_HEIGHT // 2
    return player


# Function to update vehicles' positions
def update_vehicles(vehicles, direction):
    for vehicle in vehicles:
        if direction == -1:
            vehicle.center_x -= 1
            if vehicle.right < 0:
                vehicle.left = WINDOW_WIDTH // 2
        else:
            vehicle.center_x += 1
            if vehicle.left > WINDOW_WIDTH // 2:
                vehicle.right = WINDOW_WIDTH


# Function to update turtles' positions
def update_turtles(turtles, direction):
    for turtle in turtles:
        if direction == -1:
            turtle.center_x -= 1
            if turtle.right < 0:
                turtle.left = WINDOW_WIDTH // 2
        else:
            turtle.center_x += 1
            if turtle.left > WINDOW_WIDTH // 2:
                turtle.right = WINDOW_WIDTH
