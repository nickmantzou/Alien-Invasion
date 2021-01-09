import sys

import pygame

class AlienInvasion():
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 750))
        pygame.display.set_caption("Alien Invasion")

        # set a background color
        self.bg_color = (200, 165, 210)  # RGB coding for the color, here only initialization takes place, not setting the color

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            # watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # redraw the screen during each pass through the loop
            self.screen.fill((self.bg_color))   # here the color is set

            # make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run it
    ai = AlienInvasion()
    ai.run_game()

