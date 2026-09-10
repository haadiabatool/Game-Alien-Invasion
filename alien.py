import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):

    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings

        # Load the alien image 
        self.image=pygame.image.load('assets/badge-1.png')
        self.rect=self.image.get_rect()

        # Start somewhere above the visible screen
        self.rect.x=random.randint(
            0,self.screen.get_width()-self.rect.width
        )

        self.rect.y=random.randint(
            -1200,-self.rect.height
        )


        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

        self.speed_factor = random.uniform(0.5, 1.0)

    def update(self):

        current_fall_speed = self.speed_factor * self.settings.alien_speed

        # Move alien downward
        self.y += current_fall_speed
        self.rect.y = int(self.y)


    
    def check_edges(self):
        # Not needed for vertical falling
        return False
        # screen_rect=self.screen.get_rect()
        # return (self.rect.right >=screen_rect.right) or (self.rect.left<=0)
    