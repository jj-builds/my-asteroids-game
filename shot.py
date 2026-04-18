import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.s_h = SCREEN_HEIGHT
        self.s_w = SCREEN_WIDTH

    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.position, self.radius, LINE_WIDTH)
    def update(self, dt, screen):
        keys = pygame.key.get_pressed()
        self.position += (self.velocity * dt)
        if self.position[1] > self.s_h:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.s_h

        if self.position[0] > self.s_w:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.s_w

        if keys[pygame.K_e]:
            self.kill()
        if keys[pygame.K_SPACE]:
            if keys[pygame.K_m]:    
                if keys[pygame.K_COMMA]:
                    if keys[pygame.K_PERIOD]:
                        self.kill()
