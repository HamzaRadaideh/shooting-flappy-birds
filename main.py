import pygame
import random
import math

# Initialize pygame
pygame.init()

# At the beginning of your code
bird_amplitude = 50  # Adjust as needed
bird_frequency = 0.1  # Adjust as needed

# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

player_health = 100
max_health = 100
health_regen_rate = 0.1  # Adjust as needed
damage_amount = 25


# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Flappy Birds")

# Load game assets (character, bird, bullet, background, etc.)

# Game variables
player_x = 50
player_y = HEIGHT // 2
player_speed = 5

score = 0

birds = []
bird_speed = 3
bird_spawn_timer = 0

bullets = []
bullet_speed = 10

score = 0
lives = 3

# Game loop
running = True
clock = pygame.time.Clock()

background = pygame.image.load("background.jpeg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

start_time = pygame.time.get_ticks()


while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shoot a bullet
                bullets.append([player_x + 50, player_y + 25])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Update player
    pygame.draw.rect(screen, BLACK, (player_x, player_y, 50, 50))

    # Update birds
    for bird in birds:
        bird[0] -= bird_speed

        # Update y-position in a wave-like pattern
        bird[1] = HEIGHT // 2 + bird_amplitude * math.sin(bird_frequency * bird[0])

        pygame.draw.circle(screen, RED, (bird[0], bird[1]), 20)

        # Check for collision with bullets
        for bullet in bullets:
            if pygame.Rect(bullet[0], bullet[1], 10, 10).colliderect(pygame.Rect(bird[0], bird[1], 40, 40)):
                birds.remove(bird)
                bullets.remove(bullet)
                score += 1

    # Update bullets
    for bullet in bullets:
        bullet[0] += bullet_speed
        pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], 10, 10))

        if bullet[0] > WIDTH:
            bullets.remove(bullet)

    # Inside the game loop

    # Check for collision with birds
    for bird in birds:
        bird_rect = pygame.Rect(bird[0], bird[1], 40, 40)
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        if player_rect.colliderect(bird_rect):
            player_health -= damage_amount
            birds.remove(bird)

    # Health regeneration over time
    if player_health < max_health:
        player_health += health_regen_rate
        if player_health > max_health:
            player_health = max_health

    # Check for game over condition
    if player_health <= 0:
        running = False  # End the game

    # Bird spawning logic
    bird_spawn_timer += 1
    if bird_spawn_timer >= 100:
        birds.append([WIDTH, random.randint(50, HEIGHT - 50)])
        bird_spawn_timer = 0

    # Inside the game loop

    # Draw health bar background
    pygame.draw.rect(screen, BLACK, (10, 10, max_health + 4, 24))
    pygame.draw.rect(screen, RED, (12, 12, max_health, 20))  # Max health

    # Draw current health
    pygame.draw.rect(screen, GREEN, (12, 12, player_health, 20))

    # Inside the game loop, after updating the display

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, HEIGHT - 40))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# After the game loop

# Display game over message
font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over", True, RED)
text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(game_over_text, text_rect)

# Calculate total run time
end_time = pygame.time.get_ticks()
run_time = (end_time - start_time) / 1000  # Convert to seconds

# Display score and run time
score_text = font.render(f"Score: {score}", True, BLACK)
run_time_text = font.render(f"Run Time: {run_time:.2f} seconds", True, BLACK)
screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 40))
screen.blit(run_time_text, (WIDTH // 2 - run_time_text.get_width() // 2, HEIGHT // 2 + 80))

pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)  # 3000 milliseconds (3 seconds)
pygame.quit()






