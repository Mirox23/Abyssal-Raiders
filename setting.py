"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie setting du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu. --> Ce fichier contient les constantes de configuration du jeu,
telles que les dimensions de l'écran, les couleurs, les paramètres de jeu (comme la vitesse des ennemis, les coûts des tours, etc.) et d'autres valeurs utilisées dans le projet.
"""

# Taille de la fenêtre
largeur_ecran = 1000
hauteur_ecran = 560
FPS = 60

# Le mur que les ennemis veulent atteindre
position_mur = largeur_ecran - 70   # x à partir duquel le mur commence
pos_mur = position_mur              # alias court utilisé dans placer_tour
largeur_mur = 40
vie_mur_depart = 20

# Spawning des vaguess
intervalle_spawn = 0.8
vitesse_ennemi = 110.0
total_ennemis = 20

# Tours de base
cadence_tour = 0.7
intervalle_tir = cadence_tour
portee_tour = 180

# Amélioration des tours
cout_amelioration = 8
bonus_portee = 25
bonus_cadence = 0.08
niveau_max = 5

# Économie du joueur
argent_depart = 20
argent_par_kill = 2
argent_par_vague = 15
prix_tour = 10
nb_tours_max = 10

# Projectiles
vitesse_projectile = 400
taille_projectile = 4

# Expérience et niveau joueur
xp_par_kill = 1
xp_par_vague_base = 10
niveau_joueur_depart = 1
xp_pour_niveau_suivant_base = 20

# Couleurs principales
couleur_fond = (22, 36, 28)
couleur_mur = (95, 97, 120)
couleur_texte = (240, 240, 240)
couleur_ennemis = (190, 55, 55)
couleur_ennemies = couleur_ennemis
couleur_tour = (200, 205, 218)

# Couleurs des boutons
couleur_bouton = (70, 110, 145)
couleur_bouton_survol = (95, 140, 182)

# Décor
couleur_rocher = (88, 100, 86)
couleur_herbe = (58, 94, 60)

# Alias utilisés dans d'autres fichiers
screen_height = hauteur_ecran
wall_x = position_mur
couleur_decor_rock = couleur_rocher
couleur_decor_grass = couleur_herbe
couleur_wall = couleur_mur
