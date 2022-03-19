import pygame
from pygame.sprite import Sprite
# pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet objet at the ship's current position."""
        super().__init__()      # Sprite is parent class, because it has a lot of useful code for projectiles sort of objects
        self.screen = ai_game.screen    # screen required here as well so we can draw stuff
        self.settings = ai_game.settings
        self.image = pygame.image.load('./images/bullet1.png')      # image of a bullet, instead of just simply assigning a color
        # Create a bullet rect at (0,0) and then set correct position
        self.rect = self.image.get_rect() #self.settings.bullet_width, self.settings.bullet_height)       # what(?)
        self.rect.midtop = ai_game.ship.rect.midtop     # midtop(?) "relative" to the ship! ship must be updated first!
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        self.shooting = False       # my flag for bullets
        self.time = 6           # time interval between bullets when holding space. 6 is ideal for now
        self.bullets = ai_game.bullets      # need bullets attribute connected with the one in alien_inasion

    def update(self):       # update the position of a bullet
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y        # self.y is what we see, self.rect.y is what the program sees
        
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)

    def shoot_bullet(self, ai_game):
        if self.shooting == True:   # my continuous adjustment. flag is True so:
            if self.time == 6:      # it checks whether the time interval is met
                new_bullet = Bullet(ai_game)    # ai_game is an instance of alien_invasion class, and not self (instance of this class?)
                self.bullets.add(new_bullet)
                self.time = 0       # resets the time
            self.time += 1   