import pygame
from circleshape import CircleShape

class Planet(CircleShape):
    def __init__(self, x, y, radius, picture="pictures/earth.png", name="NewFoundLand2"):
        super().__init__(x, y, radius)
        self.name = name
        self.is_selected = False

        size = radius * 2
        self.image = pygame.image.load(picture).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (size, size))

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.position)

        image_rect = self.image.get_rect(center=screen_pos)
        screen.blit(self.image, image_rect)

        if self.is_selected:
            pygame.draw.circle(
                screen,
                "blue",
                screen_pos,
                self.radius + 5,
                width=2,
            )