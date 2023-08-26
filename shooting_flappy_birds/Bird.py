import pygame


class Bird:
    # Class-level attributes to define speeds for different bird types
    yellow_bird_speed = 2  # Define the speed for yellow birds
    blue_bird_speed = 1.5  # Define the speed for blue birds
    red_bird_speed = 1     # Define the speed for red birds

    # Constructor for Bird class
    def __init__(self, x, y, image_path, speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.speed = speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    # Update the bird's position
    def update(self):
        self.x -= self.speed
        self.rect.center = (self.x, self.y)

    # Draw the bird on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)
