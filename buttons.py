import sys
import pygame
from time import sleep

class Buttons():
    def __init__(self, ai_game):
        """Initialize button attributes."""
        # Repetitive, in order to avoid circular import. Some better way to do that?
        self.aliens = ai_game.aliens
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.ship = ai_game.ship
        self.bullets = ai_game.bullets
        self.power_ups = ai_game.power_ups
        self.screen_rect = self.screen.get_rect()
        # Build buttons. Repetitive, but works for now.
        # New Game button.
        self.img1 = pygame.image.load('./images/buttons/new_game.png')
        self.img1_rect = self.img1.get_rect()
        self.img1_rect.top = 150
        self.img1_rect.left = self.screen_rect.right /2 - 260
        # Continue button.
        self.img2 = pygame.image.load('./images/buttons/continue0.png')
        self.img2_rect = self.img2.get_rect()
        self.img2_rect.top = 150 + self.img2_rect.height + 50
        self.img2_rect.left = self.screen_rect.right /2 - 260
        # Exit button.
        self.img3 = pygame.image.load('./images/buttons/exit.png')
        self.img3_rect = self.img3.get_rect()
        self.img3_rect.top = 150 + (self.img3_rect.height + 50) *2
        self.img3_rect.left = self.screen_rect.right /2 - 260
    

    def draw_buttons(self, mouse_pos):
        if self.stats.continue_gray:
            self.img2 = pygame.image.load('./images/buttons/continue0.png')
        elif not self.img2_rect.collidepoint(mouse_pos):
            self.img2 = pygame.image.load('./images/buttons/continue1.png')
        self.screen.blit(self.img1, self.img1_rect)
        self.screen.blit(self.img2, self.img2_rect)
        self.screen.blit(self.img3, self.img3_rect)


    def _check_new_game(self, ai_game, mouse_pos):
        """Reset everything except the highest score and create a new game."""
        new_game_clicked = self.img1_rect.collidepoint(mouse_pos)
        if new_game_clicked and not self.stats.game_active:
            self.screen.blit(pygame.image.load('./images/buttons/clicked_new_game.png'), self.img1_rect)
            sleep(1)
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.stats.continue_gray = False
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            self.power_ups.empty()

            # Create a new fleet and center the ship.
            ai_game._create_fleet()
            self.ship.center_ship()
                
            # Hide the mouse cursos.
            pygame.mouse.set_visible(False)

    
    def _check_continue(self, mouse_pos):
        continue_clicked = self.img2_rect.collidepoint(mouse_pos)
        if continue_clicked and not self.stats.game_active and not self.stats.continue_gray:
            self.stats.game_active = True
            pygame.mouse.set_visible(False)

    
    def _check_exit(self, mouse_pos):
        exit_clicked = self.img3_rect.collidepoint(mouse_pos)
        if exit_clicked and not self.stats.game_active:
            sys.exit()