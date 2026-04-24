from setting import (
    largeur_ecran, hauteur_ecran,
    position_mur,
    couleur_decor_rock, couleur_decor_grass, couleur_wall,
)

CHEMINS_CONTINENTS = {
    "pirate": [
        (0, 210),
        (180, 210),
        (180, 355),
        (380, 355),
        (380, 130),
        (650, 130),
        (650, 410),
        (840, 410),
        (840, 275),
        (position_mur, 275),
    ],
    "samourai": [
        (0, 120),
        (160, 120),
        (160, 275),
        (330, 275),
        (330, 465),
        (570, 465),
        (570, 225),
        (760, 225),
        (760, 350),
        (position_mur, 350),
    ],
    "medieval": [
        (0, 300),
        (210, 300),
        (210, 180),
        (430, 180),
        (430, 350),
        (640, 350),
        (640, 160),
        (830, 160),
        (830, 300),
        (position_mur, 300),
    ],
    "demoniaque": [
        (0, 250),
        (140, 250),
        (140, 120),
        (320, 120),
        (320, 410),
        (500, 410),
        (500, 220),
        (700, 220),
        (700, 455),
        (position_mur, 455),
    ],
}

CHEMIN = list(CHEMINS_CONTINENTS["pirate"])

liste_decors = [
    {"type": "rock",  "x": 80,  "y": 140, "r": 18},
    {"type": "rock",  "x": 220, "y": 420, "r": 14},
    {"type": "grass", "x": 450, "y": 220, "r": 22},
    {"type": "rock",  "x": 680, "y": 310, "r": 16},
    {"type": "grass", "x": 720, "y": 460, "r": 20},
    {"type": "rock",  "x": 300, "y": 80,  "r": 12},
    {"type": "grass", "x": 500, "y": 470, "r": 18},
    {"type": "rock",  "x": 850, "y": 180, "r": 15},
]


def configurer_chemin_continent(continent):
    """
    Met à jour le chemin actif selon le continent choisi.
    On modifie la liste en place pour garder les références déjà importées.
    """
    chemin_continent = CHEMINS_CONTINENTS.get(continent, CHEMINS_CONTINENTS["pirate"])
    CHEMIN[:] = chemin_continent


def draw_decor(fenetre, pygame):
    for decor in liste_decors:
        if decor["type"] == "rock":
            couleur = couleur_decor_rock
        else:
            couleur = couleur_decor_grass
        pygame.draw.circle(fenetre, couleur, (decor["x"], decor["y"]), decor["r"])


def draw_path(fenetre, pygame):
    if len(CHEMIN) >= 2:
        pygame.draw.lines(fenetre, (60, 80, 60), False, CHEMIN, 28)
        pygame.draw.lines(fenetre, (75, 95, 75), False, CHEMIN, 4)

    rect_mur = pygame.Rect(position_mur, 0, largeur_ecran - position_mur, hauteur_ecran)
    fenetre.fill(couleur_wall, rect_mur)