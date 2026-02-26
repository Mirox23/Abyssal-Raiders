from setting import *

class Tower:
    def __init__(self, pos):
        self.x, self.y = pos
        self.range = tower_range
        self.fire_interval = tower_fire_interval
        self.cooldown = 0
        self.size = 18

    def update(self, dt, enemies):
        self.cooldown -= dt
        if self.cooldown <= 0:
            target = self.get_target(enemies)
            if target:
                target.life -= 1
                self.cooldown = self.fire_interval

    def get_target(self, enemies):
        for enemy in enemies:
            dx = enemy.x - self.x # dx = distance x
            dy = enemy.y - self.y # dy = distance y
            dist = (dx*dx + dy*dy) ** 0.5
            if dist <= self.range:
                return enemy
        return None

    def draw(self, screen, pygame):
        pygame.draw.circle(screen, couleur_tower, (self.x, self.y), self.size) # self.size = rayon de la tourelle
        pygame.draw.circle(screen, (120,120,120), (self.x, self.y), self.range, 1) #self.rang = rayon de la portée, 1 = épaisseur du cercle de portée