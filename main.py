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
from shield_field import ShieldField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from bomb import Bomb
from bombfield import BombField
from laser import Laser
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
    explodable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)
    ShieldField.containers = (updatable,)
    BombField.containers = (updatable,)
    bombfield = BombField()
    shield_field = ShieldField()
    hurdle_spawner = AsteroidField()
    Shot.containers = (shots, drawable, updatable)
    Shield.containers = (updatable, drawable, shields)
    shield = Shield(screen)
    asteroid_field = AsteroidField()
    Bomb.containers = (drawable, explodable)
    Laser.containers = (drawable,)
    bomb = Bomb(screen)
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    laser = Laser(player)
    while True:
        dt = (clock.tick(60) / 1000)
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill('black')
        for thing in updatable:
            thing.update(dt, screen)

        for asteroid in asteroids:
            if asteroid.collides_with(player) == True:
                if player.forcefield == False:
                    log_event("player_hit")
                    print("Game over!")
                    print(f'your score was {int(score)}')
                    print("high score 1352 by jj-builds")
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

        for shot in shots:
            for asteroid in asteroids:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
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
        if player.fuel > 10:
            text_surface = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        else:
            text_surface = font.render("LOW FUEL", True, (255, 255, 255))
        screen.blit(text_surface, ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT - 50)))
        pygame.display.flip()
main()



