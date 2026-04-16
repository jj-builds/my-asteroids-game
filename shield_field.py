from shield import Shield
import pygame
class ShieldField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.timer = 0

    def update(self, dt, screen):
        self.timer += dt
        if self.timer >= 10:
            self.timer = 0
            Shield(screen)
