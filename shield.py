import pygame
import random
from constants import *
class Shield(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-SHIELD_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + SHIELD_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -SHIELD_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + SHIELD_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.position = 

    def spawn(self, SHIELD_RADIUS, position, velocity, screen):
        asteroid = (position.x, position.y, SHIELD_RADIUS)
        asteroid.velocity = velocity
        self.draw(screen, position, SHIELD_RADIUS, LINE_WIDTH)

    def update(self, dt, screen):
        self.spawn_timer += dt
        if self.spawn_timer > 60:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            self.spawn(SHIELD_RADIUS, position, velocity)

    def draw(self, screen, position, radius, width):
        pygame.draw.circle(screen, "red", postion, radius, width)
