import pygame
import random


class Starfield:
    def __init__(self, screen_width, screen_height, count=200):
        self.width = screen_width
        self.height = screen_height
        # Generate random stars across the screen
        self.stars = [
            (
                pygame.Vector2(random.uniform(0, screen_width), random.uniform(0, screen_height)),
                random.choice([1, 2]),          # Radius / size
                random.uniform(0.2, 0.8)        # Parallax depth factor (closer stars move faster)
            )
            for _ in range(count)
        ]

    def draw(self, screen, camera):
        for pos, size, depth in self.stars:
            # Shift star position based on player's world coordinates and depth
            screen_x = (pos.x - camera.target_pos.x * depth) % self.width
            screen_y = (pos.y - camera.target_pos.y * depth) % self.height

            # Choose color brightness based on size/depth
            color = (255, 255, 255) if size == 2 else (160, 160, 160)
            pygame.draw.circle(screen, color, (screen_x, screen_y), size)