"""
A quoi sert le fichier : Ce fichier contient toutes les constantes et paramètres de configuration du jeu. Il définit les dimensions de l'écran, les couleurs, les caractéristiques des ennemis, des tours, des projectiles, ainsi que les paramètres économiques (argent, coûts, etc.) et les valeurs d'expérience. C'est le fichier central de configuration pour tout le projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu. --> Ce fichier contient les constantes de configuration du jeu,
telles que les dimensions de l'écran, les couleurs, les paramètres de jeu (comme la vitesse des ennemis, les coûts des tours, etc.) et d'autres valeurs utilisées dans le projet.
"""

# Taille de la fenêtre et paramètres d'affichage
largeur_ecran = 1000  # Largeur de l'écran en pixels
hauteur_ecran = 560  # Hauteur de l'écran en pixels
FPS = 60  # Images par seconde

# Le mur que les ennemis veulent atteindre (objectif du jeu)
position_mur = largeur_ecran - 70  # Position X où le mur commence
pos_mur = position_mur  # Alias court utilisé dans placer_tour
largeur_mur = 40  # Largeur du mur
vie_mur_depart = 20  # Points de vie du mur au début

# Paramètres de spawning des vagues d'ennemis
intervalle_spawn = 0.8  # Temps entre chaque spawn de mob (en secondes)
vitesse_ennemi = 110.0  # Vitesse de base des ennemis
total_ennemis = 20  # Nombre maximum d'ennemis par vague (plafond)

# Caractéristiques des tours de base
cadence_tour = 0.7  # Temps entre chaque tir (en secondes)
intervalle_tir = cadence_tour  # Alias pour la cadence de tir
portee_tour = 180  # Portée de tir des tours de base

# Paramètres d'amélioration des tours
cout_amelioration = 8  # Coût en argent pour améliorer une tour
bonus_portee = 25  # Bonus de portée par amélioration
bonus_cadence = 0.08  # Bonus de cadence (réduction du temps) par amélioration
niveau_max = 5  # Niveau maximum d'amélioration des tours

# Économie du joueur et paramètres monétaires
argent_depart = 20  # Argent au début de la partie
argent_par_kill = 2  # Argent gagné par ennemi tué
argent_par_vague = 15  # Argent bonus à la fin de chaque vague
prix_tour = 10  # Coût d'une tour de base
nb_tours_max = 10  # Nombre maximum de tours qu'on peut placer

# Caractéristiques des projectiles
vitesse_projectile = 400  # Vitesse de déplacement des projectiles
taille_projectile = 4  # Taille des projectiles pour les collisions

# Système d'expérience et de progression du joueur
xp_par_kill = 1  # XP gagné par ennemi tué
xp_par_vague_base = 10  # XP de base gagné à la fin d'une vague
niveau_joueur_depart = 1  # Niveau du joueur au début de la partie
xp_pour_niveau_suivant_base = 20  # XP nécessaire pour le premier niveau supérieur

# Couleurs principales utilisées dans le jeu
couleur_fond = (22, 36, 28)  # Couleur du fond de l'écran
couleur_mur = (95, 97, 120)  # Couleur du mur de défense
couleur_texte = (240, 240, 240)  # Couleur du texte
couleur_ennemis = (190, 55, 55)  # Couleur des ennemis
couleur_ennemies = couleur_ennemis  # Alias pour la couleur des ennemis
couleur_tour = (200, 205, 218)  # Couleur des tours

# Couleurs des boutons de l'interface
couleur_bouton = (70, 110, 145)  # Couleur normale des boutons
couleur_bouton_survol = (95, 140, 182)  # Couleur des boutons au survol de la souris

# Couleurs pour les éléments de décor
couleur_rocher = (88, 100, 86)  # Couleur des rochers/décorations
couleur_herbe = (58, 94, 60)  # Couleur de l'herbe/décorations

# Alias utilisés dans d'autres fichiers pour compatibilité
screen_height = hauteur_ecran  # Alias pour la hauteur de l'écran
wall_x = position_mur  # Alias pour la position du mur
couleur_decor_rock = couleur_rocher  # Alias pour la couleur des rochers
couleur_decor_grass = couleur_herbe  # Alias pour la couleur de l'herbe
couleur_wall = couleur_mur  # Alias pour la couleur du mur
