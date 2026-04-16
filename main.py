import pygame
import sys
from asteroidfield import AsteroidField
from shot import Shot
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from shield import Shield
from shield_field import ShieldField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)
    ShieldField.containers = (updatable,)
    shield_field = ShieldField()
    hurdle_spawner = AsteroidField()
    Shot.containers = (shots, drawable, updatable)
    Shield.containers = (updatable, drawable, shields)
    shield = Shield(screen)
    asteroid_field = AsteroidField()
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
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
                    sys.exit()
                else:
                    asteroid.kill()
                    player.forcefield = False
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
        for thing in drawable:
            thing.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
