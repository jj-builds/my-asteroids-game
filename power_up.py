import pygame
import random
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from particle import ExplosionParticle
class Powerup(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(random.randint(1, 76), random.randint(1, 76))
        self.timer = 7
        self.drawable = True
        self.s_h = SCREEN_HEIGHT
        self.s_w = SCREEN_WIDTH
        self.is_visible = True
    
    def draw(self, screen, camera):
        screen_pos = camera.apply(self.position)
        if self.is_visible:
            r = self.radius
        
            points = [
            screen_pos + pygame.Vector2(-r * 0.4, -r), # Start: Top Left
            screen_pos + pygame.Vector2(-r * 0.4, 0.17 * r),  # 1. Vertical line down
            screen_pos + pygame.Vector2(0, 0.17 * r),         # 2. Flat line
            screen_pos + pygame.Vector2(r * 0.4, r),   # 3. Diagonal line down
            screen_pos + pygame.Vector2(r * 0.4, -(0.17 * r)),   # 4. Vertical line up
            screen_pos + pygame.Vector2(0, -(0.17 * r)),         # 5. Horizontal line across
        ]
        pygame.draw.polygon(screen, "yellow", points)

    def update(self, dt, screen):
        self.position += self.velocity * dt
        if random.random() < 0.03: # 10% chance per frame to drop a spark
            counter = 1
            while counter > 0:
                ExplosionParticle(self.position.x, self.position.y, "yellow", 0.93, 1)
                counter -= 1