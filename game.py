import pygame
from setting import *
from chemin import PATH, draw_decor, draw_path
from mob import Mob
from tower import Tower, SniperTower, CanonnierTower
from ui import Button, PhonePanel


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Abyssal Raiders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 22)

        self.enemies = []
        self.towers = []

        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.wall_life = wall_life_start
        self.player_money = start_money

        self.place_mode = False
        self.selected_tower_class = None
        self.selected_tower_for_buttons = None

        self.tower_button = Button(820, 470, 150, 40, "Tourelle")
        self.phone = PhonePanel()

    def draw_wall(self):
        mur = pygame.Rect(wall_x, 0, wall_width, screen_height)
        pygame.draw.rect(self.screen, couleur_wall, mur)

    def is_on_path(self, position):
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

    def run(self):
        running = True
        while running:
            delta_time = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.phone.handle_click(event.pos)

                    if action == "New Manche":
                        self.enemies.clear()
                        self.enemies_spawned = 0
                        self.spawn_timer = 0
                        self.player_money += money_per_wave

                    if self.tower_button.rect.collidepoint(event.pos):
                        self.place_mode = True

                    # Clique sur tour existante pour afficher boutons
                    self.selected_tower_for_buttons = None
                    for tower in self.towers:
                        dx = event.pos[0] - tower.x
                        dy = event.pos[1] - tower.y
                        distance = (dx ** 2 + dy ** 2) ** 0.5
                        if distance <= tower.size:
                            self.selected_tower_for_buttons = tower
                            break

                    # Pose tour
                    if self.place_mode and self.selected_tower_class:
                        if (len(self.towers) < max_towers and
                            not self.is_on_path(event.pos) and
                            event.pos[0] < wall_x - 10 and
                            self.player_money >= tower_price):
                            tower_instance = self.selected_tower_class(event.pos)
                            self.towers.append(tower_instance)
                            self.player_money -= tower_price
                            self.place_mode = False
                            self.selected_tower_class = None

            self.update(delta_time)
            self.draw()

        pygame.quit()

    def update(self, delta_time):
        # Spawn ennemis
        if self.enemies_spawned < total_enemies:
            self.spawn_timer += delta_time
            if self.spawn_timer >= spawn_interval:
                self.spawn_timer = 0
                self.enemies.append(Mob(PATH[0], enemy_speed, couleur_ennemies))
                self.enemies_spawned += 1

        # Update ennemis
        alive = []
        for enemy in self.enemies:
            if enemy.health <= 0:
                self.player_money += money_per_kill
                continue
            reach_end = enemy.move(delta_time, PATH)
            if reach_end:
                self.wall_life -= 1
                continue
            alive.append(enemy)
        self.enemies = alive

        # Update tours
        for tower in self.towers:
            tower.update(delta_time, self.enemies)

    def draw(self):
        self.screen.fill(couleur_fond)
        draw_decor(self.screen, pygame)
        draw_path(self.screen, pygame)
        self.draw_wall()

        # Tours et projectiles
        for tower in self.towers:
            tower.draw(self.screen)

        # Afficher boutons de la tour sélectionnée
        if self.selected_tower_for_buttons:
            tower = self.selected_tower_for_buttons
            size = 30
            spacing = 5
            x_start = tower.x - size - spacing
            y_start = tower.y + tower.size + 5

            # Amélioration
            pygame.draw.rect(self.screen, (0,255,0), (x_start, y_start, size, size))
            self.screen.blit(self.font.render("A", True, (0,0,0)), (x_start + 8, y_start + 5))

            # Niveau
            pygame.draw.rect(self.screen, (0,0,255), (x_start + size + spacing, y_start, size, size))
            self.screen.blit(self.font.render("N", True, (255,255,255)), (x_start + size + spacing + 8, y_start + 5))

            # Type
            if tower.type == "Canonnier":
                pygame.draw.rect(self.screen, (139,69,19), (x_start + 2*(size + spacing), y_start, size, size))
                self.screen.blit(self.font.render("C", True, (255,255,255)), (x_start + 2*(size + spacing) + 8, y_start + 5))

        # Mobs
        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.tower_button.draw(self.screen)
        self.phone.draw(self.screen)

        # Infos
        self.screen.blit(self.font.render(f"Vie : {self.wall_life}", True, couleur_text), (20, 20))
        self.screen.blit(self.font.render(f"Tours : {len(self.towers)} / {max_towers}", True, couleur_text), (20, 45))
        self.screen.blit(self.font.render(f"Argent : {self.player_money}", True, couleur_text), (20, 70))

        # Choix tourelle fenêtre
        # Affichage choix tour
        if self.place_mode and self.selected_tower_class is None:
            sniper_rect = pygame.Rect(400, 200, 150, 50)
            canonnier_rect = pygame.Rect(400, 270, 150, 50)

            pygame.draw.rect(self.screen, (0,0,0), sniper_rect)
            pygame.draw.rect(self.screen, (139,69,19), canonnier_rect)

            self.screen.blit(self.font.render("Sniper", True, (255,255,255)), (420,210))
            self.screen.blit(self.font.render("Canonnier", True, (255,255,255)), (420,280))

            # Détection clic
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:  # clic gauche
                if sniper_rect.collidepoint(mouse_pos):
                    self.selected_tower_class = SniperTower
                elif canonnier_rect.collidepoint(mouse_pos):
                    self.selected_tower_class = CanonnierTower

        pygame.display.flip()