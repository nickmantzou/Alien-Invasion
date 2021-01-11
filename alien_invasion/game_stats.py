
class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize the game statistics"""
        self.settings = ai_game.settings
        self.reset_stats()  # this method resets all the statistics for every new game

        # start the game in inactive state
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during a game"""
        self.ships_left = self.settings.ship_limit