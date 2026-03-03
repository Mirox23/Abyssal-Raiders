import pygame
from setting import *
from chemin import PATH, draw_decor, draw_path
from mob import Mob
from tower import Tower
from ui import Button


def draw_wall(screen):
    mur = pygame.Rect(wall_x, 0, wall_width, screen_height)
    pygame.draw.rect(screen, couleur_wall, mur)


def position_on_path(position):

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
    font = pygame.font.SysFont("consolas", 22) # consolas = police de caractère

    enemies = []
    towers = []

    enemies_spawned = 0
    spawn_timer = 0

    wall_life = wall_life_start
    money = start_money
    wave_finished = False

    tower_mode = False

    button_tower = Button(820, 470, 150, 40, "Tourelle")
    button_new = Button(820, 520, 150, 40, "New Manche")

    running = True

    while running:

        delta_time = clock.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if button_tower.zone.collidepoint(event.pos):
                    tower_mode = True

                elif button_new.zone.collidepoint(event.pos):
                    enemies.clear()
                    enemies_spawned = 0
                    spawn_timer = 0
                    wave_finished = False

                elif tower_mode:

                    if (
                        len(towers) < max_towers 
                        and money >= tower_price
                        and not position_on_path(event.pos)
                        and event.pos[0] < wall_x - 10 
                    ):
                        towers.append(Tower(event.pos))
                        money -= tower_price

                    tower_mode = False

        # Spawn
        if enemies_spawned < total_enemies:

            spawn_timer += delta_time

            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                enemies.append(Mob(PATH[0], enemy_speed, couleur_ennemies))
                enemies_spawned += 1

        # Update enemies
        alive_enemies = []

        for enemy in enemies:

            if enemy.health <= 0:
                money += money_per_kill
                continue

            reached_end = enemy.move(delta_time, PATH)

            if reached_end:
                wall_life -= 1
                continue

            alive_enemies.append(enemy)

        enemies = alive_enemies

        # Fin de vague
        if enemies_spawned == total_enemies and len(enemies) == 0 and not wave_finished:
            money += money_per_wave
            wave_finished = True

        # Update towers
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

        button_tower.draw(screen)
        button_new.draw(screen)

        screen.blit(font.render(f"Vie : {wall_life}", True, couleur_text), (20, 20))
        screen.blit(font.render(f"Tours : {len(towers)} / {max_towers}", True, couleur_text), (20, 45))
        screen.blit(font.render(f"Spawn : {enemies_spawned}/{total_enemies}", True, couleur_text), (20, 70))
        screen.blit(font.render(f"Argent : {money}", True, couleur_text), (20, 95))

        if tower_mode:
            screen.blit(font.render("Clique pour placer la tourelle", True, (255, 220, 120)), (20, 120))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()