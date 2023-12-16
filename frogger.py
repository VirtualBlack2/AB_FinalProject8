import arcade
import time


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SAFE_ZONE_HEIGHT = 100
WATER_COLOR = arcade.color.BLUE
ROAD_COLOR = arcade.color.GRAY
FROG_SIZE = 50
MOVEMENT_DISTANCE = 25
JUMP_SOUND_FILE = "jump_sound.wav"
WIN_SOUND_FILE = "win_sound.wav"
LOSE_SOUND_FILE = "lose_sound.wav"


class Turtle(arcade.Sprite):
   def __init__(self, image_file, scale, speed, start_x, start_y):
       super().__init__(image_file, scale)
       self.center_x = start_x
       self.center_y = start_y
       self.change_x = speed


   def update(self):
       super().update()


       if self.right < 0:
           self.left = SCREEN_WIDTH


       if self.left > SCREEN_WIDTH:
           self.right = 0


class Vehicle(arcade.Sprite):
   def __init__(self, image_file, scale, speed, start_x, start_y):
       super().__init__(image_file, scale)
       self.center_x = start_x
       self.center_y = start_y
       self.change_x = speed


   def update(self):
       super().update()


       if self.right < 0:
           self.left = SCREEN_WIDTH


       if self.left > SCREEN_WIDTH:
           self.right = 0


class FroggerGame(arcade.Window):
   def __init__(self):
       super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Frogger Game")
       arcade.set_background_color(arcade.color.WHITE)


       self.setup_safe_zones()
       self.setup_water()
       self.setup_road()
       self.setup_frog()
       self.setup_turtles()
       self.setup_vehicles()


       self.jump_sound = arcade.load_sound(JUMP_SOUND_FILE)
       self.win_sound = arcade.load_sound(WIN_SOUND_FILE)
       self.has_won = False
       self.lose_sound = arcade.load_sound(LOSE_SOUND_FILE)
       self.game_state = "playing"


       self.last_collision_time = 0


   def on_update(self, delta_time):
       if self.game_state != "frozen":
           self.vehicle_sprites.update()
           self.turtle_sprites.update()


           for vehicle in self.vehicle_sprites:
               if arcade.check_for_collision(self.frog_sprite, vehicle):
                   self.handle_collision_lose()


           turtle_hit_list = arcade.check_for_collision_with_list(self.frog_sprite, self.turtle_sprites)
           if turtle_hit_list:
               self.handle_collision_ride(turtle_hit_list[0])


           if self.frog_sprite.center_y > SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2 and not self.has_won:
               self.handle_win()


           if self.frog_sprite.center_y < SAFE_ZONE_HEIGHT // 2 and not turtle_hit_list:
               self.handle_collision_lose()


   def handle_win(self):
       if self.frog_sprite.center_y > SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2 and not self.has_won:
           self.has_won = True
           print("You win!")
           arcade.play_sound(self.win_sound)
           self.freeze_game()


   def handle_collision_lose(self):
       print("You lose!")


       current_time = time.time()
       if current_time - self.last_collision_time > 1:
           arcade.play_sound(self.lose_sound)
           self.last_collision_time = current_time


           lose_message = "YOU LOSE!"
           self.lose_message_sprite = arcade.Text(lose_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                                  arcade.color.RED, 40, align="center", anchor_x="center",
                                                  anchor_y="center", width=SCREEN_WIDTH)


           self.frog_sprite.change_x = 0
           self.frog_sprite.change_y = 0


           self.game_state = "lost"
           self.freeze_game()


   def handle_collision_ride(self, turtle):
       self.frog_sprite.center_x = turtle.center_x
       self.frog_sprite.center_y = turtle.center_y


   def freeze_game(self):
       self.game_state = "frozen"


   def setup_safe_zones(self):
       top_safe_zone = arcade.Sprite("grass.png", center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2)
       top_safe_zone.height = SAFE_ZONE_HEIGHT
       top_safe_zone.width = SCREEN_WIDTH


       bottom_safe_zone = arcade.Sprite("grass.png", center_x=SCREEN_WIDTH // 2, center_y=SAFE_ZONE_HEIGHT // 2)
       bottom_safe_zone.height = SAFE_ZONE_HEIGHT
       bottom_safe_zone.width = SCREEN_WIDTH


       middle_safe_zone = arcade.Sprite("grass.png", center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2)
       middle_safe_zone.height = SAFE_ZONE_HEIGHT
       middle_safe_zone.width = SCREEN_WIDTH


       top_safe_zone.center_x = SCREEN_WIDTH // 2
       top_safe_zone.center_y = SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2


       bottom_safe_zone.center_x = SCREEN_WIDTH // 2
       bottom_safe_zone.center_y = SAFE_ZONE_HEIGHT // 2


       middle_safe_zone.center_x = SCREEN_WIDTH // 2
       middle_safe_zone.center_y = SCREEN_HEIGHT // 2


       self.safe_zone_sprites = arcade.SpriteList()
       self.safe_zone_sprites.extend([top_safe_zone, bottom_safe_zone, middle_safe_zone])


   def setup_water(self):
       water_top = SCREEN_HEIGHT - SAFE_ZONE_HEIGHT
       water_bottom = SCREEN_HEIGHT // 2


       arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, water_top, water_bottom, WATER_COLOR)


   def setup_road(self):
       road_top = SCREEN_HEIGHT // 2
       road_bottom = SAFE_ZONE_HEIGHT


       arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, road_top, road_bottom, ROAD_COLOR)


   def setup_frog(self):
       self.frog_sprite = arcade.Sprite("frog.png", 0.02)
       self.frog_sprite.center_x = SCREEN_WIDTH // 2
       self.frog_sprite.center_y = SAFE_ZONE_HEIGHT // 2


   def setup_turtles(self):
       self.turtle_sprites = arcade.SpriteList()


       turtle1_image = "turtle.png"
       turtle2_image = "turtle2.png"
       turtle_scale = 0.3
       turtle_speed = 2


       turtle1 = Turtle(turtle1_image, turtle_scale, -turtle_speed, 100, SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2 - 80)
       turtle2 = Turtle(turtle1_image, turtle_scale, -turtle_speed, 400, SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2 - 80)
       turtle3 = Turtle(turtle1_image, turtle_scale, -turtle_speed, 700, SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2 - 80)


       self.turtle_sprites.extend([turtle1, turtle2, turtle3])


       turtle4 = Turtle(turtle2_image, turtle_scale, turtle_speed, SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2 - -80)
       turtle5 = Turtle(turtle2_image, turtle_scale, turtle_speed, SCREEN_WIDTH - 400, SCREEN_HEIGHT // 2 - -80)
       turtle6 = Turtle(turtle2_image, turtle_scale, turtle_speed, SCREEN_WIDTH - 700, SCREEN_HEIGHT // 2 - -80)


       self.turtle_sprites.extend([turtle4, turtle5, turtle6])


   def setup_vehicles(self):
       self.vehicle_sprites = arcade.SpriteList()


       vehicle1_image = "vehicle.png"
       vehicle2_image = "vehicle2.png"
       vehicle_scale = 0.06
       vehicle_speed = 1


       vehicle1 = Vehicle(vehicle1_image, vehicle_scale, -vehicle_speed, 100, SCREEN_HEIGHT // 2 - 150)
       vehicle2 = Vehicle(vehicle1_image, vehicle_scale, -vehicle_speed, 400, SCREEN_HEIGHT // 2 - 150)
       vehicle3 = Vehicle(vehicle1_image, vehicle_scale, -vehicle_speed, 700, SCREEN_HEIGHT // 2 - 150)


       self.vehicle_sprites.extend([vehicle1, vehicle2, vehicle3])


       vehicle4 = Vehicle(vehicle2_image, -vehicle_scale, vehicle_speed, SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2 - 75)
       vehicle5 = Vehicle(vehicle2_image, -vehicle_scale, vehicle_speed, SCREEN_WIDTH - 400, SCREEN_HEIGHT // 2 - 75)
       vehicle6 = Vehicle(vehicle2_image, -vehicle_scale, vehicle_speed, SCREEN_WIDTH - 700, SCREEN_HEIGHT // 2 - 75)


       self.vehicle_sprites.extend([vehicle4, vehicle5, vehicle6])


   def on_draw(self):
       arcade.start_render()
       self.setup_water()
       self.setup_road()
       self.vehicle_sprites.draw()
       self.turtle_sprites.draw()
       self.safe_zone_sprites.draw()
       self.frog_sprite.draw()


       if hasattr(self, 'lose_message_sprite'):
           self.lose_message_sprite.draw()


   def on_key_press(self, key, modifiers):
       if self.game_state == "playing":
           # Move the frog when WASD keys are pressed with the adjusted movement distance
           if key == arcade.key.W:
               self.frog_sprite.center_y += MOVEMENT_DISTANCE
           elif key == arcade.key.A:
               self.frog_sprite.center_x -= MOVEMENT_DISTANCE
           elif key == arcade.key.S:
               self.frog_sprite.center_y -= MOVEMENT_DISTANCE
           elif key == arcade.key.D:
               self.frog_sprite.center_x += MOVEMENT_DISTANCE


           # Play jump sound
           arcade.play_sound(self.jump_sound)


def main():
   print("Main function called")
   game = FroggerGame()
   arcade.run()


if __name__ == "__main__":
   main()
