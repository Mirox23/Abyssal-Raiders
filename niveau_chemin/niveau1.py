from setting import position_mur

# Niveau 1 : 4 vagues = 4 chemins simples
CHEMINS_VAGUES = [
    [(0, 220), (position_mur, 220)],
    [(0, 170), (250, 170), (250, 290), (position_mur, 290)],
    [(0, 300), (180, 300), (180, 130), (520, 130), (520, 300), (position_mur, 300)],
    [(0, 130), (340, 130), (340, 390), (700, 390), (700, 210), (position_mur, 210)],
]