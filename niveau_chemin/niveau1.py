"""
Qu'est-ce que le fichier gère :
    Les 4 chemins de la vague du niveau 1 (facile, chemins courts et droits).
Entrée : aucune (constantes)
Résultat : CHEMINS_VAGUES, une liste de 4 chemins (liste de tuples (x, y))
"""

from setting import position_mur, hauteur_ecran

# Chaque chemin est une liste de points (x, y) que les ennemis suivent.
# Le dernier point doit toujours finir à x = position_mur pour atteindre le mur.
CHEMINS_VAGUES = [
    # Vague 1 : chemin simple, peu de virages
    [
        (0, 200),
        (200, 200),
        (200, 350),
        (420, 350),
        (420, 180),
        (position_mur, 180),
    ],
    # Vague 2 : légèrement plus bas
    [
        (0, 260),
        (180, 260),
        (180, 380),
        (400, 380),
        (400, 140),
        (640, 140),
        (position_mur, 140),
    ],
    # Vague 3 : chemin en zigzag doux
    [
        (0, 300),
        (220, 300),
        (220, 160),
        (440, 160),
        (440, 340),
        (660, 340),
        (position_mur, 340),
    ],
    # Vague 4 (boss) : chemin long mais pas trop difficile
    [
        (0, 240),
        (160, 240),
        (160, 400),
        (360, 400),
        (360, 120),
        (580, 120),
        (580, 380),
        (position_mur, 380),
    ],
]