from setting import SCREEN_WIDTH, SCREEN_HEIGHT

# obejctif : Chemin exact suivi par les mobs
# Spawn au milieu de la hauteur à gauche
PATH = [
    (0, SCREEN_HEIGHT//2),  # début spawn gauche
    (150, SCREEN_HEIGHT//2),
    (150, SCREEN_HEIGHT//2 + 100),
    (150, SCREEN_HEIGHT//2 + 200),
    (300, SCREEN_HEIGHT//2 + 200),
    (300, SCREEN_HEIGHT//2 + 100),
    (300, SCREEN_HEIGHT//2),
    (450, SCREEN_HEIGHT//2),
    (450, SCREEN_HEIGHT//2 + 100),
    (600, SCREEN_HEIGHT//2 + 100),
    (600, SCREEN_HEIGHT//2 + 200),
    (750, SCREEN_HEIGHT//2 + 200),
    (750, SCREEN_HEIGHT//2 + 150)  # fin proche de la muraille
]
