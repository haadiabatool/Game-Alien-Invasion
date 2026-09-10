import sys
import pygame
from settings import Settings
from time import sleep
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

THEME = {
    'BG_COLOR': (11, 13, 25),  
    'CARD_BG': (20, 24, 45),       
    'BORDER_COLOR': (31, 41, 77), 
    'NEON_TEAL': (0, 255, 204),     
    'NEON_CORAL': (255, 71, 87),   
    'TEXT_MAIN': (233, 233, 240),    
    'TEXT_MUTED': (160, 170, 191),   
}

def draw_visibility_glow(surface, color, target_surface, position):
    """Black icons/images ke around neon outline glow draw karne ka helper method."""
    mask = pygame.mask.from_surface(target_surface)
    outline = mask.outline()
    
    # Glow surface layer
    glow_surf = pygame.Surface(target_surface.get_size(), pygame.SRCALPHA)
    for point in outline:
        pygame.draw.circle(glow_surf, (*color, 180), point, 3)
        
    surface.blit(glow_surf, position)
    surface.blit(target_surface, position)

class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create instances for game stats and scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)   
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.bg_color = (230, 230, 230)

        # Game states
        self.game_active = False
        self.game_over = False  # Track if the player is out

        # Buttons
        self.play_button = Button(self, "Play")
        self.try_again_button = Button(self, "Try Again")
        self.home_button = Button(self, "Home")

        # Position "Try Again" and "Home" buttons
        self._position_game_over_buttons()



    def _style_buttons(self):
        """CSS color scheme buttons par apply karna."""
       
        for btn in [self.play_button, self.try_again_button]:
            btn.button_color = THEME['NEON_TEAL']
            btn.text_color = THEME['BG_COLOR']
            btn._prep_msg(btn.msg)

       
        self.home_button.button_color = THEME['NEON_CORAL']
        self.home_button.text_color = THEME['TEXT_MAIN']
        self.home_button._prep_msg("RETURN HOME")


    def _position_game_over_buttons(self):
        """Try Again aur Home buttons ko screen ke center mein arrange karna."""
        center_x = self.screen.get_rect().centerx
        center_y = self.screen.get_rect().centery


        self.try_again_button.rect.center = (center_x, center_y - 20)
        self.try_again_button._prep_msg("Try Again")

        # Home Button 
        self.home_button.rect.center = (center_x, center_y + 50)
        self.home_button._prep_msg("Home")

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def run_game(self):
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
           
            self._update_screen()
            self.clock.tick(60)


    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            self.bullets.empty()
            
            #speed gradually increase
            self.settings.increase_speed()


            self._create_fleet()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE and self.game_active:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        """When Ship hit game Over State."""
        self.game_active = False
        self.game_over = True
        pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


    def _check_buttons(self, mouse_pos):
        """Play, Try Again,and Home click handles"""
        # Main Start Play Button
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active and not self.game_over:
            self._start_game()


        # Game Over Screen Buttons
        if self.game_over:
            if self.try_again_button.rect.collidepoint(mouse_pos):
                self._start_game()
            elif self.home_button.rect.collidepoint(mouse_pos):
                self.game_over = False



    def _start_game(self):
        
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()

        self.game_active = True
        self.game_over = False

        self.sb.prep_score()

        self.bullets.empty()
        self.aliens.empty()

        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)


    def _draw_card_overlay(self, width, height, y_offset=0):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + y_offset)
        
        # Transparent Card Background
        card_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (*THEME['CARD_BG'], 220), card_surf.get_rect(), border_radius=16)
        pygame.draw.rect(card_surf, THEME['BORDER_COLOR'], card_surf.get_rect(), width=2, border_radius=16)
        
        self.screen.blit(card_surf, rect.topleft)


    def _update_screen(self):
        # 1. CSS Background Color
        self.screen.fill(THEME['BG_COLOR'])

        # 2. Draw Bullets (Neon Lasers)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 3. Draw Ship with Cyan Glow for Black Icon Visibility
        draw_visibility_glow(self.screen, THEME['NEON_TEAL'], self.ship.image, self.ship.rect.topleft)

        # 4. Draw Aliens with Red Glow for Black Icon Visibility
        for alien in self.aliens.sprites():
            draw_visibility_glow(self.screen, THEME['NEON_CORAL'], alien.image, alien.rect.topleft)

        self.sb.show_score()

        # 5. UI Overlay Logic
        if self.game_over:
            self._draw_card_overlay(450, 300)

            # Game Over Title
            font = pygame.font.SysFont("Press Start 2P", 42)
            msg_image = font.render("GAME OVER", True, THEME['NEON_CORAL'])
            msg_rect = msg_image.get_rect()
            msg_rect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery - 80)
            self.screen.blit(msg_image, msg_rect)

            self.try_again_button.draw_button()
            self.home_button.draw_button()

        elif not self.game_active:
            self._draw_card_overlay(480, 220)
            
            # Arcade Title Screen
            font = pygame.font.SysFont("Press Start 2P", 32)
            title_surf = font.render("ALIEN INVASION", True, THEME['TEXT_MAIN'])
            title_rect = title_surf.get_rect()
            title_rect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery - 40)
            self.screen.blit(title_surf, title_rect)

            self.play_button.rect.center = (self.screen.get_rect().centerx, self.screen.get_rect().centery + 30)
            self.play_button._prep_msg("PLAY GAME")
            self.play_button.draw_button()

        pygame.display.flip()



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()