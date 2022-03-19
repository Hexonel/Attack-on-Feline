class Settings:
    """A class to store all settings for Alien Invastion."""        # this class just creates data, no functions yet

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        # self.screen_width = 1200
        # self.screen_height = 800      # not relevant
        self.bg_color = (58, 38, 88)
        # Ship settings
        self.ship_limit = 3
        # Bullet settings
        self.bullet_width = 3       # height and weight are required for rect
        self.bullet_height = 15     # will keep these so I can change when testing
        # self.bullets_allowed = 5      # screw this limit
        # Alien settings
        self.fleet_drop_speed = 15
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5


        self.initialize_dynamic_settings()      # for dynamic values which change during the game

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 8.5
        self.bullet_speed = 15
        self.alien_speed = 2.5

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50      # so we can assign higher points accoridng to Level, but reset to this initial 

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)