from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
import pygame
import random
from circleshape import CircleShape
from logger import log_event
from player import Player
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        if self.radius / ASTEROID_MIN_RADIUS == 3:
            self.color = (169, 169, 169)
        elif self.radius / ASTEROID_MIN_RADIUS == 2:
            self.color = (211, 211, 211)
        else:
            self.color = (254, 254, 254)
    def draw(self, screen, camera):
        screen_pos = camera.apply(self.position)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            pygame.draw.circle(screen, "blue", screen_pos, self.radius)
        elif keys[pygame.K_r]:
            pygame.draw.circle(screen, "red", screen_pos, self.radius)
        elif keys[pygame.K_u]:
            self.split()
        else:
            pygame.draw.circle(screen, self.color, screen_pos, self.radius)
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
    def in_area(self, x_1, y_1, x_2, y_2):
        if self.position[0] >= x_1 and self.position[0] <= x_2 and self.position[1] >= y_1 and self.position[1] <= y_2:
            self.kill()
            return
        else:
            return
    def bounce_if_colliding(self, other):
    # 1. Check if they are colliding (and aren't the same asteroid)
        if self != other and self.collides_with(other):
        
            # 2. Find the collision normal (direction from self to other)
            axis = other.position - self.position
            distance = axis.length()
        
        # Prevent division by zero if they occupy the exact same spot
            if distance == 0:
                return
            
            normal = axis.normalize()
        
        # 3. Separate them slightly so they don't get stuck together ("stiction")
            overlap = (self.radius + other.radius) - distance
            self.position -= normal * (overlap / 2)
            other.position += normal * (overlap / 2)
        
        # 4. Swap or reflect velocities along the collision normal (Elastic collision)
        # Using relative velocity
            vel_safe = self.velocity - other.velocity
            vel_along_normal = vel_safe.dot(normal)
        
        # Do not resolve if velocities are separating
            if vel_along_normal < 0:
                return
            
        # Assuming equal mass for simplicity
            impulse = normal * vel_along_normal
            self.velocity -= impulse
            other.velocity += impulse
