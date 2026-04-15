from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
from shot import Shot
from shield import Shield
import pygame
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.forcefield = False
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        shot = Shot(self.position[0], self.position[1], SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt, screen):
        from constants import SHIELD_TIMER
        keys = pygame.key.get_pressed()
        self.timer -= dt
        SHIELD_TIMER -= dt
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.timer > 0:
                return
            else:
                self.timer = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
        if SHIELD_TIMER <= 0:
            self.forcefield = False
            SHIELD_TIMER = 15
        if super().collides_with(Shield) == True:
            self.forcefield = True


    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

