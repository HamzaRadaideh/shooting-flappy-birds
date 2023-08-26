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
                    self.score += 10  # Increase score when an enemy is hit
                    return True
        return False

    def check_collision(self, object1, object2_list):
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
                for enemy in self.enemies:
                    if self.check_collision(self.player, self.enemies):
                        pass
                    if self.check_bullet_collisions(self.bullets, self.enemies):
                        pass

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
            game_over_font = pygame.font.Font(None, 48)
            game_over_text = game_over_font.render("Game Over", True, self.Red)
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render(f"Score: {self.score}", True, self.White)

            game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 50))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
        pass


class Main:
    def __init__(self):
        self.game = Game()

    def start(self):
        self.game.run()
        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.start()
