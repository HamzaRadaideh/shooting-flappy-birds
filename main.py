import pygame
import random


class Bird:
    yellow_bird_speed = 2  # Define the speed for yellow birds
    blue_bird_speed = 1.5  # Define the speed for blue birds
    red_bird_speed = 1     # Define the speed for red birds

    def __init__(self, x, y, image_path, speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.speed = speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.x -= self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player:
    def __init__(self, x, y):
        self.height = 600
        self.x = x
        self.y = y
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Ensure the player doesn't go above the top boundary
        if self.y < 0:
            self.y = 0

        # Ensure the player doesn't go below the bottom boundary
        if self.y > self.height - self.rect.height:
            self.y = self.height - self.rect.height

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)


class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 10, 10)  # Create a rect for collision detection

    def update(self):
        self.x += self.speed
        self.rect.topleft = (self.x, self.y)  # Update the rect position

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)


class Game:
    def __init__(self):
        pygame.init()

        self.width = 1000
        self.height = 600
        self.fps = 144

        self.White = (255, 255, 255)
        self.Black = (0, 0, 0)
        self.Red = (255, 0, 0)
        self.Blue = (0, 0, 255)
        self.Green = (0, 255, 0)
        self.Yellow = (255, 255, 0)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Shooting Flappy Birds")

        self.player = Player(50, self.height // 2)
        self.bullets = []
        self.enemies = []

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.score = 0
        self.background = pygame.image.load("background.jpeg").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.health_regen_rate = 0.01  # Define the health regeneration rate
        self.yellow_spawn_timer = 0    # Initialize the yellow bird spawn timer
        self.blue_spawn_timer = 0      # Initialize the blue bird spawn timer
        self.red_spawn_timer = 0       # Initialize the red bird spawn timer

        self.restart_button = None  # Initialize the restart_button variable

    def reset_game(self):
        self.player = Player(50, self.height // 2)
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.player.health = self.player.max_health
        self.running = True

    def spawn_enemy(self, bird_class, bird_list, spawn_timer, spawn_frequency, image_path, speed):
        spawn_timer += spawn_frequency
        if spawn_timer >= 100:
            bird_list.append(bird_class(self.width, random.randint(50, self.height - 50), image_path, speed))
            spawn_timer = 0
        return spawn_timer

    def check_bullet_collisions(self, bullet_list, enemy_list):
        for bullet in bullet_list:
            for enemy in enemy_list:
                if bullet.rect.colliderect(enemy.rect):
                    bullet_list.remove(bullet)
                    enemy_list.remove(enemy)
                    self.score += 1  # Increase score when an enemy is hit
                    return True
        return False

    @staticmethod
    def check_collision(object1, object2_list):
        for obj2 in object2_list:
            if object1.rect.colliderect(obj2.rect):
                object1.health -= 10
                object2_list.remove(obj2)
                return True
        return False

    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullets.append(Bullet(self.player.x + 50, self.player.y + 25, 5))
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
                                                           "yellow_bird.png", Bird.yellow_bird_speed)
                self.blue_spawn_timer = self.spawn_enemy(Bird, self.enemies, self.blue_spawn_timer, 0.8,
                                                         "blue_bird.png", Bird.blue_bird_speed)
                self.red_spawn_timer = self.spawn_enemy(Bird, self.enemies, self.red_spawn_timer, 0.5, "red_bird.png",
                                                        Bird.red_bird_speed)

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
            game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))

            # Display score
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render(f"Score: {self.score}", True, self.White)
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 50))

            # Display runtime
            runtime = pygame.time.get_ticks() // 1000  # Get runtime in seconds
            runtime_font = pygame.font.Font(None, 24)
            runtime_text = runtime_font.render(f"Runtime: {runtime} seconds", True, self.White)
            runtime_text_rect = runtime_text.get_rect(center=(self.width // 2, self.height // 2 + 100))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(runtime_text, runtime_text_rect)

            self.restart_button = pygame.Rect(self.width // 2 - 50, self.height // 2 + 150, 100, 50)
            pygame.draw.rect(self.screen, self.Green, self.restart_button)

            # Restart button
            restart_button = pygame.Rect(self.width // 2 - 50, self.height // 2 + 150, 100, 50)
            pygame.draw.rect(self.screen, self.Green, restart_button)
            restart_font = pygame.font.Font(None, 24)
            restart_text = restart_font.render("Restart", True, self.Black)
            restart_text_rect = restart_text.get_rect(center=restart_button.center)
            self.screen.blit(restart_text, restart_text_rect)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.screen, self.Yellow, restart_button)
                if pygame.mouse.get_pressed()[0]:
                    self.reset_game()
            pass

        pygame.display.flip()  # Update the display
        waiting_for_restart = True

        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting_for_restart = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.restart_button.collidepoint(event.pos):
                    self.reset_game()
                    waiting_for_restart = False

                self.clock.tick(self.fps)

        pygame.quit()


class Main:
    def __init__(self):
        self.game = Game()

    def start(self):
        while True:
            self.game.run()
            if not self.game.paused:
                break

        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.start()
