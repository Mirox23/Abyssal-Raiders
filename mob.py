import pygame


class Mob:
    def __init__(self, start_pos, speed, color):

        self.x = float(start_pos[0])
        self.y = float(start_pos[1])
        self.speed = speed
        self.color = color
        self.size = 12
        self.point = 1
        self.health = 4

    def move(self, delta_time, path):

        if self.point >= len(path):
            return True

        target_x, target_y = path[self.point]

        distance_x = target_x - self.x
        distance_y = target_y - self.y

        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        movement = self.speed * delta_time

        if distance <= movement:
            self.x, self.y = target_x, target_y
            self.point += 1
            return self.point >= len(path)

        if distance > 0:
            self.x += (distance_x / distance) * movement
            self.y += (distance_y / distance) * movement

        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)