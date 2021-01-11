import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop of the game"""
        while True:   # main game loop is run indefinetely until the sys.exit() command
            self._check_events()   # helper method to watch for keyboard and mouse events
            self.ship.update()     # update the position of the ship based on key presses
            self._update_bullets()
            self._update_screen()  # helper method to update the screen on every pass

    def _check_events(self):   # helper method that only affects the run_game() method
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()   # quit the python interpreter when q is pressed
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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of the old bullets"""
        # update bullet positions
        self.bullets.update()

        # get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create the fleet of ALiens"""
        # Create an alien and find the number of aliens in a row
        # spacing between each alien is equal to one alien width
        alien = Alien(self)   # u create the alien using the class u wrote
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine the number of rows of aliens that fit in the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (4 * alien_height)

        # create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # create an alien and place it in the row
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)  # alien added to the Group

    def _update_screen(self):
        """update images on the screen, and flip to the new screen"""
        self.screen.fill((self.settings.bg_color))  # here the color is set
        self.ship.blitme()  # redraw the current position of the ship
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()  # make the most recently drawn screen visible


if __name__ == '__main__':
    # Make a game instance and run it
    ai = AlienInvasion()
    ai.run_game()

