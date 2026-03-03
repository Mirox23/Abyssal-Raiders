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
        self.selected_tower_type = None

        self.tower_button = Button(820, 470, 150, 40, "Tourelle")
        self.phone = PhonePanel()

    def draw_wall(self):
        mur = pygame.Rect(wall_x, 0, wall_width, screen_height)
        pygame.draw.rect(self.screen, couleur_wall, mur)

    def run(self):
        running = True
        while running:
            delta_time = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.phone.handle_click(event.pos)

                    # Phone actions
                    if action == "New Manche":
                        self.enemies.clear()
                        self.enemies_spawned = 0
                        self.spawn_timer = 0
                        self.player_money += money_per_wave

                    # Tower placement
                    if self.tower_button.rect.collidepoint(event.pos):
                        self.place_mode = True

                    elif self.place_mode:
                        # Fenêtre de choix de type de tourelle
                        chosen = self.choose_tower_type(event.pos)
                        if chosen and self.player_money >= tower_price:
                            self.towers.append(chosen)
                            self.player_money -= tower_price
                        self.place_mode = False

            self.update(delta_time)
            self.draw()

        pygame.quit()

    def choose_tower_type(self, pos):
        # Simple click zone pour choisir type
        # Exemple : 2 rectangles au centre
        rect_sniper = pygame.Rect(400, 200, 150, 50)
        rect_canonnier = pygame.Rect(400, 270, 150, 50)
        if rect_sniper.collidepoint(pos):
            return SniperTower(pos)
        elif rect_canonnier.collidepoint(pos):
            return CanonnierTower(pos)
        return None

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

        for tower in self.towers:
            tower.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.tower_button.draw(self.screen)
        self.phone.draw(self.screen)

        self.screen.blit(self.font.render(f"Vie : {self.wall_life}", True, couleur_text), (20, 20))
        self.screen.blit(self.font.render(f"Tours : {len(self.towers)} / {max_towers}", True, couleur_text), (20, 45))
        self.screen.blit(self.font.render(f"Argent : {self.player_money}", True, couleur_text), (20, 70))

        # Choix tourelle fenêtre
        if self.place_mode:
            pygame.draw.rect(self.screen, (60,60,60), (400, 200, 150, 120))
            pygame.draw.rect(self.screen, (0,0,0), (400, 200, 150, 50))
            pygame.draw.rect(self.screen, (50,25,0), (400, 270, 150, 50))
            self.screen.blit(self.font.render("Sniper", True, (255,255,255)), (420,210))
            self.screen.blit(self.font.render("Canonnier", True, (255,255,255)), (420,280))

        pygame.display.flip()