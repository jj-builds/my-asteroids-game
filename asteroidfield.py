import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.spawn_timer = 0.0

        half_w = SCREEN_WIDTH / 2
        half_h = SCREEN_HEIGHT / 2

        self.edges = [
            # Spawn left of screen, moving right
            [
                pygame.Vector2(1, 0),
                lambda offset: pygame.Vector2(
                    self.player.position.x - half_w - ASTEROID_MAX_RADIUS,
                    self.player.position.y - half_h + (offset * SCREEN_HEIGHT),
                ),
            ],
            # Spawn right of screen, moving left
            [
                pygame.Vector2(-1, 0),
                lambda offset: pygame.Vector2(
                    self.player.position.x + half_w + ASTEROID_MAX_RADIUS,
                    self.player.position.y - half_h + (offset * SCREEN_HEIGHT),
                ),
            ],
            # Spawn above screen, moving down
            [
                pygame.Vector2(0, 1),
                lambda offset: pygame.Vector2(
                    self.player.position.x - half_w + (offset * SCREEN_WIDTH),
                    self.player.position.y - half_h - ASTEROID_MAX_RADIUS,
                ),
            ],
            # Spawn below screen, moving up
            [
                pygame.Vector2(0, -1),
                lambda offset: pygame.Vector2(
                    self.player.position.x - half_w + (offset * SCREEN_WIDTH),
                    self.player.position.y + half_h + ASTEROID_MAX_RADIUS,
                ),
            ],
        ]

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt, screen):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            
            # offset is a random float between 0.0 and 1.0 along that edge
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)