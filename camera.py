import pygame
class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_center = pygame.Vector2(screen_width / 2, screen_height / 2)
        self.target_pos = pygame.Vector2(0, 0)

    def update(self, target_world_pos):
        self.target_pos = target_world_pos

    def apply(self, world_pos):
        """Converts world coordinates to screen coordinates."""
        return world_pos - self.target_pos + self.screen_center