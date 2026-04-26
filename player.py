from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
from shot import Shot
from shield import Shield
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from laser import Laser
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        from constants import SCREEN_HEIGHT, SCREEN_WIDTH
        self.rotation = 0
        self.timer = 0
        self.forcefield = False
        self.shield_timer = 15
        self.s_h = SCREEN_HEIGHT
        self.s_w = SCREEN_WIDTH
        self.laser = False
        self.fuel = 15
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        if self.forcefield:
            pygame.draw.circle(screen, "yellow", self.position, self.radius + 10, 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        shot = Shot(self.position[0], self.position[1], SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt, screen):
        keys = pygame.key.get_pressed()
        self.timer -= dt
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            if self.fuel > 0:
                self.move(dt)
        if keys[pygame.K_s]:
            if self.fuel > 0:
                self.move(-dt)
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            if self.fuel > 0:
                self.move(dt)
        if keys[pygame.K_DOWN]:
            if self.fuel > 0:
                self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                self.timer = 0.3
                self.shoot()

        if keys[pygame.K_LSHIFT] and keys[pygame.K_RSHIFT] and keys[pygame.K_a]:
            if keys[pygame.K_l] == True:
                self.laser = True
        elif keys[pygame.K_l] or keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_a] == False:
                self.laser = False

        if keys[pygame.K_d] and keys[pygame.K_RIGHT] and keys[pygame.K_m]:
            self.shoot()


        if self.position[1] > self.s_h:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.s_h

        if self.position[0] > self.s_w:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.s_w
        
        if self.fuel > 0:
            self.fuel -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
