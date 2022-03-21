import pygame, random
from pygame.sprite import Sprite

class PowerUps(Sprite):
    """Power-ups that drop from the top and make your aircraft stronger."""
    def __init__(self, ai_game):
        """Initialize the power ups"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('./images/bullet2.png') 
        self.rect = self.image.get_rect()
        self.speed = 4
        self.power_ups = ai_game.power_ups
        # self.rect.bottom = self.screen_rect.top
        # self.rect.y = random.randint(0, self.screen_rect.right - 15)

    def _create_power_up(self, ai_game):
        self.number = 33
        self.chance = random.randint(1, 700)
        if self.number == self.chance:
            power_up = PowerUps(ai_game)
            power_up.rect.x = random.randint(0, self.screen_rect.right - 15)
            power_up.rect.y = 0
            self.power_ups.add(power_up)

    def update(self):
        """Move the alien to the right."""
        self.rect.y += self.speed

    def draw_power_up(self):
        """Draw it on the screen."""
        self.screen.blit(self.image, self.rect)