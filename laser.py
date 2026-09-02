import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(self.containers)
        self.player = player

    def draw(self, screen, camera):
        if self.player.laser == True:
            screen_pos = camera.apply(self.player.position)
            self.start = screen_pos.copy()
            self.end = self.start + pygame.Vector2(0, 800).rotate(self.player.rotation)
            pygame.draw.line(screen, "red", self.start, self.end, 2)

    def collides_with(self, asteroid):
        start = self.player.position.copy()
        end = start + pygame.Vector2(0, 800).rotate(self.player.rotation)

        ab = end - start
        ap = asteroid.position - start
        t = max(0, min(1, ap.dot(ab) / ab.length_squared()))
        closest = start + ab * t

        return asteroid.position.distance_to(closest) <= asteroid.radius

