import arcade
from froggerhelper import create_player, create_vehicles, create_turtles, WINDOW_WIDTH, WINDOW_HEIGHT, SAFE_ZONE_HEIGHT
from froggerhelper import update_vehicles, update_turtles

class FroggerGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Frogger Game")
        self.player = create_player()
        self.vehicles_left = create_vehicles(-1, 3)
        self.vehicles_right = create_vehicles(1, 3)
        self.turtles_left_sprites = create_turtles(-1, 3)
        self.turtles_right_sprites = create_turtles(1, 3)
        self.jump_sound = arcade.load_sound("jump_sound.wav")
        self.win_sound = arcade.load_sound("win_sound.wav")
        self.player_won = False
        self.win_text = arcade.Text("You Win!", self.width // 2, self.height // 2,
                                    arcade.color.BLACK, font_size=36, width=400, align="center", anchor_x="center")

    def setup(self):
        arcade.set_background_color(arcade.color.GO_GREEN)

    def on_draw(self):
        arcade.start_render()
        self.turtles_left_sprites.draw()
        self.turtles_right_sprites.draw()
        self.vehicles_left.draw()
        self.vehicles_right.draw()
        self.player.draw()

        if self.player_won:
            self.win_text.draw()

    def update(self, delta_time):
        if not self.player_won:
            update_vehicles(self.vehicles_left, -1)
            update_vehicles(self.vehicles_right, 1)
            update_turtles(self.turtles_left_sprites, -1)
            update_turtles(self.turtles_right_sprites, 1)

            self.player.update()

            for vehicle in self.vehicles_left:
                if vehicle.right < 0:
                    vehicle.left = self.width
            for vehicle in self.vehicles_right:
                if vehicle.left > self.width:
                    vehicle.right = 0

            # Check and reset turtles that move out of the window
            for turtle in self.turtles_left_sprites:
                if turtle.right < 0:
                    turtle.left = self.width
            for turtle in self.turtles_right_sprites:
                if turtle.left > self.width:
                    turtle.right = 0

            if arcade.check_for_collision_with_list(self.player, self.vehicles_left):
                self.reset_player_position()

            if arcade.check_for_collision_with_list(self.player, self.vehicles_right):
                self.reset_player_position()

            # Check for collisions with turtles
            if arcade.check_for_collision_with_list(self.player, self.turtles_left_sprites):
                self.reset_player_position()

            if arcade.check_for_collision_with_list(self.player, self.turtles_right_sprites):
                self.reset_player_position()

            # Check if the player has reached the top of the screen (win condition)
            if self.player.center_y > WINDOW_HEIGHT - SAFE_ZONE_HEIGHT:
                self.player_won = True
                arcade.play_sound(self.win_sound)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 5
            arcade.play_sound(self.jump_sound)
        elif key == arcade.key.A:
            self.player.change_x = -5
        elif key == arcade.key.D:
            self.player.change_x = 5
        elif key == arcade.key.S:
            self.player.change_y = -5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0

    def reset_player_position(self):
        self.player.center_x = WINDOW_WIDTH // 2
        self.player.center_y = SAFE_ZONE_HEIGHT // 2  # Reset player position
        arcade.play_sound(arcade.load_sound("lose_sound.wav"))

def main():
    window = FroggerGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
