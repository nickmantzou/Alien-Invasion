import sys
from time import sleep
import json

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        # create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)   # the Ship class requires the AlienInvasion Class as input parameter
        self.bullets = pygame.sprite.Group()   # bullets are many objects that we will control through a Group
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """Start the main loop of the game"""
        while True:   # main game loop is run indefinetely until the sys.exit() command
            self._check_events()   # helper method to watch for keyboard and mouse events

            if self.stats.game_active:
                self.ship.update()     # update the position of the ship based on key presses
                self._update_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True  # set the moving right flag to True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True  # set the moving left flag to True
        elif event.key == pygame.K_q:
            self._save_high_score(self.stats.high_score)
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

    def _check_play_button(self, mouse_pos):
        """start a new game when the player hits play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset the game's dynamic settings
            self.settings.initialize_dynamic_settings()

            # reset game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # get rid of any remaining aliens or bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _update_bullets(self):
        """Update the position of bullets and get rid of the old bullets"""
        # update bullet positions
        self.bullets.update()

        # get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """check whether bullet has hit aliens and whether fleet is empty, then repopulate"""
        # remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # check if all aliens are shot down
        # if so, repopulate the group
        if not self.aliens:
            # destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()   # increase difficulty

            # Increase Level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        check if the fleet is at an edge,
        then update the positions of all alliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # decrement ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # get rid of any remaining aliens or bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if aliens hit the bottom, if yes start over"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship was hit
                self._ship_hit()
                break

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

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """frop the entire fleet and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _save_high_score(self, high_score):
        """Save the high score to a txt file"""
        high_score_file = 'high_score.json'
        with open(high_score_file, 'w') as f:
            json.dump(high_score, f)


    def _update_screen(self):
        """update images on the screen, and flip to the new screen"""
        self.screen.fill((self.settings.bg_color))  # here the color is set
        self.ship.blitme()  # redraw the current position of the ship
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  # make the most recently drawn screen visible


if __name__ == '__main__':
    # Make a game instance and run it
    ai = AlienInvasion()
    ai.run_game()

