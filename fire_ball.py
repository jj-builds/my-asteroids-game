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
        self.max_radius = 200  # Keep it punchy and arcade-sized!
        self.lifetime = 0.2    # Fast, snappy explosion
        self.timer = self.lifetime

    def update(self, dt, screen):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def draw(self, screen):
        # Calculate expansion progress (0.0 to 1.0)
        progress = 1.0 - (self.timer / self.lifetime)
        current_radius = int(self.max_radius * progress)
        
        if current_radius > 5:
            # Generate a jagged starburst/spike pattern using trig
            points = []
            num_spikes = 8
            for i in range(num_spikes * 2):
                # Alternate between outer spike tip and inner trough
                r = current_radius if i % 2 == 0 else current_radius * 0.4
                angle = i * (math.pi / num_spikes)
                
                x = self.position.x + r * math.cos(angle)
                y = self.position.y + r * math.sin(angle)
                points.append((x, y))
            
            # Draw a solid, bright yellow-orange retro starburst
            pygame.draw.polygon(screen, "orange", points)
            # Inner core highlight for extra arcade punch
            pygame.draw.polygon(screen, "yellow", [(p[0]*0.7 + self.position.x*0.3, p[1]*0.7 + self.position.y*0.3) for p in points])