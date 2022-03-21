class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        # self.settings = ai_game.settings
        self.ship_limit = 3
        self.reset_stats()
        # Start Alien Invastion in an inactive state.
        self.game_active = False
        self.continue_gray = True
        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ship_limit   #self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.bullet_level = 1   # max is set to 2!