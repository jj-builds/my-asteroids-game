from power_up import Powerup
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
class PowerupField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.timer = 25

    def update(self, dt, screen):
        self.timer += dt
        if self.timer >= 30:
            Powerup(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 25)
            self.timer = 0