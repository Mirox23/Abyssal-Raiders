from setting import (
    couleur_decor_grass,
    couleur_decor_rock,
    screen_height,
    wall_x,
)

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


DECOR_ROCKS = [
    (90, 120, 46, 28),
    (250, 445, 58, 36),
    (430, 90, 70, 42),
    (645, 470, 64, 36),
    (860, 155, 52, 30),
]

DECOR_GRASS = [
    (180, 70, 18),
    (370, 505, 24),
    (560, 120, 20),
    (700, 360, 22),
    (905, 460, 20),
]


def draw_path(screen, pygame_module):
    pygame_module.draw.lines(screen, (146, 119, 86), False, PATH, 44)


def draw_decor(screen, pygame_module):
    for x, y, w, h in DECOR_ROCKS:
        pygame_module.draw.ellipse(screen, couleur_decor_rock, (x, y, w, h))
    for x, y, r in DECOR_GRASS:
        pygame_module.draw.circle(screen, couleur_decor_grass, (x, y), r)
