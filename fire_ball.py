import pygame
import math


class Fireball(pygame.sprite.Sprite):
    containers = None

    def __init__(self, x, y):
        if Fireball.containers:
            super().__init__(Fireball.containers)
        else:
            super().__init__()
            
        self.position = pygame.Vector2(x, y)
        self.max_radius = 200
        self.lifetime = 0.2
        self.timer = self.lifetime

    def update(self, dt, screen):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def draw(self, screen, camera):
        progress = 1.0 - (self.timer / self.lifetime)
        current_radius = int(self.max_radius * progress)
        
        if current_radius > 5:
            screen_pos = camera.apply(self.position)
            points = []
            num_spikes = 8

            for i in range(num_spikes * 2):
                r = current_radius if i % 2 == 0 else current_radius * 0.4
                angle = i * (math.pi / num_spikes)
                
                x = screen_pos.x + r * math.cos(angle)
                y = screen_pos.y + r * math.sin(angle)
                points.append((x, y))
            
            pygame.draw.polygon(screen, "orange", points)

            inner_points = [
                (p[0] * 0.7 + screen_pos.x * 0.3, p[1] * 0.7 + screen_pos.y * 0.3)
                for p in points
            ]
            pygame.draw.polygon(screen, "yellow", inner_points)