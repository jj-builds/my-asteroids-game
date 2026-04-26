from fuel import Fuel
import pygame
class FuelField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.timer = 0

    def update(self, dt, screen):
        self.timer += dt
        if self.timer >= 20:
            self.timer = 0
            Fuel(screen)