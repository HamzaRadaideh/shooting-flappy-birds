import random
import sys
import pygame

from shooting_flappy_birds.AudioSettings import AudioSettings
from shooting_flappy_birds.Bird import Bird
from shooting_flappy_birds.Bullet import Bullet
from shooting_flappy_birds.Player import Player


class Game:
    def __init__(self):
        self.audio_settings = AudioSettings()
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer

        # Define game parameters
        self.width = 1280
        self.height = 720
        self.fps = 90

        self.White = (255, 255, 255)
        self.Black = (0, 0, 0)
        self.Red = (255, 0, 0)
        self.Blue = (0, 0, 255)
        self.Green = (0, 255, 0)
        self.Yellow = (255, 255, 0)

        # Initialize pygame screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Shooting Flappy Birds")

        # Initialize player, bullets, enemies, and other game variables
        self.player = Player(50, self.height // 2, "assets/images/player.png")  # Initialize player before accessing it
        self.bullets = []
        self.enemies = []

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.score = 0
        self.background = pygame.image.load("assets/images/background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.health_regen_rate = 0.01  # Define the health regeneration rate
        self.yellow_spawn_timer = 0    # Initialize the yellow bird spawn timer
        self.blue_spawn_timer = 0      # Initialize the blue bird spawn timer
        self.red_spawn_timer = 0       # Initialize the red bird spawn timer

        self.restart_button = None  # Initialize the restart_button variable
        self.main_menu_button = None  # Initialize the restart_button variable

        # Load and play background music
        self.background_music = pygame.mixer.Sound("assets/music/music.mp3")  # Load the background music
        self.background_music.set_volume(self.player.audio_settings.background_music_volume)

        self.background_music.play(-1)  # Play the music indefinitely (-1 means loop)

        # Load sound effects
        self.bullet_sound = pygame.mixer.Sound("assets/sound effects/bullet.wav")
        self.bullet_sound.set_volume(self.player.audio_settings.bullet_sound_volume)  # Set bullet sound volume

        self.bird_sound = pygame.mixer.Sound("assets/sound effects/bird.wav")
        self.bird_sound.set_volume(self.player.audio_settings.bird_sound_volume)  # Set bird sound volume

        self.game_over_sound = pygame.mixer.Sound("assets/sound effects/game_over.wav")
        self.bird_spawn_count = 0  # Initialize the bird spawn count

    # Display the start screen and handle user input
    def display_start_screen(self):

        self.player = Player(50, self.height // 2, "assets/images/player.png")
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.player.health = self.player.max_health
        self.running = True

        start_font = pygame.font.Font(None, 48)
        start_text = start_font.render("Shooting Flappy Birds", True, self.Red)
        start_rect = start_text.get_rect(center=(self.width // 2, self.height // 3 - 50))

        back_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 + 120, 200, 50)  # Add this line

        start_button_rects = {
            "Start Game": pygame.Rect(self.width // 2 - 100, self.height // 2.5, 200, 50),
            "Options": pygame.Rect(self.width // 2 - 100, self.height // 2.5 + 80, 200, 50),
            "Exit": pygame.Rect(self.width // 2 - 100, self.height // 2.5 + 160, 200, 50)
        }
        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(start_text, start_rect)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button, rect in start_button_rects.items():
                        if rect.collidepoint(mouse_x, mouse_y):
                            if button == "Start Game":
                                self.run()  # Start the game
                            elif button == "Options":
                                self.display_options_menu()
                                pass
                            elif button == "Exit":
                                pygame.quit()
                                sys.exit()

                    # Add this block to handle the "Back" button in options menu
                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        return

            for button, rect in start_button_rects.items():
                color = self.Green if rect.collidepoint(mouse_x, mouse_y) else self.White
                pygame.draw.rect(self.screen, color, rect)
                button_font = pygame.font.Font(None, 24)
                button_text = button_font.render(button, True, self.Black)
                button_text_rect = button_text.get_rect(center=rect.center)
                self.screen.blit(button_text, button_text_rect)

            pygame.display.flip()
            self.clock.tick(self.fps)

    # Display the options menu and handle user input
    def display_options_menu(self):
        options_font = pygame.font.Font(None, 48)
        options_text = options_font.render("Options", True, self.White)
        options_rect = options_text.get_rect(center=(self.width // 2, self.height // 3 - 50))

        audio_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2.5, 200, 50)
        shortcuts_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2.5 + 80, 200, 50)
        back_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2.5 + 160, 200, 50)  # Add this line

        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(options_text, options_rect)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if audio_button_rect.collidepoint(mouse_x, mouse_y):
                        self.display_audio_settings()  # Call the audio settings function
                    elif shortcuts_button_rect.collidepoint(mouse_x, mouse_y):
                        self.display_shortcuts_settings()  # Call the shortcuts settings function
                        # After returning from shortcuts, the loop will continue and update the screen again
                    elif back_button_rect.collidepoint(mouse_x, mouse_y):  # Add this block
                        return

            for rect, text in [(audio_button_rect, "Audio"),
                               (shortcuts_button_rect, "Shortcuts"), (back_button_rect, "Back")]:
                color = self.Green if rect.collidepoint(mouse_x, mouse_y) else self.White
                pygame.draw.rect(self.screen, color, rect)
                button_font = pygame.font.Font(None, 24)
                button_text = button_font.render(text, True, self.Black)
                button_text_rect = button_text.get_rect(center=rect.center)
                self.screen.blit(button_text, button_text_rect)

            pygame.display.flip()
            self.clock.tick(self.fps)

    # Restart the game
    def restart(self):
        self.reset_game()
        self.running = True

    # Display audio settings and handle user input
    def display_audio_settings(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()  # Initialize mouse position

        back_button_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 50)

        bg_music_slider_rect = pygame.Rect(50, 250, 200, 10)
        bullet_effects_slider_rect = pygame.Rect(50, 350, 200, 10)
        bird_effects_slider_rect = pygame.Rect(50, 450, 200, 10)

        bg_music_slider_handle_rect = pygame.Rect(
            50 + (self.audio_settings.background_music_volume * 200), 245, 10, 20
        )

        bullet_effects_slider_handle_rect = pygame.Rect(
            50 + (self.audio_settings.bullet_sound_volume * 200), 345, 10, 20
        )
        bird_effects_slider_handle_rect = pygame.Rect(
            50 + (self.audio_settings.bird_sound_volume * 200), 445, 10, 20
        )

        dragging_bg_music_slider = False
        dragging_bullet_slider = False
        dragging_bird_slider = False

        while True:
            self.screen.blit(self.background, (0, 0))

            audio_title_font = pygame.font.Font(None, 48)
            audio_title_text = audio_title_font.render("Audio Settings", True, self.White)
            audio_title_rect = audio_title_text.get_rect(center=(self.width // 2, 100))
            self.screen.blit(audio_title_text, audio_title_rect)

            # Draw background rectangles for sliders
            pygame.draw.rect(self.screen, self.White, bg_music_slider_rect)

            bg_music_label_font = pygame.font.Font(None, 32)
            bg_music_label = bg_music_label_font.render("Background Music Volume", True, self.White)
            bg_music_label_rect = bg_music_label.get_rect(midleft=(50, 200))
            self.screen.blit(bg_music_label, bg_music_label_rect)

            bg_music_slider_rect = pygame.Rect(50, 250, 200, 10)
            pygame.draw.rect(self.screen, self.White, bg_music_slider_rect)
            pygame.draw.rect(self.screen, self.Yellow, bg_music_slider_handle_rect)

            pygame.draw.rect(self.screen, self.White, bullet_effects_slider_rect)

            bullet_effects_label_font = pygame.font.Font(None, 32)
            bullet_effects_label = bullet_effects_label_font.render("Bullet Effects Volume", True, self.White)
            bullet_effects_label_rect = bullet_effects_label.get_rect(midleft=(50, 300))
            self.screen.blit(bullet_effects_label, bullet_effects_label_rect)

            bullet_effects_slider_rect = pygame.Rect(50, 350, 200, 10)
            pygame.draw.rect(self.screen, self.White, bullet_effects_slider_rect)
            pygame.draw.rect(self.screen, self.Yellow, bird_effects_slider_handle_rect)

            pygame.draw.rect(self.screen, self.White, bird_effects_slider_rect)

            bird_effects_label_font = pygame.font.Font(None, 32)
            bird_effects_label = bird_effects_label_font.render("Bird Effects Volume", True, self.White)
            bird_effects_label_rect = bird_effects_label.get_rect(midleft=(50, 400))
            self.screen.blit(bird_effects_label, bird_effects_label_rect)

            bird_effects_slider_rect = pygame.Rect(50, 450, 200, 10)
            pygame.draw.rect(self.screen, self.White, bird_effects_slider_rect)
            pygame.draw.rect(self.screen, self.Yellow, bird_effects_slider_handle_rect)

            # Draw the "Back" button
            color = self.Green if back_button_rect.collidepoint(mouse_x, mouse_y) else self.White
            pygame.draw.rect(self.screen, color, back_button_rect)
            back_font = pygame.font.Font(None, 24)
            back_text = back_font.render("Back", True, self.Black)
            back_text_rect = back_text.get_rect(center=back_button_rect.center)
            self.screen.blit(back_text, back_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        return  # Return to the options menu

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if bg_music_slider_handle_rect.collidepoint(mouse_x, mouse_y):
                        dragging_bg_music_slider = True
                        dragging_bullet_slider = False
                        dragging_bird_slider = False

                    if bullet_effects_slider_handle_rect.collidepoint(mouse_x, mouse_y):
                        dragging_bullet_slider = True
                        dragging_bg_music_slider = False
                        dragging_bird_slider = False

                    if bird_effects_slider_handle_rect.collidepoint(mouse_x, mouse_y):
                        dragging_bird_slider = True
                        dragging_bg_music_slider = False
                        dragging_bullet_slider = False

                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_bg_music_slider = False
                    dragging_bullet_slider = False
                    dragging_bird_slider = False

            # Update the slider position based on the volume settings
            bg_music_slider_handle_rect.x = bg_music_slider_rect.left + int(
                bg_music_slider_rect.width * self.audio_settings.background_music_volume)

            bullet_effects_slider_handle_rect.x = bullet_effects_slider_rect.left + int(
                bullet_effects_slider_rect.width * self.audio_settings.bullet_sound_volume)

            bird_effects_slider_handle_rect.x = bird_effects_slider_rect.left + int(
                bird_effects_slider_rect.width * self.audio_settings.bird_sound_volume)

            pygame.draw.rect(self.screen, self.White, bg_music_slider_rect)
            pygame.draw.rect(self.screen, self.Yellow, bg_music_slider_handle_rect)

            pygame.draw.rect(self.screen, self.White, bullet_effects_slider_rect)
            pygame.draw.rect(self.screen, self.Yellow, bullet_effects_slider_handle_rect)

            pygame.draw.rect(self.screen, self.White, bird_effects_slider_rect)
            pygame.draw.rect(self.screen, self.Yellow, bird_effects_slider_handle_rect)

            if dragging_bg_music_slider:
                mouse_x, _ = pygame.mouse.get_pos()
                self.audio_settings.background_music_volume = ((mouse_x - bg_music_slider_rect.left)
                                                               / bg_music_slider_rect.width)
                self.background_music.set_volume(self.audio_settings.background_music_volume)
                self.audio_settings.background_music_volume = max(0,
                                                                  min(1, self.audio_settings.background_music_volume))
                bg_music_slider_handle_rect.x = bg_music_slider_rect.left + int(
                    bg_music_slider_rect.width * self.audio_settings.background_music_volume)

            # Update bullet sound effects volume based on slider position
            if dragging_bullet_slider:
                mouse_x, _ = pygame.mouse.get_pos()
                self.audio_settings.bullet_sound_volume = ((mouse_x - bullet_effects_slider_rect.left)
                                                           / bullet_effects_slider_rect.width)
                self.bullet_sound.set_volume(self.audio_settings.bullet_sound_volume)
                self.audio_settings.bullet_sound_volume = max(0,
                                                              min(1, self.audio_settings.bullet_sound_volume))
                bullet_effects_slider_handle_rect.x = bullet_effects_slider_rect.left + int(
                    bullet_effects_slider_rect.width * self.audio_settings.bullet_sound_volume)

            # Update bird sound effects volume based on slider position
            if dragging_bird_slider:
                mouse_x, _ = pygame.mouse.get_pos()
                self.audio_settings.bird_sound_volume = ((mouse_x - bird_effects_slider_rect.left)
                                                         / bird_effects_slider_rect.width)
                self.bird_sound.set_volume(self.audio_settings.bird_sound_volume)
                self.audio_settings.bird_sound_volume = max(0,
                                                            min(1, self.audio_settings.bird_sound_volume))
                bird_effects_slider_handle_rect.x = bird_effects_slider_rect.left + int(
                    bird_effects_slider_rect.width * self.audio_settings.bird_sound_volume)

            pygame.display.flip()
            self.clock.tick(self.fps)

    # Display shortcuts settings and handle user input
    def display_shortcuts_settings(self):
        # Clear the screen
        self.screen.blit(self.background, (0, 0))

        # Initialize mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Display shortcuts settings title
        shortcuts_title_font = pygame.font.Font(None, 48)
        shortcuts_title_text = shortcuts_title_font.render("Shortcuts Settings", True, self.White)
        shortcuts_title_rect = shortcuts_title_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(shortcuts_title_text, shortcuts_title_rect)

        # Display customizable actions and current key bindings
        action_list = [
            ("Move Up:", "K_UP"),
            ("Move Down:", "K_DOWN"),
            ("Shoot:", "K_SPACE"),
            # Add more actions as needed
        ]
        y_offset = 200

        for action, key_name in action_list:
            action_font = pygame.font.Font(None, 32)
            action_text = action_font.render(action, True, self.White)
            action_rect = action_text.get_rect(midleft=(50, y_offset))
            self.screen.blit(action_text, action_rect)

            key_binding_font = pygame.font.Font(None, 32)
            key_binding_text = key_binding_font.render(key_name, True, self.Yellow)
            key_binding_rect = key_binding_text.get_rect(midleft=(250, y_offset))
            self.screen.blit(key_binding_text, key_binding_rect)

            y_offset += 60

        # Define a dictionary to store the default key bindings
        default_key_bindings = {
            "Move Up": pygame.K_UP,
            "Move Down": pygame.K_DOWN,
            "Shoot": pygame.K_SPACE,
            "Pause": pygame.K_ESCAPE
        }

        # Create a dictionary to store the current key bindings
        key_bindings = dict(default_key_bindings)

        back_button_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Update mouse position
                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        return  # Return to the previous menu
                elif event.type == pygame.KEYDOWN:
                    for action, key in key_bindings.items():
                        if key == event.key:
                            # Display a message indicating the key is already bound to an action
                            print(f"Key {pygame.key.name(key)} is already bound to {action}")
                            break
                    else:
                        # Update the key binding for the selected action
                        key_bindings[selected_action] = event.key
                        selected_action = None

            # Draw the back button and its text
            color = self.Green if back_button_rect.collidepoint(mouse_x, mouse_y) else self.White
            pygame.draw.rect(self.screen, color, back_button_rect)
            back_font = pygame.font.Font(None, 24)
            back_text = back_font.render("Back", True, self.Black)
            back_text_rect = back_text.get_rect(center=back_button_rect.center)
            self.screen.blit(back_text, back_text_rect)

            pygame.display.flip()
            self.clock.tick(self.fps)

            # Clear the screen
            self.screen.blit(self.background, (0, 0))

            # Display the current key bindings
            for i, (action, key) in enumerate(key_bindings.items()):
                text = key_binding_font.render(f"{action}: {pygame.key.name(key)}", True, self.White)
                text_rect = text.get_rect(center=(self.width // 2, 200 + i * 40))
                self.screen.blit(text, text_rect)

    # Display the game over screen and handle user input
    def display_game_over_screen(self):

        self.bullet_sound.set_volume(self.audio_settings.bullet_sound_volume)  # Update bullet sound volume
        self.bullet_sound.play()  # Play the bullet sound effect

        restart_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 80, 200, 50)
        pygame.draw.rect(self.screen, self.Green, restart_button)


        restart_font = pygame.font.Font(None, 24)
        restart_text = restart_font.render("Restart", True, self.Black)
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        self.screen.blit(restart_text, restart_text_rect)

        main_menu_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 160, 200, 50)
        pygame.draw.rect(self.screen, self.Green, main_menu_button)

        main_menu_font = pygame.font.Font(None, 24)
        main_menu_text = main_menu_font.render("Main menu", True, self.Black)
        main_menu_text_rect = main_menu_text.get_rect(center=main_menu_button.center)
        self.screen.blit(main_menu_text, main_menu_text_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if restart_button.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.screen, self.Yellow, restart_button)
            if pygame.mouse.get_pressed()[0]:
                self.restart()  # Call the restart function
        elif main_menu_button.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.screen, self.Yellow, main_menu_button)
            if pygame.mouse.get_pressed()[0]:
                self.display_start_screen()

    # Reset game variables for a new game
    def reset_game(self):
        self.player = Player(50, self.height // 2, "assets/images/player.png")
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.player.health = self.player.max_health
        self.running = True
        self.run()

    # Spawn enemies based on timers and update their positions
    def spawn_enemy(self, bird_class, bird_list, spawn_timer, spawn_frequency, image_path, speed):
        spawn_timer += spawn_frequency
        if spawn_timer >= 100:
            bird_list.append(bird_class(self.width, random.randint(50, self.height - 50), image_path, speed))
            spawn_timer = 0

        return spawn_timer

    # Check for collisions between bullets and enemies
    def check_bullet_collisions(self, bullet_list, enemy_list):
        for bullet in bullet_list:
            for enemy in enemy_list:
                if bullet.rect.colliderect(enemy.rect):
                    bullet_list.remove(bullet)
                    enemy_list.remove(enemy)
                    self.score += 1  # Increase score when an enemy is hit
                    return True
        return False

    # Check for collisions between two objects
    @staticmethod
    def check_collision(object1, object2_list):
        for obj2 in object2_list:
            if object1.rect.colliderect(obj2.rect):
                object1.health -= 10
                object2_list.remove(obj2)
                return True
        return False

    # Main game loop
    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullets.append(Bullet(self.player.x + 50, self.player.y + 25, 5))
                        self.bullet_sound.play()  # Play the bullet sound effect
                    elif event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused

            if self.paused:
                pause_font = pygame.font.Font(None, 36)
                pause_text = pause_font.render("Paused", True, self.White)
                pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(pause_text, pause_rect)
                pass
            else:
                keys = pygame.key.get_pressed()
                self.player.move(keys)
                self.player.update()
                self.player.draw(self.screen)

                self.player.health = min(self.player.health + self.health_regen_rate, self.player.max_health)

                # Spawn enemies and update them
                self.yellow_spawn_timer = self.spawn_enemy(Bird, self.enemies, self.yellow_spawn_timer, 2,
                                                           "assets/images/yellow_bird.png", Bird.yellow_bird_speed)
                self.blue_spawn_timer = self.spawn_enemy(Bird, self.enemies, self.blue_spawn_timer, 0.8,
                                                         "assets/images/blue_bird.png", Bird.blue_bird_speed)
                self.red_spawn_timer = self.spawn_enemy(Bird, self.enemies, self.red_spawn_timer, 0.5,
                                                        "assets/images/red_bird.png",
                                                        Bird.red_bird_speed)

                self.bird_spawn_count += 1
                if self.bird_spawn_count == 500:  # Play bird sound every 500 birds
                    self.bird_sound.play()
                    self.bird_spawn_count = 0

                for enemy in self.enemies:
                    enemy.update()
                    enemy.draw(self.screen)

                # Update bullets
                for bullet in self.bullets:
                    bullet.update()
                    bullet.draw(self.screen)
                    if bullet.x > self.width:
                        self.bullets.remove(bullet)

                # Handle collisions
                for _ in self.enemies:
                    if self.check_collision(self.player, self.enemies):
                        pass
                    if self.check_bullet_collisions(self.bullets, self.enemies):
                        pass

                if self.player.health <= 0:
                    self.running = False

                # Calculate elapsed time in seconds
                elapsed_time = pygame.time.get_ticks() // 1000

                # Render the elapsed time text
                time_font = pygame.font.Font(None, 24)
                time_text = time_font.render(f"Time: {elapsed_time} seconds", True, self.White)

                # Display the elapsed time text
                time_text_rect = time_text.get_rect(midleft=(10, 50))
                self.screen.blit(time_text, time_text_rect)

                score_font = pygame.font.Font(None, 36)
                score_text = score_font.render(f"Score: {self.score}", True, self.White)
                score_text_rect = score_text.get_rect(midleft=(220, 50))
                self.screen.blit(score_text, score_text_rect)

                health_percentage = int((self.player.health / self.player.max_health) * 100)
                percentage_font = pygame.font.Font(None, 24)
                percentage_text = percentage_font.render(f"{health_percentage}%", True, self.White)
                percentage_text_rect = percentage_text.get_rect(midleft=(220, 20))
                self.screen.blit(percentage_text, percentage_text_rect)

                health_bar_width = (self.player.health / self.player.max_health) * 200
                pygame.draw.rect(self.screen, self.Red, (10, 10, 200, 20))  # Background
                pygame.draw.rect(self.screen, self.Green, (10, 10, health_bar_width, 20))  # Health bar
                pass

            pygame.display.flip()
            self.clock.tick(self.fps)

        if not self.paused:
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.update()
            self.player.draw(self.screen)
            self.player.health = min(self.player.health + self.health_regen_rate, self.player.max_health)
        pass

        # Display game over message and score
        if not self.running:
            self.screen.blit(self.background, (0, 0))  # Clear the screen

            game_over_font = pygame.font.Font(None, 48)
            game_over_text = game_over_font.render("Game Over", True, self.Red)
            game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 3))

            # Display score
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render(f"Score: {self.score}", True, self.White)
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 3 + 50))

            # Display runtime
            runtime = pygame.time.get_ticks() // 1000  # Get runtime in seconds
            runtime_font = pygame.font.Font(None, 24)
            runtime_text = runtime_font.render(f"Runtime: {runtime} seconds", True, self.White)
            runtime_text_rect = runtime_text.get_rect(center=(self.width // 2, self.height // 3 + 100))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(runtime_text, runtime_text_rect)

            self.restart_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 80, 200, 50)
            pygame.draw.rect(self.screen, self.Green, self.restart_button)

            # Restart button
            restart_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 80, 200, 50)
            pygame.draw.rect(self.screen, self.Green, restart_button)
            restart_font = pygame.font.Font(None, 24)
            restart_text = restart_font.render("Restart", True, self.Black)
            restart_text_rect = restart_text.get_rect(center=restart_button.center)
            self.screen.blit(restart_text, restart_text_rect)

            self.main_menu_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 160, 200, 50)
            pygame.draw.rect(self.screen, self.Green, self.main_menu_button)

            # Restart button
            main_menu_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 160, 200, 50)
            pygame.draw.rect(self.screen, self.Green, main_menu_button)
            main_menu_font = pygame.font.Font(None, 24)
            main_menu_text = main_menu_font.render("Main menu", True, self.Black)
            main_menu_text_rect = main_menu_text.get_rect(center=main_menu_button.center)
            self.screen.blit(main_menu_text, main_menu_text_rect)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.screen, self.Yellow, restart_button)
                if pygame.mouse.get_pressed()[0]:
                    self.reset_game()
            elif main_menu_button.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.screen, self.Yellow, main_menu_button)
                if pygame.mouse.get_pressed()[0]:
                    self.display_start_screen()

        pygame.mixer.music.stop()  # Stop the background music

        self.game_over_sound.play()  # Play the game over sound effect

        pygame.display.flip()  # Update the display

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
                    self.reset_game()
                    waiting = False

                elif event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN and main_menu_button.collidepoint(event.pos):
                    self.display_start_screen()
                    waiting = False
            self.clock.tick(self.fps)  # Add this line to control loop speed

        pygame.display.flip()

    pygame.quit()

    # Wait for restart after game over
    def wait_for_restart(self):
        pass
