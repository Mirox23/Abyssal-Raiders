import pygame


class Mob:
    def __init__(self, start_position, speed, color):

        self.x = float(start_position[0])
        self.y = float(start_position[1])

        self.speed = speed
        self.color = color

        self.size = 12
        self.health = 4
        self.path_index = 1

    def move(self, delta_time, path): #delta_time = temps écoulé depuis la dernière frame, path = liste de points que le mob doit suivre

        if self.path_index >= len(path):
            return True

        target_x = path[self.path_index][0]
        target_y = path[self.path_index][1]

        distance_x = target_x - self.x
        distance_y = target_y - self.y

        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        movement = self.speed * delta_time

        if distance <= movement:
            self.x = target_x
            self.y = target_y
            self.path_index += 1
            return self.path_index >= len(path)

        if distance > 0:
            self.x += (distance_x / distance) * movement
            self.y += (distance_y / distance) * movement

        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)