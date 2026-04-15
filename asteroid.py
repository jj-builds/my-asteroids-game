from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
import pygame
import random
from circleshape import CircleShape
from logger import log_event
from player import Player
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    def update(self, dt, screen):
        self.position += (self.velocity * dt)
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20, 50)
            direction = self.velocity.rotate(angle)
            direction2 = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = direction * 1.2
            asteroid2.velocity = direction2 * 1.2
