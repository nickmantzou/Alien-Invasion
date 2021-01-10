import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion():
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)   # the Ship class requires the AlienInvasion Class as input parameter
        self.bullets = pygame.sprite.Group()   # bullets are many objects that we will control through a Group

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            self._check_events()   # helper method to watch for keyboard and mouse events
            self.ship.update()     # update the position of the ship based on key presses
            self.bullets.update()

            # get rid of bullets that have disappeared
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            self._update_screen()  # helper method to update the screen on every pass

            # get rid of the bullets that have disapeared



    def _check_events(self):   # helper method that only affects the run_game() method
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True  # set the moving right flag to True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True  # set the moving left flag to True
        elif event.key == pygame.K_q:
            sys.exit()  # exit when q is pressed
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  # set the moving right flag to False when the Key is released
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False  # set the moving left flag to False when Key is released

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        """update images on the screen, and flip to the new screen"""
        self.screen.fill((self.settings.bg_color))  # here the color is set
        self.ship.blitme()  # redraw the current position of the ship
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()  # make the most recently drawn screen visible


if __name__ == '__main__':
    # Make a game instance and run it
    ai = AlienInvasion()
    ai.run_game()

