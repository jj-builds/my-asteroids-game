import pygame
import random
from circleshape import CircleShape
from constants import SHIELD_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT

class Shield(CircleShape):
    def __init__(self, screen):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        super().__init__(x, y, SHIELD_RADIUS)
        self.velocity = pygame.Vector2(random.randint(-50, 50), random.randint(-50, 50))
        self.draw(screen)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, dt, screen):
        self.position += self.velocity * dt
