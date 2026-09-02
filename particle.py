import pygame
import random


class ExplosionParticle(pygame.sprite.Sprite):
    containers = ()
    _surface_cache = {}

    def __init__(self, x, y, color="white", friction=0.95, lifetime=0.7):
        super().__init__(self.containers)
        if color not in ExplosionParticle._surface_cache:
            surf = pygame.Surface((4, 4))
            surf.fill(color)
            ExplosionParticle._surface_cache[color] = surf
        self.image = ExplosionParticle._surface_cache[color]
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(x, y)

        # Uniform radial explosion
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        self.lifetime = lifetime
        self.friction = friction

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.position)
        self.rect.center = (screen_pos.x, screen_pos.y)
        screen.blit(self.image, self.rect)

    def update(self, dt, screen):
        self.position += self.velocity * dt
        self.velocity *= self.friction

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()