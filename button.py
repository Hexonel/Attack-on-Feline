import pygame

# from game_stats import Gamestats

class Buttons:
    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.stats = ai_game.stats
        self.screen_rect = self.screen.get_rect()
        # Build buttons. Repetitive, but works for now.
        # New Game button.
        self.img1 = pygame.image.load('./images/new_game.png')
        self.img1_rect = self.img1.get_rect()
        self.img1_rect.top = 150
        self.img1_rect.left = self.screen_rect.right /2 - 260
        # Continue button.
        self.img2 = pygame.image.load('./images/continue0.png')
        self.img2_rect = self.img2.get_rect()
        self.img2_rect.top = 150 + self.img2_rect.height + 50
        self.img2_rect.left = self.screen_rect.right /2 - 260
        # Exit button.
        self.img3 = pygame.image.load('./images/exit.png')
        self.img3_rect = self.img3.get_rect()
        self.img3_rect.top = 150 + (self.img3_rect.height + 50) *2
        self.img3_rect.left = self.screen_rect.right /2 - 260
    

    def draw_buttons(self):
        if self.stats.continue_gray:
            self.img2 = pygame.image.load('./images/continue0.png')
        else:
            self.img2 = pygame.image.load('./images/continue1.png')
        self.screen.blit(self.img1, self.img1_rect)
        self.screen.blit(self.img2, self.img2_rect)
        self.screen.blit(self.img3, self.img3_rect)