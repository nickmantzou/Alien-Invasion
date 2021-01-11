import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """ a class to manage the ship"""

    def __init__(self, ai_game):   # initialization requires also an instance of the current game class
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen   # screens are matching with the game
        self.settings = ai_game.settings  # importing the game settings
        self.screen_rect = ai_game.screen.get_rect()   # every object is considered a rectangle, including the screen

        # load the ship image and get its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()    # ship image is turned into a rectangle

        # start each new ship at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store the decimal value for the ship'' horizontal position
        self.x = float(self.rect.x)

        # movement flags
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position based on movement flags"""
        # update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:  # respecting screen boundaries
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:  # respecting screen boundaries
            self.x -= self.settings.ship_speed

        # update the rect object from self.x
        self.rect.x = self.x