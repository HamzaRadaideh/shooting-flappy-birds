import pygame

from shooting_flappy_birds.Game import Game


class Main:
    def __init__(self):
        self.game = Game()

    # Start the game by displaying the start screen and managing game flow
    def start(self):
        self.game.display_start_screen()
        while True:
            self.game.run()
            if not self.game.paused:
                self.game.display_game_over_screen()  # Display game over screen
                self.game.wait_for_restart()  # Wait for restart

    pygame.quit()


# Entry point of the program
if __name__ == "__main__":
    main = Main()
    main.start()
