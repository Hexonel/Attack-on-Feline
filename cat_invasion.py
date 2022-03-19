#! /usr/bin/env python3
# alien_invastion.py - The making of a 'space invader'-ish game!

import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet       # Imports classes from different files
from alien import Alien
from button import Button

class AlienInvasion:        # this one class contains the 'whole' program
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()       # method within pygame, to initiate the module (?)
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)        # full screen. How does this work tho (?)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')        # what (?)

        # Create an instance to store game statistics and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)      # is ai_game in (self, ai_game) not for self
        self.bullets = pygame.sprite.Group()    # .Group()is a pygame list, with some extra functionality, no idea how it works
        self.bullet = Bullet(self)  # but actually, self is for ai_game, since self self is created with an instance
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self,"Play")      # this works because we need only one button.


    def run_game(self):         # the loop. these things are done in this order, until the game is over.
        """Start the main loop for the game."""
        while True:
            self._check_events()        # 1) checks for events (keypress)

            if self.stats.game_active:          # Just lets you check for events, and updates screen accordingly
                self.ship.update()          # 2) updates ship (coordinates, images and what not)
                self._update_bullets()      # 3) updates bullet (coordinates, images and what now)
                self._update_aliens()       # 4) update after bullets, to see if they've been shot.

            self._update_screen()       # 5) draws above info, so that everything is visible to a person
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()       # makes the whole area (screen) visible. similar to display.update() (?)


    def _check_events(self):
        """Respond to keypreses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:    # if/elif because multiple keys can be active/inactive
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
                
            # Hide the mouse cursos.
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""        # just turns flag to True, except for q
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_top = True
        elif event.key == pygame.K_s:
            self.ship.moving_bottom = True
        elif event.key == pygame.K_p:
            sys.exit()
        elif event.key == pygame.K_RETURN:
            self._check_play_button((self.settings.screen_width /2, self.settings.screen_height /2))
        elif event.key == pygame.K_SPACE:
            self.bullet.shooting = True            # my own flag, so shooting can be continuous as well
    

    def _check_keyup_events(self, event):
        """Respond to key releases."""      # flags to False
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_top = False
        elif event.key == pygame.K_s:
            self.ship.moving_bottom = False
        elif event.key == pygame.K_SPACE:
            self.bullet.shooting = False
            self.bullet.time = 6           # required!! so there is no delay the next time space is pressed.


    def _update_bullets(self):
        """Update position of bulets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()       # Group() updates each sprite in the Group, defined at the top 
        self.bullet.shoot_bullet(self) # need self included, an instance of this class
        #Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():      # makes a copy of the list, so the changes don't affect the original (?)
            if bullet.rect.bottom <= 0:         # check this ^ a bit, to see why bother with this
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(    # checks for bullet and alien rects that are overlaping
            self.bullets,self.aliens, True, True)   # True(bullet) and True(alien) will delete thqe item it is connected to
        if collisions:
            for aliens in collisions.values():      # change a dict into a list which is 'hit aliens' long
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleed."""
        self._check_fleet_edges()
        self.aliens.update()        # call update on all the aliens (in aliens Group)

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement the number of ships.
        self.stats.ships_left -= 1      # Do it before if statement, so you don't have 4 lives, instead of 3.
        self.sb.prep_ships()
        if self.stats.ships_left > 0:
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break


    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size     # size contains (width, height) as a tuple!
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 4 * alien_height - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleed of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)        # fills the background, so                  
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()            
        self.ship.blitme()          # first draw the bullets, so the ship can be drawn on top!!
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()           # again (?)
    

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()