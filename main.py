import pygame
from camera import Camera
import sys
import math
from starfield import Starfield
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
from power_up import Powerup
from powerupfield import PowerupField as pf
from fire_ball import Fireball
from planet import Planet
def main():
    game_started = False
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    font2 = pygame.font.SysFont("Courier New", 150)
    showing_rules = False
    while not game_started and not showing_rules:
        screen.fill('black') # Clear the screen each frame
        
        button_rect = pygame.Rect((SCREEN_WIDTH / 2 - 100), (SCREEN_HEIGHT - 100), 200, 50)
        pygame.draw.rect(screen, "yellow", button_rect)
        text_surface = font.render("Play", True, (0, 0, 0))
        welcoming = font2.render("Asteroids", True, (255, 255, 255)) 
        welcoming_rect = welcoming.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150))# White text
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(welcoming, welcoming_rect)
        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # This must be inside the event loop!
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        game_started = True
        pygame.display.flip() # Render the menu frame
        clock.tick(60)        # Cap the menu frame rate
    if game_started and not showing_rules:
        dt = 0
        score = 0
        points = 0
        planets = pygame.sprite.Group()
        Powerups = pygame.sprite.Group()
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        shields = pygame.sprite.Group()
        particles = pygame.sprite.Group()
        fuel_asteroids = pygame.sprite.Group()
        explodable = pygame.sprite.Group()
        Planet.containers = (drawable, planets)
        Player.containers = (updatable,)
        ExplosionParticle.containers = (particles, drawable, updatable)
        Asteroid.containers = (updatable, drawable, asteroids)
        AsteroidField.containers = (updatable,)
        ShieldField.containers = (updatable,)
        BombField.containers = (updatable,)
        FuelField.containers = (updatable,)
        pf.containers = (updatable,)
        bombfield = BombField()
        shield_field = ShieldField()
        fuelfield = FuelField()
        pF = pf()
        camera1 = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        Powerup.containers = (drawable, updatable, Powerups)
        Shot.containers = (shots, drawable, updatable)
        Shield.containers = (updatable, drawable, shields)
        Fuel.containers = (updatable, drawable, fuel_asteroids)
        shield = Shield(screen)
        Bomb.containers = (drawable, explodable)
        Laser.containers = (drawable,)
        bomb = Bomb(screen)
        fuel_asteroid = Fuel(screen)
        player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
        laser = Laser(player)
        my_num = 7
        my_planet = Planet(255, 300, 100)
        planet2 = Planet(455, 302, 50, "pictures/luna.png", "Luna")
        starfield = Starfield(SCREEN_WIDTH, SCREEN_HEIGHT)
        Power_up = Powerup(50, 50, 25)
        Power_up.containers = (Powerups,)
        fireballs = pygame.sprite.Group()
        Fireball.containers = (drawable, updatable, fireballs)
        asteroid_field = AsteroidField(player)
        selected_planet = None
        while True:
            dt = (clock.tick(60) / 1000)
            screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_screen_pos = pygame.mouse.get_pos()
                        selected_planet = None
                        for p in planets:
                            p.is_selected = False
                            screen_pos = camera1.apply(p.position)
                            dist = pygame.Vector2(screen_pos).distance_to(pygame.Vector2(mouse_screen_pos))
                            if dist <= p.radius:
                                p.is_selected = True
                                selected_planet = p
                                print(f"Selected: {p.name}")
                                break

    # Key Press for Landing and Launching
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                            if player.state == "landed":
                                print("Initiating launch...")
                                player.start_launch()
                            if player.state == "flying" and selected_planet is not None:
                                print(f"Initiating landing on {selected_planet.name}...")
                                player.start_landing(selected_planet)
            if player.state == "landed":
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_l:
                            if player.state == "landed":
                                print("Initiating launch...")
                                player.start_launch()
                                continue
                info_rect = pygame.Rect((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), 200, 50)
                pygame.draw.rect(screen, "white", info_rect, 20)
                continue
            starfield.draw(screen, camera1)
            camera1.update(player.position)
            for asteroid in asteroids:
                if asteroid.collides_with(player) == True and player.state == "flying":
                    if player.forcefield == False:
                        log_event("player_hit")
                        print("Game over!")
                        print(f'Your score was {int(score)}')
                        print("High scoare 1352 by jj-builds")
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
            asteroid_list = list(asteroids)

            for i in range(len(asteroid_list)):
                for j in range(i + 1, len(asteroid_list)):
                    asteroid_list[i].bounce_if_colliding(asteroid_list[j])
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
                        Fireball(bomb.position.x, bomb.position.y)
                        for asteroid in asteroids:
                            asteroid.in_area(my_list[0], my_list[1], my_list[2], my_list[3])
            for thing in drawable:
                thing.draw(screen, camera1)
            if my_num >= 0 and player.laser == True:
                my_num -= dt
                player.laser = True
            else:
                player.laser = False
                my_num = 7
            for pPowerup in Powerups:
                if player.collides_with(pPowerup) and pPowerup.is_visible:
                    pPowerup.is_visible = False
                    pPowerup.kill()
                    player.laser = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

    # Mouse Click Selection
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_screen_pos = pygame.mouse.get_pos()
                    selected_planet = None
                    for p in planets:
                        p.is_selected = False
                        screen_pos = camera1.apply(p.position)
                        dist = pygame.Vector2(screen_pos).distance_to(pygame.Vector2(mouse_screen_pos))
                        if dist <= p.radius:
                            p.is_selected = True
                            selected_planet = p
                            print(f"Selected: {p.name}")
                            break

    # Key Press for Landing and Launching
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                            if player.state == "landed":
                                print("Initiating launch...")
                                player.start_launch()
                            if player.state == "flying" and selected_planet is not None:
                                print(f"Initiating landing on {selected_planet.name}...")
                                player.start_landing(selected_planet)
            score += points
            points = 0
            
            if player.fuel <= 0:
                text = font.render("NO FUEL", True, (255, 255, 255))
            elif player.fuel > 10:
                text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
            elif player.fuel < 10:
                text = font.render("LOW FUEL", True, (255, 255, 255))
            screen.blit(text, ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT - 50)))
            for thing in updatable:
                thing.update(dt, screen)
            draw_fuel_bar(screen, player)
            player.draw(screen, camera1)
            if player.state == "landed":
                screen.fill('black')
            pygame.display.flip()
    pygame.quit()
def draw_fuel_bar(screen, player):
    x, y = 20, 20
    width, max_height = 20, 200
    ratio = player.fuel / player.max_fuel
    current_height = max_height * ratio
    bottom_y = y + max_height
    top_left_y = bottom_y - current_height
    bg_rect = pygame.Rect(x, y, width, max_height)
    pygame.draw.rect(screen, (50, 50, 50), bg_rect)
    if current_height > 0:
        fuel_rect = pygame.Rect(x, top_left_y, width, current_height)
        pygame.draw.rect(screen, "yellow", fuel_rect)
main()