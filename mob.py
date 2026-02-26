class Mob:
    def __init__(self, start_pos, speed, color):
        self.x = float(start_pos[0])
        self.y = float(start_pos[1])
        self.speed = speed
        self.color = color
        self.size = 12
        self.target_index = 1
        self.health = 4

    def move(self, delta_time, path): # delta_time = temps écoulé depuis la dernière mise à jour, path = liste de points du chemin
        if self.target_index >= len(path):
            return True

        target_x, target_y = path[self.target_index]

        distance_x = target_x - self.x
        distance_y = target_y - self.y

        distance = (distance_x * distance_x + distance_y * distance_y) ** 0.5

        move_distance = self.speed * delta_time

        if distance <= move_distance:
            self.x = target_x
            self.y = target_y
            self.target_index += 1
            return self.target_index >= len(path)

        if distance > 0:
            self.x += (distance_x / distance) * move_distance
            self.y += (distance_y / distance) * move_distance

        return False

    def draw(self, screen, pygame):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)