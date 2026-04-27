import pygame
import random
class ExplosionParticle(pygame.sprite.Sprite):
    # We define an empty containers tuple here to prevent errors
    containers = () 

    def __init__(self, x, y):
        # By passing containers here, the Sprite automatically joins the groups
        super().__init__(self.containers)
        
        self.image = pygame.Surface((4, 4))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity *= random.uniform(50, 200)
        self.lifetime = 0.7 # Long lifetime for testing

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt, screen):
        # Update position based on velocity
        self.position += self.velocity * dt
        self.velocity *= 0.95 
        self.position += self.velocity * dt
        self.rect.center = (self.position.x, self.position.y)
        
        # Reduce lifetime and remove when "dead"
        self.lifetime -= dt
        if self.lifetime <= 0:
           self.kill()