import pygame
import random

# Initialize the game
pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Frogger Game")

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Set the frog dimensions
frog_width = 50
frog_height = 50

# Set the frog's initial position
frog_x = screen_width // 2 - frog_width // 2
frog_y = screen_height - frog_height

# Set the frog's movement speed
frog_speed = 5

# Set the car dimensions
car_width = 100
car_height = 50

# Set the car's initial position and movement speed
car_x = random.randint(0, screen_width - car_width)
car_y = random.randint(0, screen_height // 2 - car_height)
car_speed = random.randint(1, 5)

# Set the game clock
clock = pygame.time.Clock()

def draw_frog(x, y):
    """
    Draw the frog on the screen.

    Args:
    - x (int): The x-coordinate of the frog's position.
    - y (int): The y-coordinate of the frog's position.
    """
    pygame.draw.rect(screen, green, (x, y, frog_width, frog_height))

def draw_car(x, y):
    """
    Draw the car on the screen.

    Args:
    - x (int): The x-coordinate of the car's position.
    - y (int): The y-coordinate of the car's position.
    """
    pygame.draw.rect(screen, red, (x, y, car_width, car_height))

def game_loop():
    """
    The main game loop.
    """
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Move the frog based on user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            frog_x -= frog_speed
        if keys[pygame.K_RIGHT]:
            frog_x += frog_speed
        if keys[pygame.K_UP]:
            frog_y -= frog_speed
        if keys[pygame.K_DOWN]:
            frog_y += frog_speed

        # Move the car
        car_x += car_speed

        # Check for collision between the frog and the car
        if frog_x < car_x + car_width and frog_x + frog_width > car_x and frog_y < car_y + car_height and frog_y + frog_height > car_y:
            game_over = True

        # Check if the frog has reached the top of the screen
        if frog_y < 0:
            game_over = True

        # Check if the car has reached the right edge of the screen
        if car_x > screen_width:
            car_x = 0
            car_y = random.randint(0, screen_height // 2 - car_height)
            car_speed = random.randint(1, 5)

        # Clear the screen
        screen.fill(black)

        # Draw the frog and the car
        draw_frog(frog_x, frog_y)
        draw_car(car_x, car_y)

        # Update the display
        pygame.display.update()

        # Set the frames per second
        clock.tick(60)

    # Quit the game
    pygame.quit()

# Start the game loop
game_loop()