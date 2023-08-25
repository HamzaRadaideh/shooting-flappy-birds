import pygame
import random
import math

pygame.init()

audio_muted = False
show_shortcuts_menu = False

bird_amplitude = 50
bird_frequency = 0.1

width = 1000
height = 600
fps = 60

# Colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Green = (0, 255, 0)
Yellow = (255, 255, 0)

player_health = 100
max_health = 100
health_regen_rate = 0.1
damage_amount = 25

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Shooting Flappy Birds")

player_x = 50
player_y = height //2
player_speed = 5

score = 0

yellow_bird = []
yellow_bird_speed = 2
yellow_spawn_timer = 0

blue_bird = []
blue_bird_speed = 2
blue_spawn_timer = 0

red_bird = []
red_bird_speed = 2
red_spawn_timer = 0

bullets = []
bullet_speed = 10

running = True
clock = pygame.time.Clock()
paused = False
background = pygame.image.load("background.jpeg").convert()
background = pygame.transform.scale(background, (width,height))
start_time = pygame.time.get_ticks()


while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + 50, player_y + 25])
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_a:
                audio_muted = not audio_muted
            elif event.key == pygame.K_h:
                show_shortcuts_menu = not show_shortcuts_menu

    if paused:
        # Draw a pause message or screen
        pause_text = font.render("PAUSED", True, Red)
        pause_rect = pause_text.get_rect(center=(width // 2, height // 2))
        screen.blit(pause_text, pause_rect)

        if audio_muted:
            audio_text = font.render("Audio: Muted (Press 'A' to Unmute", True, Black)
        else:
            audio_text = font.render("Audio: On (Press 'A' to Mute)", True, Black)

        if show_shortcuts_menu:
            shortcuts_text = font.render("Keyboard Shortcuts:", True, Black)
            shortcut_info = [
                "A - Toggle Audio",
                "H - Show/Hide Shortcuts",
                "Esc - Pause/Resume",
                "Space - Shoot",
                "Up/Down - Move",
            ]
            y_position = 40
            for shortcut in shortcut_info:
                shortcut_render = font.render(shortcut, True, Black)
                screen.blit(shortcut_render, (10, y_position))
                y_position += 30

        # Display game progress (score)
        progress_text = font.render(f"Score: {score} | Time: {run_time:.2f} seconds", True, Black)
        screen.blit(progress_text, (10, 10))

    else:
        end_time = pygame.time.get_ticks()
        run_time = (end_time - start_time) / 1000  # Convert to seconds

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Update player
        pygame.draw.rect(screen, Black, (player_x, player_y, 50, 50))

        # spawn yellow birds
        yellow_spawn_timer += 2
        if yellow_spawn_timer >= 100:
            yellow_bird.append([width, random.randint(50, height - 50)])
            yellow_spawn_timer = 0

        # Update yellow birds
        for bird in yellow_bird:
            bird[0] -= yellow_bird_speed
            bird[1] = height // 2 + bird_amplitude * math.sin(bird_frequency * bird[0])
            pygame.draw.circle(screen, Yellow, (bird[0], bird[1]), 20)

            # Check for collision with birds
            for bird in yellow_bird:
                bird_rect = pygame.Rect(bird[0], bird[1], 40, 40)
                player_rect = pygame.Rect(player_x, player_y, 50, 50)
                if player_rect.colliderect(bird_rect):
                    player_health -= damage_amount
                    yellow_bird.remove(bird)

            # Check for collision with bullets
            for bullet in bullets:
                if pygame.Rect(bullet[0], bullet[1], 10, 10).colliderect(pygame.Rect(bird[0], bird[1], 40, 40)):
                    yellow_bird.remove(bird)
                    bullets.remove(bullet)
                    score += 1

        # spawn blue birds
        blue_spawn_timer += 1
        if blue_spawn_timer >= 100:
            blue_bird.append([width, random.randint(50, height - 50)])
            blue_spawn_timer = 0
        # Update blue birds
        for bird in blue_bird:
            bird[0] -= blue_bird_speed
            bird[1] = height // 2 + bird_amplitude * math.sin(bird_frequency * bird[0])
            pygame.draw.circle(screen, Blue, (bird[0], bird[1]), 20)

            # Check for collision with birds
            for bird in blue_bird:
                bird_rect = pygame.Rect(bird[0], bird[1], 40, 40)
                player_rect = pygame.Rect(player_x, player_y, 50, 50)
                if player_rect.colliderect(bird_rect):
                    player_health -= damage_amount
                    blue_bird.remove(bird)

            # Check for collision with bullets
            for bullet in bullets:
                if pygame.Rect(bullet[0], bullet[1], 10, 10).colliderect(pygame.Rect(bird[0], bird[1], 40, 40)):
                    blue_bird.remove(bird)
                    bullets.remove(bullet)
                    score += 1

        # spawn red birds
        red_spawn_timer += 0.5
        if red_spawn_timer >= 100:
            red_bird.append([width, random.randint(50, height - 50)])
            red_spawn_timer = 0

        # Update red birds
        for bird in red_bird:
            bird[0] -= red_bird_speed
            bird[1] = height // 2 + bird_amplitude * math.sin(bird_frequency * bird[0])
            pygame.draw.circle(screen, Red, (bird[0], bird[1]), 20)

            # Check for collision with birds
            for bird in red_bird:
                bird_rect = pygame.Rect(bird[0], bird[1], 40, 40)
                player_rect = pygame.Rect(player_x, player_y, 50, 50)
                if player_rect.colliderect(bird_rect):
                    player_health -= damage_amount
                    red_bird.remove(bird)

            # Check for collision with bullets
            for bullet in bullets:
                if pygame.Rect(bullet[0], bullet[1], 10, 10).colliderect(pygame.Rect(bird[0], bird[1], 40, 40)):
                    red_bird.remove(bird)
                    bullets.remove(bullet)
                    score += 1

        # Update bullets
        for bullet in bullets:
            bullet[0] += bullet_speed
            pygame.draw.rect(screen, Black, (bullet[0], bullet[1], 10, 10))

            if bullet[0] > width:
                bullets.remove(bullet)

        # Health regeneration over time
        if player_health < max_health:
            player_health += health_regen_rate
            if player_health > max_health:
                player_health = max_health

        # Check for game over condition
        if player_health <= 0:
            running = False  # End the game

        # Draw health bar background
        pygame.draw.rect(screen, Black, (10, 10, max_health + 4, 24))
        pygame.draw.rect(screen, Red, (12, 12, max_health, 20))  # Max health

        # Draw current health
        pygame.draw.rect(screen, Green, (12, 12, player_health, 20))

        # Inside the game loop, after updating the display

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, Black)
        screen.blit(score_text, (10, height - 40))

    # Update display
    pygame.display.flip()
    clock.tick(fps)

# Calculate total run time
end_time = pygame.time.get_ticks()
run_time = (end_time - start_time) / 1000  # Convert to seconds

# Display game over message
font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over", True, Red)
text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
screen.blit(game_over_text, text_rect)

# Display score and run time
score_text = font.render(f"Score: {score}", True, Black)
run_time_text = font.render(f"Run Time: {run_time:.2f} seconds", True, Black)
screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + 40))
screen.blit(run_time_text, (width // 2 - run_time_text.get_width() // 2, height // 2 + 80))

pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(5000)

pygame.quit()
