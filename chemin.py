from setting import screen_height, wall_x

PATH = [
    (0, screen_height // 2),
    (140, screen_height // 2),
    (140, screen_height // 2 - 90),
    (320, screen_height // 2 - 90),
    (320, screen_height // 2 + 80),
    (520, screen_height // 2 + 80),
    (520, screen_height // 2 - 30),
    (740, screen_height // 2 - 30),
    (740, screen_height // 2 + 100),
    (wall_x, screen_height // 2 + 100),
]

def draw_path(screen, pygame_module):
    pygame_module.draw.lines(screen, (146, 119, 86), False, PATH, 44)
