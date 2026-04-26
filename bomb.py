import pygame
import random
from circleshape import CircleShape
from constants import SHIELD_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT

class Bomb(CircleShape):
    def __init__(self, screen):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        super().__init__(x, y, SHIELD_RADIUS)
        self.velocity = pygame.Vector2(random.randint(0, 75), random.randint(0, 75))
        self.s_h = SCREEN_HEIGHT
        self.s_w = SCREEN_WIDTH
        self.explosion_radius = 1000

    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", self.position, self.radius)

    def update(self, dt, screen):
        self.position += self.velocity * dt

        if self.position[1] > self.s_h:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.s_h

        if self.position[0] > self.s_w:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.s_w

    def explode(self):
        self.kill()
        return [self.position.x - self.explosion_radius,
            self.position.y - self.explosion_radius,
            self.position.x + self.explosion_radius,
            self.position.y + self.explosion_radius]