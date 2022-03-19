import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):        # ai_game is self in Ship(self) in ai_side (?)
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen        # ai_game is self of instance, so .screen must already be defined in the main class
        self.settings = ai_game.settings    # making 'settings' file available here as well. instead of .settings = Settings() (?)
        self.screen_rect = ai_game.screen.get_rect()    # sets a rectangle of the whole screen (?)

        # Load the ship image and get its rect.
        self.image = pygame.image.load('./images/aircraft1-0.png')      # loads the image for ship
        self.rect = self.image.get_rect()       # rectangle values of the ship (image)

        # Start each new ship at the bottom centre of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)     # decimal values are more precise (since movement can be 1.6 or w/e)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_right = False       # all flags are False at start
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False

    def update(self):
        """Update the ship's position based on the movement flag."""    # based on 'check events' it decides what to change
        # Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_top and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x    # keep rect.x and x same, since we want object interaction to match the image
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        if self.moving_bottom == True:      # off image when going down, so right-down and left-down can also have the same image
            self.image = pygame.image.load('./images/aircraft1-0.png')
        elif self.moving_right == True or self.moving_left == True or self.moving_top == True: # top/right/left (without down) are on img
            self.image = pygame.image.load('./images/aircraft1.png')
        else:
            self.image = pygame.image.load('./images/aircraft1-0.png')      # stationary (False flags) is also off image!

        self.screen.blit(self.image, self.rect)     # blit() is to draw an object (?)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)     # reset the self.x attribute, which is used to track the ship's position
        self.y = float(self.rect.y)     # book didn't add this!! stuck in the middle of the screen lol