from bomb import Bomb
import pygame
class BombField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.timer = 0

    def update(self, dt, screen):
        self.timer += dt
        if self.timer >= 10:
            self.timer = 0
            Bomb(screen)
