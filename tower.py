import pygame
from setting import *
from projectile import Projectile

class Tower:
    def __init__(self, position):
        self.x, self.y = position
        self.size = 15
        self.range = tower_range
        self.fire_interval = tower_fire_interval
        self.time_since_last_shot = 0
        self.projectiles = []
        self.color = couleur_tower
        self.type = "Base"
        self.level = 1

    def update(self, delta_time, enemies):
        self.time_since_last_shot += delta_time
        if self.time_since_last_shot >= self.fire_interval:
            for enemy in enemies:
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                distance = (dx**2 + dy**2)**0.5
                if distance <= self.range:
                    self.projectiles.append(Projectile(self.x, self.y, enemy))
                    self.time_since_last_shot = 0
                    break

        # Update projectiles
        active_projectiles = []
        for p in self.projectiles:
            p.update(delta_time)
            if p.active:
                active_projectiles.append(p)
        self.projectiles = active_projectiles

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (100,100,255), (int(self.x), int(self.y)), self.range, 1)
        for p in self.projectiles:
            p.draw(screen)

class SniperTower(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.color = (0,0,0)
        self.fire_interval = 1.5
        self.range = 180
        self.type = "Sniper"

class CanonnierTower(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.color = (139,69,19)
        self.fire_interval = 0.5
        self.range = 100
        self.type = "Canonnier"