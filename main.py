import arcade
from froggerhelper import WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE, VEHICLE_SIZE, TURTLE_SIZE, SAFE_ZONE_HEIGHT
from froggerhelper import create_vehicles, create_turtles, create_player


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

        # Load sounds during initialization
        self.jump_sound = arcade.load_sound("jump_sound.wav")
        self.win_sound = arcade.load_sound("win_sound.wav")
        self.lose_sound = arcade.load_sound("lose_sound.wav")

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

            # Check for collisions with turtles
            turtles_collided_left = arcade.check_for_collision_with_list(self.player, self.turtles_left_to_right)
            turtles_collided_right = arcade.check_for_collision_with_list(self.player, self.turtles_right_to_left)

            # Check if the player has collided with any turtles
            if turtles_collided_left or turtles_collided_right:
                self.is_loser = True
                arcade.play_sound(self.lose_sound)

            # Check if the player has reached the top safe zone
            if self.player.center_y > WINDOW_HEIGHT - SAFE_ZONE_HEIGHT // 2:
                self.is_winner = True
                arcade.play_sound(self.win_sound)

            # Update player position
            self.player.update()

    def on_key_press(self, symbol, modifiers):
        # Move the player when a key is pressed
        if symbol == arcade.key.W:
            self.player.change_y = 5  # Adjust the speed as needed
            arcade.play_sound(self.jump_sound)
        elif symbol == arcade.key.A:
            self.player.change_x = -5
        elif symbol == arcade.key.D:
            self.player.change_x = 5

    def on_key_release(self, symbol, modifiers):
        # Stop player movement when a key is released
        if symbol == arcade.key.W:
            self.player.change_y = 0
        elif symbol == arcade.key.A or symbol == arcade.key.D:
            self.player.change_x = 0


def main():
    window = FroggerGame()
    arcade.run()


if __name__ == "__main__":
    main()
