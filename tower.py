import pygame
from setting import *
from projectile import Projectile


class Tower:
    def __init__(self, position):

        self.x = position[0]
        self.y = position[1]

        self.range = tower_range
        self.fire_interval = tower_fire_interval
        self.time_since_last_shot = 0

        self.projectiles = []

        self.size = 15
        self.color = couleur_tower

    def update(self, delta_time, enemies):

        self.time_since_last_shot += delta_time

        if self.time_since_last_shot >= self.fire_interval:

            for enemy in enemies:

                dx = enemy.x - self.x
                dy = enemy.y - self.y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance <= self.range:
                    projectile = Projectile(self.x, self.y, enemy)
                    self.projectiles.append(projectile)
                    self.time_since_last_shot = 0
                    break

        active_projectiles = []

        for projectile in self.projectiles:
            projectile.update(delta_time)
            if projectile.active:
                active_projectiles.append(projectile)

        self.projectiles = active_projectiles

    def draw(self, screen):

        # Cercle de portée
        pygame.draw.circle(screen, (100, 100, 255), (self.x, self.y), self.range, 1)

        # Tour
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

        for projectile in self.projectiles:
            projectile.draw(screen)