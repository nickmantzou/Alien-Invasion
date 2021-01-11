import json

class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize the game statistics"""
        self.settings = ai_game.settings
        self.reset_stats()  # this method resets all the statistics for every new game

        # start the game in inactive state
        self.game_active = False

        # High score should never be reset and is loaded from the json file where it is saved
        high_score_file = 'high_score.json'
        with open(high_score_file) as f:
            self.high_score = json.load(f)

    def reset_stats(self):
        """Initialize statistics that can change during a game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1