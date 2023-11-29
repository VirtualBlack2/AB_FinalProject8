import arcade
import random
from froggerhelper import WINDOW_WIDTH
from froggerhelper import WINDOW_HEIGHT
from froggerhelper import PLAYER_SIZE
from froggerhelper import VEHICLE_SIZE
from froggerhelper import TURTLE_SIZE
from froggerhelper import SAFE_ZONE_HEIGHT
import froggerhelper

# Function to load images
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


class FroggerGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Frogger Game")
        arcade.set_background_color(arcade.color.BLACK)
        self.vehicles_left_to_right = create_vehicles()
        self.vehicles_right_to_left = create_vehicles()
        self.turtles_left_to_right = create_turtles()
        self.turtles_right_to_left = create_turtles()
        self.player = create_player()
        self.is_winner = False
        self.is_loser = False

    def on_draw(self):
        arcade.start_render()
        # Draw the safe zones, road, and river
        arcade.draw_rectangle_filled(WINDOW_WIDTH // 2, SAFE_ZONE_HEIGHT // 2, WINDOW_WIDTH, SAFE_ZONE_HEIGHT,
                                     arcade.color.GREEN)
        arcade.draw_rectangle_filled(WINDOW_WIDTH // 2, WINDOW_HEIGHT - SAFE_ZONE_HEIGHT // 2, WINDOW_WIDTH,
                                     SAFE_ZONE_HEIGHT, arcade.color.GREEN)
        arcade.draw_rectangle_filled(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, SAFE_ZONE_HEIGHT,
                                     arcade.color.BLUE)
        arcade.draw_rectangle_filled(WINDOW_WIDTH // 2, SAFE_ZONE_HEIGHT + SAFE_ZONE_HEIGHT // 2, WINDOW_WIDTH,
                                     SAFE_ZONE_HEIGHT, arcade.color.GRAY)

        # Draw sprites
        self.vehicles_left_to_right.draw()
        self.vehicles_right_to_left.draw()
        self.turtles_left_to_right.draw()
        self.turtles_right_to_left.draw()
        self.player.draw()

        # Draw game over messages
        if self.is_winner:
            arcade.draw_text("You Win!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, arcade.color.WHITE, font_size=50,
                             anchor_x="center")
        elif self.is_loser:
            arcade.draw_text("Game Over", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, arcade.color.RED, font_size=50,
                             anchor_x="center")

    def update(self, delta_time):
        if not self.is_winner and not self.is_loser:
            # Update vehicle and turtle positions
            self.vehicles_left_to_right.update()
            self.vehicles_right_to_left.update()
            self.turtles_left_to_right.update()
            self.turtles_right_to_left.update()

            # Check for collisions with vehicles
            if arcade.check_for_collision_with_list(self.player, self.vehicles_left_to_right) or \
                    arcade.check_for_collision_with_list(self.player, self.vehicles_right_to_left):
                self.is_loser = True
                arcade.play_sound(arcade.load_sound("lose_sound.wav"))

            # Check for collisions with turtles
            turtles_collided = arcade.check_for_collision_with_list(self.player,
                                                                    self.turtles_left_to_right + self.turtles_right_to_left)
            if turtles_collided:
                # Move player with the turtle
                for turtle in turtles_collided:
                    self.player.center_x += turtle.change_x
                    self.player.center_y += turtle.change_y

                # Check if the player has gone off the window while riding a turtle
                if self.player.center_x < 0 or self.player.center_x > WINDOW_WIDTH or \
                        self.player.center_y < SAFE_ZONE_HEIGHT or self.player.center_y > WINDOW_HEIGHT - SAFE_ZONE_HEIGHT:
                    self.is_loser = True
                    arcade.play_sound(arcade.load_sound("lose_sound.wav"))

            # Check if the player has reached the top safe zone
            if self.player.center_y > WINDOW_HEIGHT - SAFE_ZONE_HEIGHT // 2:
                self.is_winner = True
                arcade.play_sound(arcade.load_sound("win_sound.wav"))

    def on_key_press(self, key, modifiers):
        # Move the player when a key is pressed
        if key == arcade.key.W:
            self.player.change_y = PLAYER_SIZE
            arcade.play_sound(arcade.load_sound("jump_sound.wav"))

    def on_key_release(self, key, modifiers):
        # Stop player movement when a key is released
        if key == arcade.key.W:
            self.player.change_y = 0


if __name__ == "__main__":
    window = FroggerGame()
    arcade.run()
