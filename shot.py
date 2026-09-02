import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.s_h = SCREEN_HEIGHT
        self.s_w = SCREEN_WIDTH
        self.image = pygame.image.load("pictures/bullet.png")

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.position)
        bullet_rect = self.image.get_rect(center=screen_pos)
        screen.blit(self.image, bullet_rect)
    def update(self, dt, screen):
        keys = pygame.key.get_pressed()
        self.position += (self.velocity * 2 * dt)
        if keys[pygame.K_e]:
            self.kill()