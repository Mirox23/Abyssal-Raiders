# Toutes les constantes du jeu regroupées ici

# Taille de la fenêtre
largeur_ecran = 1000
hauteur_ecran = 560
FPS = 60

# Le mur que les ennemis veulent atteindre
position_mur = largeur_ecran - 70
pos_mur = position_mur
largeur_mur = 40
vie_mur_depart = 20

# Les vagues d'ennemis
intervalle_spawn = 0.8
vitesse_ennemi = 110.0
total_ennemis = 18

# Les tours
cadence_tour = 0.7
intervalle_tir = cadence_tour
portee_tour = 180

# Amélioration des tours
cout_amelioration = 8
bonus_portee = 25
bonus_cadence = 0.08
niveau_max = 5

# L'argent
argent_depart = 20
argent_par_kill = 2
argent_par_vague = 15
prix_tour = 10
nb_tours_max = 8

# Les projectiles
vitesse_projectile = 400
taille_projectile = 4

# Couleurs principales
couleur_fond = (22, 36, 28)
couleur_mur = (95, 97, 120)
couleur_texte = (240, 240, 240)
couleur_ennemis = (190, 55, 55)
couleur_ennemies = couleur_ennemis
couleur_tour = (200, 205, 218)

# Boutons
couleur_bouton = (70, 110, 145)
couleur_bouton_survol = (95, 140, 182)

# Décor
couleur_rocher = (88, 100, 86)
couleur_herbe = (58, 94, 60)

# Alias pour chemin.py
screen_height = hauteur_ecran
wall_x = position_mur
couleur_decor_rock = couleur_rocher
couleur_decor_grass = couleur_herbe
couleur_wall = couleur_mur
