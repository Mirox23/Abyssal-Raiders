import pygame
from setting import *
from chemin import PATH, draw_decor, draw_path
from mob import Mob
from tower import Tower
from ui import Button


def draw_wall(screen):
    wall_rect = pygame.Rect(wall_x, 0, wall_width, screen_height)
    pygame.draw.rect(screen, couleur_wall, wall_rect)


def is_on_path(position):
    for i in range(len(PATH) - 1):
        path_zone = pygame.Rect(
            min(PATH[i][0], PATH[i + 1][0]) - 22,
            min(PATH[i][1], PATH[i + 1][1]) - 22,
            abs(PATH[i][0] - PATH[i + 1][0]) + 44,
            abs(PATH[i][1] - PATH[i + 1][1]) + 44,
        )
        if path_zone.collidepoint(position):
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

    enemy_spawned = 0
    spawn_timer = 0
    wall_health = wall_life_start

    placing_tower = False

    button_tower = Button(820, 470, 150, 40, "Tourelle")
    button_new_vague = Button(820, 520, 150, 40, "New Manche")

    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if button_tower.rect.collidepoint(event.pos):
                    placing_tower = True

                elif button_new_vague.rect.collidepoint(event.pos):
                    enemies.clear()
                    enemy_spawned = 0
                    spawn_timer = 0

                elif placing_tower:
                    if (
                        len(towers) < 5
                        and not is_on_path(event.pos)
                        and event.pos[0] < wall_x - 10
                    ):
                        towers.append(Tower(event.pos))
                    placing_tower = False

        # Spawn ennemis
        if enemy_spawned < total_enemies:
            spawn_timer += delta_time
            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                enemies.append(Mob(PATH[0], enemy_speed, couleur_ennemies))
                enemy_spawned += 1

        # Mise à jour ennemis
        enemies_alive = []
        for enemy in enemies:
            if enemy.health <= 0:
                continue

            reached_wall = enemy.move(delta_time, PATH)

            if reached_wall:
                wall_health -= 1
                continue

            enemies_alive.append(enemy)

        enemies = enemies_alive

        # Mise à jour tours
        for tower in towers:
            tower.update(delta_time, enemies)

        # Dessin
        screen.fill(couleur_fond)
        draw_decor(screen, pygame)
        draw_path(screen, pygame)
        draw_wall(screen)

        for tower in towers:
            tower.draw(screen, pygame)

        for enemy in enemies:
            enemy.draw(screen, pygame)

        button_tower.draw(screen, pygame)
        button_new_vague.draw(screen, pygame)

        # Texte infos
        info1 = f"Vie muraille : {wall_health}"
        info2 = f"Tourelles : {len(towers)} / 5"
        info3 = f"Spawn : {enemy_spawned}/{total_enemies}"

        screen.blit(font.render(info1, True, couleur_text), (20, 20))
        screen.blit(font.render(info2, True, couleur_text), (20, 45))
        screen.blit(font.render(info3, True, couleur_text), (20, 70))

        if placing_tower:
            screen.blit(
                font.render("Clique pour placer la tourelle", True, (255, 220, 120)),
                (20, 100),
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()