from setting import (
    largeur_ecran, hauteur_ecran,
    position_mur,
    couleur_decor_rock, couleur_decor_grass, couleur_wall,
)

# Points du chemin suivi par les ennemis
CHEMIN = [
    (0,   200),
    (150, 200),
    (150, 350),
    (350, 350),
    (350, 130),
    (600, 130),
    (600, 400),
    (800, 400),
    (800, 280),
    (position_mur, 280),
]

# Petits éléments de décor
DECORS = [
    {"type": "rock",  "x": 80,  "y": 140, "r": 18},
    {"type": "rock",  "x": 220, "y": 420, "r": 14},
    {"type": "grass", "x": 450, "y": 220, "r": 22},
    {"type": "rock",  "x": 680, "y": 310, "r": 16},
    {"type": "grass", "x": 720, "y": 460, "r": 20},
    {"type": "rock",  "x": 300, "y": 80,  "r": 12},
    {"type": "grass", "x": 500, "y": 470, "r": 18},
    {"type": "rock",  "x": 850, "y": 180, "r": 15},
]


def draw_decor(fenetre, pygame):
    """Dessine les rochers et touffes d'herbe."""
    for d in DECORS:
        couleur = couleur_decor_rock if d["type"] == "rock" else couleur_decor_grass
        pygame.draw.circle(fenetre, couleur, (d["x"], d["y"]), d["r"])


def draw_path(fenetre, pygame):
    """Dessine le chemin et le mur de droite."""
    if len(CHEMIN) >= 2:
        pygame.draw.lines(fenetre, (60, 80, 60), False, CHEMIN, 28)
        pygame.draw.lines(fenetre, (75, 95, 75), False, CHEMIN, 4)

    mur_rect = pygame.Rect(position_mur, 0, largeur_ecran - position_mur, hauteur_ecran)
    fenetre.fill(couleur_wall, mur_rect)