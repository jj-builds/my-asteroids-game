import math
import pygame
from circleshape import CircleShape
from shot import Shot
from shield import Shield
from constants import *
from laser import Laser

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0.0
        self.timer = 0.0
        self.forcefield = False
        self.shield_timer = 15
        self.s_h = SCREEN_HEIGHT
        self.s_w = SCREEN_WIDTH
        self.laser = False
        self.fuel = 50.0
        self.velocity = pygame.Vector2(0, 0)
        self.angular_velocity = 0.0
        self.max_fuel = 50.0
        self.ship = ""
        self.image = pygame.image.load("pictures/lance.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.flame = pygame.image.load("pictures/medium+0.png")
        self.flame = pygame.transform.scale(self.flame, (60, 60))
        self.thrusting = False
        # Landing / Launching System
        self.time = 0.0
        self.base_radius = PLAYER_RADIUS
        self.scale = 1.0
        self.transition_speed = 0.9
        self.state = "flying"
        self.land_stage = None  # "align_forward", "burn_forward", "retrograde", "retro_burn", "shrink"
        self.land_timer = 0.0
        self.landed_planet = None
        self.counter = 60.0
        self.camera = None
    def draw(self, screen, camera):
        if self.scale <= 0.02 or self.state == "landed":
            return

        screen_pos = camera.apply(self.position)
        image_angle = -self.rotation + 180
        if self.thrusting:
            # Flame: move it aft, opposite the direction of travel
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            flame_world_pos = self.position - forward * 25
            flame_screen_pos = camera.apply(flame_world_pos)
            rotated_flame = pygame.transform.rotate(self.flame, image_angle)
            flame_rect = rotated_flame.get_rect(center=flame_screen_pos)
            screen.blit(rotated_flame, flame_rect)

        rotated_ship = pygame.transform.rotate(self.image, image_angle)
        ship_rect = rotated_ship.get_rect(center=screen_pos)
        screen.blit(rotated_ship, ship_rect)
    def start_landing(self, planet):
        if self.state == "flying" and planet is not None:
            self.state = "landing"
            self.land_stage = "align_forward"
            self.landed_planet = planet
            self.land_timer = 0.0
            self.velocity = pygame.Vector2(0, 0)
            self.angular_velocity = 0.0

    def start_launch(self):
        if self.state == "landed":
            self.state = "launching"

    def rotate_towards(self, target_angle, dt, speed=260.0):
    # Shortest distance between two angles in degrees (-180 to 180)
        diff = (target_angle - self.rotation + 180.0) % 360.0 - 180.0
        turn_step = speed * dt

        if abs(diff) <= turn_step:
            self.rotation = target_angle % 360.0
            return True
    
        if diff > 0:
            self.rotation = (self.rotation + turn_step) % 360.0
        else:
            self.rotation = (self.rotation - turn_step) % 360.0

        return False

    def rotate(self, dt):
        self.angular_velocity += PLAYER_ROT_ACCEL * dt
        self.fuel -= (dt / 10.0)

    def move(self, dt, screen):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCEL * dt
        self.fuel -= ((2.0 / 3.0) * dt)
    def shoot(self):
        shot = Shot(self.position[0], self.position[1], SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt, screen):
        self.thrusting = False
        # --- MULTI-STAGE LANDING SEQUENCE ---
        if self.state == "landing":
            to_planet = self.landed_planet.position - self.position
            dist = to_planet.length()

    # Target angles matching pygame.Vector2(0, 1) down-baseline
            if dist > 0:
                angle_to_planet = pygame.Vector2(0, 1).angle_to(to_planet) % 360.0
            else:
                angle_to_planet = self.rotation
                angle_away_from_planet = (angle_to_planet + 180.0) % 360.0

    # Helper vectors for Option 2 lateral damping
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            right = forward.rotate(90)
            angle_away_from_planet = (angle_to_planet + 180.0) % 360.0
    # Step 1: Turn ship nose-first towards planet
        if self.land_stage == "align_forward":
        # Dampen any residual sideways drift while turning
            lateral_speed = self.velocity.dot(right)
            self.velocity -= right * lateral_speed * 6.0 * dt
            self.position += self.velocity * dt

            aligned = self.rotate_towards(angle_to_planet, dt, speed=260.0)
            if aligned:
                self.land_stage = "burn_forward"
            self.land_timer = 0.0

    # Step 2: Accelerate towards the planet with lateral damping
        elif self.land_stage == "burn_forward":
            self.land_timer += dt

            # Dampen lateral drift
            lateral_speed = self.velocity.dot(right)
            self.velocity -= right * lateral_speed * 8.0 * dt

            # Accelerate forward
            self.velocity += forward * 320.0 * dt
            self.position += self.velocity * dt

            # Transition once approaching surface or timer limits
            if dist <= (self.landed_planet.radius * 1.5) or self.land_timer > 2.0:
                self.land_stage = "retrograde"
                self.time = self.land_timer
                self.land_timer = 0.0

        # Step 3: Rotate 180 degrees (flip around for retro-burn)
                # Step 3: Rotate 180 degrees (flip around for retro-burn)
        elif self.land_stage == "retrograde":
            # Dampen lateral wobble
            lateral_speed = self.velocity.dot(right)
            self.velocity -= right * lateral_speed * 6.0 * dt

            # Optional: Start gentle deceleration while turning so you don't overshoot
            self.position += self.velocity * dt

            # Smooth turn speed: 360 deg/sec takes exactly 0.5s to flip 180 degrees
            aligned = self.rotate_towards(angle_away_from_planet, dt, speed=360.0)
            if aligned:
                self.land_stage = "retro_burn"
                self.land_timer = 0.0

        # Step 4: Decelerate with retro thrusters into planet center
        elif self.land_stage == "retro_burn":
            self.land_timer += dt

            # Rapidly brake velocity toward 0
            if self.velocity.length_squared() > 0:
                speed = self.velocity.length()
                brake_speed = max(0.0, speed - 250.0 * dt)
                self.velocity = self.velocity.normalize() * brake_speed

            self.position += self.velocity * dt

            if self.land_timer >= 1.0 or dist <= 1.0 or self.velocity.length() < 5.0:
                self.velocity = pygame.Vector2(0, 0)
                self.land_stage = "shrink"

        # Step 5: Shrink down and land on surface
        elif self.land_stage == "shrink":
            self.counter -= dt
            self.scale -= dt * self.transition_speed
            self.radius = self.base_radius * max(0.0, self.scale)
            self.image = pygame.transform.scale(self.image, (self.counter, self.counter))
            if dist > 0:
                self.position += to_planet * (dt * 3.0)

            if self.scale <= 0.0:
                self.scale = 0.0
                self.radius = 0
                self.velocity = pygame.Vector2(0, 0)
                self.position = pygame.Vector2(self.landed_planet.position)
                self.state = "landed"
                self.land_stage = None
                print("Touchdown on surface!")
            return

        # --- LAUNCHING SEQUENCE ---
        if self.state == "launching":
            self.counter += dt
            self.image = pygame.transform.scale(self.image, (self.counter, self.counter))
            self.scale += dt * self.transition_speed
            self.radius = self.base_radius * min(1.0, self.scale)
            if self.scale >= 0.99:
                self.state = "flying"
                self.scale = 1.0
                self.radius = self.base_radius
                self.fuel = self.max_fuel
                self.landed_planet = None
                print("Launched into space!")
            return

        elif self.state == "landed":
            if self.landed_planet:
                self.position = pygame.Vector2(self.landed_planet.position)
            return

                # --- NORMAL FLIGHT CONTROLS ---
        if self.fuel > 0:
            keys = pygame.key.get_pressed()
            self.timer -= dt
            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_w]:
                if self.fuel > 0:
                    self.thrusting = True
                    self.move(dt, screen)
            if keys[pygame.K_s]:
                if self.fuel > 0:
                    self.thrusting = True
                    self.move(-dt, screen)
            if keys[pygame.K_LEFT]:
                self.rotate(-dt)
            if keys[pygame.K_RIGHT]:
                self.rotate(dt)
            if keys[pygame.K_UP]:
                if self.fuel > 0:
                    self.thrusting = True
                    self.move(dt, screen)
            if keys[pygame.K_DOWN]:
                if self.fuel > 0:
                    self.thrusting = True
                    self.move(-dt, screen)
            if keys[pygame.K_SPACE]:
                if self.timer <= 0:
                    self.timer = 0.3
                    self.shoot()

            if keys[pygame.K_LSHIFT] and keys[pygame.K_RSHIFT] and keys[pygame.K_a] and keys[pygame.K_l]:
                self.laser = True

            if keys[pygame.K_d] and keys[pygame.K_n] and keys[pygame.K_RIGHT] == True and keys[pygame.K_m] == False:
                self.shoot()

        # Update position and apply deceleration / inertia
        self.position += self.velocity * dt
        self.velocity *= PLAYER_FRICTION
        self.rotation += self.angular_velocity * dt
        self.angular_velocity *= PLAYER_FRICTION