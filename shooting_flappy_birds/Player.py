import pygame

from shooting_flappy_birds.AudioSettings import AudioSettings


class Player:
    # Constructor for Player class
    def __init__(self, x, y):
        self.background_music_volume = None
        self.height = 600
        self.x = x
        self.y = y
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.audio_settings = AudioSettings()  # Create an instance of AudioSettings

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
