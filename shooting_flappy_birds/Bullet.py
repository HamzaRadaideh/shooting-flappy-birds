import pygame


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
