from setting import (
largeur_ecran, hauteur_ecran,
position_mur,
couleur_decor_rock, couleur_decor_grass, couleur_wall,
)
# créé par Diego

CHEMINS = [
[ # spawn gauche → centre
(0, 200),
(100, 200),
(100, 350),
(400, 350),
],
[ # spawn droite → centre
(position_mur, 400),
(700, 400),
(700, 200),
(400, 200),
]
]

liste_decors = [
{"type": "rock", "x": 80, "y": 140, "r": 18},
{"type": "rock", "x": 220, "y": 420, "r": 14},
{"type": "grass", "x": 450, "y": 220, "r": 22},
{"type": "rock", "x": 680, "y": 310, "r": 16},
{"type": "grass", "x": 720, "y": 460, "r": 20},
{"type": "rock", "x": 300, "y": 80, "r": 12},
{"type": "grass", "x": 500, "y": 470, "r": 18},
{"type": "rock", "x": 850, "y": 180, "r": 15},
]

def draw_decor(fenetre, pygame):
for decor in liste_decors:
if decor["type"] == "rock":
couleur = couleur_decor_rock
else:
couleur