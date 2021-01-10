import pygame

class Ship():
    """ a class to manage the ship"""

    def __init__(self, ai_game):   # initialization requires also an instance of the current game class
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen   # screens are matching with the game
        self.screen_rect = ai_game.screen.get_rect()   # every object is considered a rectangle, including the screen

        # load the ship image and get its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()    # ship image is turned into a rectangle

        # start each new ship at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)