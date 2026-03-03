import pygame
from setting import *
from chemin import PATH, draw_decor, draw_path
from mob import Mob
from tower import Tower
from ui import Button, PhonePanel


def draw_wall(screen):
    mur = pygame.Rect(wall_x, 0, wall_width, screen_height)
    pygame.draw.rect(screen, couleur_wall, mur)


def is_on_path(position):
    for i in range(len(PATH) - 1):
        zone = pygame.Rect(
            min(PATH[i][0], PATH[i + 1][0]) - 22,
            min(PATH[i][1], PATH[i + 1][1]) - 22,
            abs(PATH[i][0] - PATH[i + 1][0]) + 44,
            abs(PATH[i][1] - PATH[i + 1][1]) + 44,
        )
        if zone.collidepoint(position):
            return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Abyssal Raiders")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    enemies = []
    towers = []

    enemies_spawned = 0
    spawn_timer = 0
    wall_life = wall_life_start
    player_money = 20

    place_mode = False

    tower_button = Button(820, 470, 150, 40, "Tourelle")
    phone = PhonePanel()

    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Gestion Phone
                action = phone.handle_click(event.pos)

                if action == "New Manche":
                    enemies.clear()
                    enemies_spawned = 0
                    spawn_timer = 0

                if tower_button.rect.collidepoint(event.pos):
                    place_mode = True

                elif place_mode:
                    if (
                        len(towers) < max_towers
                        and not is_on_path(event.pos)
                        and event.pos[0] < wall_x - 10
                        and player_money >= tower_price
                    ):
                        towers.append(Tower(event.pos))
                        player_money -= tower_price

                    place_mode = False

        # Spawn ennemis
        if enemies_spawned < total_enemies:
            spawn_timer += delta_time
            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                enemies.append(Mob(PATH[0], enemy_speed, couleur_ennemies))
                enemies_spawned += 1

        # Update ennemis
        alive = []
        for enemy in enemies:
            if enemy.health <= 0:
                player_money += 2
                continue

            reach_end = enemy.move(delta_time, PATH)

            if reach_end:
                wall_life -= 1
                continue

            alive.append(enemy)

        # Fin de manche bonus
        if enemies_spawned == total_enemies and len(alive) == 0:
            player_money += 15
            enemies_spawned = 0

        enemies = alive

        # Update tours
        for tower in towers:
            tower.update(delta_time, enemies)

        # DRAW
        screen.fill(couleur_fond)
        draw_decor(screen, pygame)
        draw_path(screen, pygame)
        draw_wall(screen)

        for tower in towers:
            tower.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        tower_button.draw(screen)
        phone.draw(screen)

        screen.blit(font.render(f"Vie : {wall_life}", True, couleur_text), (20, 20))
        screen.blit(font.render(f"Tours : {len(towers)} / {max_towers}", True, couleur_text), (20, 45))
        screen.blit(font.render(f"Argent : {player_money}", True, couleur_text), (20, 70))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()