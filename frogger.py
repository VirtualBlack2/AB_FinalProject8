
#modules
import arcade
import time


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SAFE_ZONE_HEIGHT = 100
WATER_COLOR = arcade.color.BLUE
ROAD_COLOR = arcade.color.GRAY
FROG_SIZE = 50
MOVEMENT_DISTANCE = 30
JUMP_SOUND_FILE = "jump_sound.wav"
WIN_SOUND_FILE = "win_sound.wav"
LOSE_SOUND_FILE = "lose_sound.wav"
# Constants


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
       self.lives = 3  #number of lives

       self.setup_lives_display()

       self.last_turtle = None
       self.has_jumped = False
       self.can_jump_to_safezone = False

       if self.turtle_sprites:
           self.last_turtle = self.turtle_sprites[0]

   def setup_lives_display(self):
        self.lives_label = arcade.Text(f"Lives: {self.lives}", 10, 10, arcade.color.BLACK, 16)

   def update_lives_display(self):
        self.lives_label.text = f"Lives: {self.lives}"

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

            if self.frog_sprite.center_y > SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2 and not self.on_turtle:
                self.handle_win()

            if self.frog_sprite.center_y < SAFE_ZONE_HEIGHT // 2 and not turtle_hit_list:
                self.handle_collision_lose()


            self.has_jumped = False

   def display_win_message(self):
        win_message = "YOU WIN!"
        self.win_message_sprite = arcade.Text(win_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                              arcade.color.GREEN, 40, align="center", anchor_x="center",
                                              anchor_y="center", width=SCREEN_WIDTH)
        self.win_message_sprite.draw()
        self.freeze_game()

   def handle_win(self):
       if self.frog_sprite.center_y > SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2 and not self.has_won:
           self.has_won = True
           print("You win!")
           arcade.play_sound(self.win_sound)
           self.freeze_game()



   def handle_collision_lose(self):
        current_time = time.time()
        if current_time - self.last_collision_time > 1:
            arcade.play_sound(self.lose_sound)
            self.last_collision_time = current_time

            self.lives -= 1
            self.update_lives_display()

            if self.lives <= 0:
                self.handle_game_over()
            else:
                # Reset the frog to the bottom if they have lives
                self.frog_sprite.center_x = SCREEN_WIDTH // 2
                self.frog_sprite.center_y = SAFE_ZONE_HEIGHT // 2

   def handle_game_over(self):
        print("Game Over! You lose!")

        # Freeze the game
        self.freeze_game()

        # Draw the "You lose!"
        arcade.draw_text("YOU LOSE!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.RED, 40, align="center", anchor_x="center", anchor_y="center")


   def handle_collision_ride(self, turtle):
       self.frog_sprite.center_x = turtle.center_x
       self.frog_sprite.center_y = turtle.center_y

#freeze the game if you die
   def freeze_game(self):
       self.game_state = "frozen"

#creating my safe zones with the grass.png image
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

#setup the turtles and directions
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

#setup the vehicles and directions
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


   def handle_game_over(self):
        print("Game Over!")
        self.freeze_game()

#draw out the images
   def on_draw(self):
        arcade.start_render()
        self.setup_water()
        self.setup_road()
        self.vehicle_sprites.draw()
        self.turtle_sprites.draw()
        self.safe_zone_sprites.draw()
        self.frog_sprite.draw()

        if hasattr(self, 'win_message_sprite'):
            self.win_message_sprite.draw()

        if self.game_state == "frozen" and self.lives <= 0:
            arcade.draw_text("YOU LOSE!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.RED, 40, width=SCREEN_WIDTH, align="center",
                             anchor_x="center", anchor_y="center")

        self.lives_label.draw()

   def display_win_message(self):
       win_message = "YOU WIN!"
       self.win_message_sprite = arcade.Text(win_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                             arcade.color.GREEN, 40, align="center", anchor_x="center",
                                             anchor_y="center", width=SCREEN_WIDTH)
       self.freeze_game()

#user key presses

   def on_key_press(self, key, modifiers):
        if self.game_state == "playing":
            if key == arcade.key.W and not self.has_jumped:
                # Check if the frog is on a turtle
                on_turtle = any(turtle.left <= self.frog_sprite.center_x <= turtle.right and turtle.bottom <= self.frog_sprite.center_y <= turtle.top for turtle in self.turtle_sprites)
                if on_turtle and not self.can_jump_to_safezone:

                    closest_turtle = min(self.turtle_sprites,
                                         key=lambda turtle: abs(self.frog_sprite.center_x - turtle.center_x))

                    # order of current turtle in the list
                    current_turtle_index = self.turtle_sprites.index(closest_turtle)

                    # Get the next turtle in the list
                    next_turtle_index = (current_turtle_index + 1) % len(self.turtle_sprites)
                    next_turtle = self.turtle_sprites[next_turtle_index]

                    # Jump only if on the closest turtle and the next turtle is in front
                    if (
                            closest_turtle.left <= self.frog_sprite.center_x <= closest_turtle.right
                            and closest_turtle.bottom <= self.frog_sprite.center_y <= closest_turtle.top
                            and self.frog_sprite.center_x < next_turtle.center_x
                    ):
                        self.frog_sprite.center_x = next_turtle.center_x
                        self.frog_sprite.center_y = next_turtle.center_y
                        self.on_turtle = True
                        self.can_jump_to_safezone = True
                else:
                    # Move upward if not on a turtle
                    self.frog_sprite.center_y += MOVEMENT_DISTANCE
                    self.on_turtle = False

                    # Check if the frog reaches the safezone
                    if self.frog_sprite.center_y > SCREEN_HEIGHT - SAFE_ZONE_HEIGHT // 2 and self.can_jump_to_safezone:
                        self.handle_win()
                        self.can_jump_to_safezone = False


                # Play jump sound
                arcade.play_sound(self.jump_sound)

            elif key == arcade.key.A:
                self.frog_sprite.center_x -= MOVEMENT_DISTANCE
                self.on_turtle = False
            elif key == arcade.key.S:
                self.frog_sprite.center_y -= MOVEMENT_DISTANCE
                self.on_turtle = False
            elif key == arcade.key.D:
                self.frog_sprite.center_x += MOVEMENT_DISTANCE
                self.on_turtle = False


#call the function
def main():
   print("Main function called")
   game = FroggerGame()
   arcade.run()


if __name__ == "__main__":
   main()

