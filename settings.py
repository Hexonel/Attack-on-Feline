import pygame

class Settings:
    """A class to store all settings for Alien Invastion."""        # this class just creates data, no functions yet

    def __init__(self, ai_game):
        """Initialize the game's settings."""
        self.screen = ai_game.screen
        self.stats = ai_game.stats
        # Screen settings
        self.bg_color = (58, 38, 88)
        self.trans_bg = (200, 200, 200, 150)
        # Ship settings
        # Bullet settings
        self.bullet_info = {
            1: {'image': './images/bullet1.png', 'delete': True, 'speed': 10}, 
            2: {'image': './images/bullet2.png', 'delete': False, 'speed': 10}
        }
        self.bullet_speed = self.bullet_info[self.stats.bullet_level]['speed']
        # Alien settings
        self.fleet_drop_speed = 10
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5


        self.initialize_dynamic_settings()      # for dynamic values which change during the game

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 8.5
        # self.bullet_speed = 15
        self.alien_speed = 4

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50      # so we can assign higher points accoridng to Level, but reset to this initial 

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        # self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def set_trans_bg(self):         # make a transparent background when in PAUSE
        self.surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.surface.fill(self.trans_bg)
        self.screen.blit(self.surface, (0, 0))