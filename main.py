

import arcade
from froggerhelper import create_player, create_vehicles, create_turtles

class FroggerGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Frogger Game")
        self.player = create_player()
        self.vehicles_left = create_vehicles(-1, 3)
        self.vehicles_right = create_vehicles(1, 3)
        self.turtles_left_sprites = create_turtles(-1, 3)
        self.turtles_right_sprites = create_turtles(1, 3)
        self.jump_sound = arcade.load_sound("jump_sound.wav")

    def setup(self):
        arcade.set_background_color(arcade.color.BLUE)

    def on_draw(self):
        arcade.start_render()
        self.turtles_left_sprites.draw()
        self.turtles_right_sprites.draw()
        self.vehicles_left.draw()
        self.vehicles_right.draw()
        self.player.draw()

    def update(self, delta_time):
        self.turtles_left_sprites.update()
        self.turtles_right_sprites.update()
        self.vehicles_left.update()
        self.vehicles_right.update()
        self.player.update()

        # Check for collisions here

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

def main():
    window = FroggerGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
