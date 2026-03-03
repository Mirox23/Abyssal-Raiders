import pygame
from setting import projectile_speed, projectile_size


class Projectile:
    def __init__(self, start_x, start_y, target):

        self.x = start_x
        self.y = start_y
        self.target = target

        self.speed = projectile_speed
        self.size = projectile_size

        self.active = True

    def update(self, delta_time):

        if not self.target or self.target.health <= 0:
            self.active = False
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 5:
            self.target.health -= 1
            self.active = False
            return

        if distance > 0:
            self.x += (dx / distance) * self.speed * delta_time
            self.y += (dy / distance) * self.speed * delta_time

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 220, 50), (int(self.x), int(self.y)), self.size)