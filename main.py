import pygame
import sys
import math
from asteroidfield import AsteroidField
from shot import Shot
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from shield import Shield
from fuel import Fuel
from shield_field import ShieldField
from fuel_field import FuelField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from bomb import Bomb
from bombfield import BombField
from laser import Laser
from particle import ExplosionParticle
def draw_fuel_bar(screen, player):
    # Bar settings
    x, y = 20, 20
    width, max_height = 20, 150
    
    # Calculate current height
    ratio = player.fuel / player.max_fuel
    current_height = max_height * ratio
    
    # Calculate the Y to grow upwards from a base
    # Let's say the base of the bar is at y=170
    bottom_y = y + max_height
    top_left_y = bottom_y - current_height

    # 1. Draw Background (Gray)
    bg_rect = pygame.Rect(x, y, width, max_height)
    pygame.draw.rect(screen, (50, 50, 50), bg_rect)

    # 2. Draw Fuel (Yellow)
    if current_height > 0:
        fuel_rect = pygame.Rect(x, top_left_y, width, current_height)
        pygame.draw.rect(screen, "yellow", fuel_rect)
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    dt = 0
    score = 0
    points = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    fuel_asteroids = pygame.sprite.Group()
    explodable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    ExplosionParticle.containers = (particles, drawable, updatable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)
    ShieldField.containers = (updatable,)
    BombField.containers = (updatable,)
    FuelField.containers = (updatable,)
    bombfield = BombField()
    shield_field = ShieldField()
    fuelfield = FuelField()
    hurdle_spawner = AsteroidField()
    Shot.containers = (shots, drawable, updatable)
    Shield.containers = (updatable, drawable, shields)
    Fuel.containers = (updatable, drawable, fuel_asteroids)
    shield = Shield(screen)
    asteroid_field = AsteroidField()
    Bomb.containers = (drawable, explodable)
    Laser.containers = (drawable,)
    bomb = Bomb(screen)
    fuel_asteroid = Fuel(screen)
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    laser = Laser(player)
    while True:
        dt = (clock.tick(60) / 1000)
        screen.fill('black')
        pygame.draw.circle(screen, "red", (100, 100), 10)
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        for asteroid in asteroids:
            if asteroid.collides_with(player) == True:
                if player.forcefield == False:
                    log_event("player_hit")
                    print("Game over!")
                    print(f'Your score was {int(score)}')
                    print("High score 1352 by jj-builds")
                    sys.exit()
                else:
                    asteroid.kill()
                    player.forcefield = False
            if laser.collides_with(asteroid) and player.laser == True:
                asteroid.split()
        for shield in shields:
            if shield and player.collides_with(shield):
                player.forcefield = True
                shield.kill()

        for fuel_asteroid in fuel_asteroids:
            if fuel_asteroid and player.collides_with(fuel_asteroid):
                player.fuel = 50
                fuel_asteroid.kill()

        for shot in shots:
            for asteroid in asteroids:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    for i in range(20):
                        p = ExplosionParticle(asteroid.position.x, asteroid.position.y)
                    asteroid.split()
                    shot.kill()
                    points += 1
            for bomb in explodable:
                if shot.collides_with(bomb):
                    my_list = bomb.explode()
                    for asteroid in asteroids:
                        asteroid.in_area(my_list[0], my_list[1], my_list[2], my_list[3])
        for thing in drawable:
            thing.draw(screen)
        score += points
        points = 0
        if player.fuel <= 0:
            text_surface = font.render("NO FUEL", True, (255, 255, 255))
        elif player.fuel > 10:
            text_surface = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        elif player.fuel < 10:
            text_surface = font.render("LOW FUEL", True, (255, 255, 255))
        screen.blit(text_surface, ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT - 50)))
        for thing in updatable:
            thing.update(dt, screen)
        draw_fuel_bar(screen, player)
        pygame.display.flip()
main()