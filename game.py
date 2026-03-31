import pygame
from setting import *
from chemin import CHEMIN, draw_decor, draw_path
from mob import Mob, MobRapide
from tower import Tour, TourSniper, TourCanonnier
from ui import Bouton, PanneauTelephone, PanneauAmelioration, EcranFinVague
from vague import GestionnaireVague


class Jeu:
    def __init__(self):
        pygame.init()

        self.fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
        pygame.display.set_caption("Abyssal Raiders")

        self.horloge = pygame.time.Clock()
        self.police_hud = pygame.font.SysFont("consolas", 22) #consolas pour un style pixelisé
        self.police_vague = pygame.font.SysFont("consolas", 24, bold=True) 

        self.reinitialiser()

    def reinitialiser(self): #réinitialise les éléments du jeu pour pouvoir recommencer une partie depuis le début sans avoir à relancer le programme
        self.liste_ennemis = []
        self.liste_tours = []

        self.points_de_vie_mur = vie_mur_depart
        self.argent = argent_depart

        self.telephone = PanneauTelephone()
        self.panneau_amelioration = PanneauAmelioration()
        self.ecran_fin_vague = EcranFinVague()

        self.mode_placement_actif = False #indique si le joueur est en train de placer une tour (après avoir cliqué sur le bouton tourelle) pour que les clics soient interprétés comme des placements de tour plutôt que des sélections de tour ou des interactions avec l'UI
        self.type_tour_a_placer = None
        self.tour_actuellement_selectionnee = None

        self.gestionnaire_vague = GestionnaireVague()
        self.en_attente_lancement_vague = True

    def est_sur_chemin(self, position):
        for indice in range(len(CHEMIN) - 1):
            zone = pygame.Rect(
                min(CHEMIN[indice][0], CHEMIN[indice+1][0]) - 30, #on crée une zone rectangulaire autour de chaque segment du chemin pour vérifier si le clic du joueur est à l'intérieur de cette zone. Si c'est le cas, cela signifie que le joueur essaie de placer une tour sur le chemin, ce qui n'est pas autorisé
                min(CHEMIN[indice][1], CHEMIN[indice+1][1]) - 30,
                abs(CHEMIN[indice][0] - CHEMIN[indice+1][0]) + 60,
                abs(CHEMIN[indice][1] - CHEMIN[indice+1][1]) + 60,
            )
            if zone.collidepoint(position):
                return True
        return False

    def lancer_nouvelle_vague(self):
        self.argent += argent_par_vague
        self.gestionnaire_vague.demarrer_vague(CHEMIN[0]) #le point de départ de la vague est le premier point du chemin pour que les ennemis commencent à avancer depuis le début du chemin vers le mur
        self.en_attente_lancement_vague = False
        self.ecran_fin_vague.fermer()

    def lancer(self):
        jeu_en_cours = True

        while jeu_en_cours:
            delta_temps = self.horloge.tick(FPS) / 1000 #calcul du temps écoulé depuis la dernière itération de la boucle principale pour que les animations et les mouvements soient fluides et indépendants du nombre de frames par seconde

            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    jeu_en_cours = False

                if evenement.type == pygame.MOUSEBUTTONDOWN:
                    self.gerer_clic(evenement.pos)

            self.mettre_a_jour(delta_temps)
            self.dessiner()
            pygame.display.flip()

        pygame.quit()

    def gerer_clic(self, position_clic):
        # Écran de fin de vague prioritaire
        resultat_fin_vague = self.ecran_fin_vague.gerer_clic(position_clic) #si le panneau de fin de vague est visible, on gère les clics sur ce panneau en priorité pour que le joueur puisse facilement lancer la nouvelle vague ou fermer le panneau avant d'interagir avec les autres éléments du jeu
        if resultat_fin_vague == "nouvelle_vague":
            self.lancer_nouvelle_vague()
            return
        if resultat_fin_vague == "modification":
            self.ecran_fin_vague.fermer()
            self.en_attente_lancement_vague = True
            return

        # Panneau amélioration prioritaire si visible
        if self.panneau_amelioration.visible:
            action, self.argent = self.panneau_amelioration.gerer_clic(position_clic, self.argent)
            return

        # Téléphone et bouton tourelle
        action_telephone = self.telephone.gerer_clic(position_clic)

        if action_telephone == "Tourelle":
            self.mode_placement_actif = True
            self.type_tour_a_placer = None #le joueur doit choisir le type de tour après avoir cliqué sur le bouton tourelle, donc on réinitialise le type de tour à placer pour que le menu de choix de type de tour s'affiche correctement
            self.tour_actuellement_selectionnee = None
            return

        if action_telephone == "New vague" and self.en_attente_lancement_vague:
            self.lancer_nouvelle_vague()
            return

        if action_telephone == "Amelioration":
            if self.tour_actuellement_selectionnee:
                self.panneau_amelioration.ouvrir(self.tour_actuellement_selectionnee)
            return

        # Sélection d'une tour existante
        if not self.mode_placement_actif: # si le mode de placement n'est pas actif, les clics sont interprétés comme des sélections de tour ou des interactions avec l'UI. Si le mode de placement est actif, les clics sont interprétés comme des placements de tour, donc on ne veut pas que le joueur puisse sélectionner une tour existante ou interagir avec l'UI pendant qu'il choisit où placer une nouvelle tour pour éviter les confusions et les erreurs de placement
            self.tour_actuellement_selectionnee = None
            for tour in self.liste_tours:
                distance = ((position_clic[0] - tour.x)**2 + (position_clic[1] - tour.y)**2) ** 0.5 # calcul de la distance entre le clic du joueur et le centre de chaque tour pour vérifier si le clic est suffisamment proche d'une tour pour être considéré comme une sélection de cette tour. Si la distance est inférieure à la taille de la tour plus une petite marge, on considère que le joueur a sélectionné cette tour
                if distance <= tour.taille + 4:
                    self.tour_actuellement_selectionnee = tour # si le joueur a cliqué sur une tour, on la sélectionne pour afficher ses informations et permettre les améliorations. Si le joueur a cliqué à côté de toutes les tours, aucune tour n'est sélectionnée et les clics suivants seront interprétés comme des placements de tour ou des interactions avec l'UI en fonction du contexte
                    break

        # Choix du type de tour
        if self.mode_placement_actif and self.type_tour_a_placer is None: # si le mode de placement est actif mais que le type de tour à placer n'est pas encore défini, cela signifie que le joueur vient de cliquer sur le bouton tourelle et doit maintenant choisir le type de tour qu'il souhaite placer. Dans ce cas, on vérifie si le clic du joueur correspond à l'une des options de type de tour dans le menu qui s'affiche pour que le joueur puisse choisir entre les différents types de tours disponibles
            zone_sniper = pygame.Rect(400, 200, 160, 50)
            zone_canonnier = pygame.Rect(400, 260, 160, 50)
            if zone_sniper.collidepoint(position_clic): # si le joueur clique sur la zone correspondant au sniper, on définit le type de tour à placer comme étant une tour sniper. Si le joueur clique sur la zone correspondant au canonnier, on définit le type de tour à placer comme étant une tour canonnier. Si le joueur clique en dehors de ces zones, on ne fait rien et le menu de choix de type de tour reste affiché pour que le joueur puisse faire un choix valide
                self.type_tour_a_placer = TourSniper
            elif zone_canonnier.collidepoint(position_clic):
                self.type_tour_a_placer = TourCanonnier
            return

        # Placement effectif de la tour
        if self.mode_placement_actif and self.type_tour_a_placer:
            peut_placer = (
                len(self.liste_tours) < nb_tours_max
                and not self.est_sur_chemin(position_clic)
                and position_clic[0] < pos_mur - 10
                and self.argent >= prix_tour
            ) # vérifie que le nombre de tours placées n'a pas atteint la limite maximale, que le clic du joueur n'est pas sur le chemin des ennemis, que le clic du joueur n'est pas trop proche du mur pour éviter les placements impossibles, et que le joueur a suffisamment d'argent pour placer la tour. Si toutes ces conditions sont remplies, on peut placer la tour à l'emplacement du clic du joueur
            if peut_placer:
                nouvelle_tour = self.type_tour_a_placer(position_clic)
                self.liste_tours.append(nouvelle_tour)
                self.argent -= prix_tour

            self.mode_placement_actif = False
            self.type_tour_a_placer = None

    def mettre_a_jour(self, delta_temps): 
        if not self.en_attente_lancement_vague and not self.ecran_fin_vague.visible: # si on n'est pas en attente de lancement de vague et que le panneau de fin de vague n'est pas visible, cela signifie qu'une vague est en cours et que les ennemis doivent avancer et interagir avec les tours. Dans ce cas, on met à jour la gestion des vagues pour faire avancer les ennemis le long du chemin, gérer les interactions entre les ennemis et le mur, et vérifier si la vague est terminée pour afficher le panneau de fin de vague
            self.gestionnaire_vague.mettre_a_jour(delta_temps, self.liste_ennemis, CHEMIN) 

            ennemis_survivants = []
            for ennemi in self.liste_ennemis: # on parcourt la liste des ennemis pour mettre à jour leur position en fonction du temps écoulé et de leur vitesse, vérifier s'ils ont atteint le mur pour réduire les points de vie du mur, et vérifier s'ils ont été tués par les tours pour les retirer de la liste des ennemis et ajouter de l'argent au joueur en fonction de la récompense de chaque ennemi tué. Les ennemis qui n'ont pas été tués et qui n'ont pas atteint le mur sont ajoutés à une nouvelle liste d'ennemis survivants qui remplacera la liste actuelle des ennemis à la fin de la boucle pour que les ennemis morts ou ayant atteint le mur soient correctement retirés du jeu
                if ennemi.vie <= 0:
                    self.argent += ennemi.recompense
                    continue
                a_atteint_le_mur = ennemi.avancer(delta_temps, CHEMIN)
                if a_atteint_le_mur:
                    self.points_de_vie_mur -= 1
                    continue
                ennemis_survivants.append(ennemi)
            self.liste_ennemis = ennemis_survivants

            if self.gestionnaire_vague.vague_terminee: # si la vague est terminée (tous les ennemis de la vague ont été tués ou ont atteint le mur), on affiche le panneau de fin de vague pour que le joueur puisse voir les résultats de la vague et choisir de lancer la suivante ou de faire des modifications avant de continuer. On réinitialise également l'état de la gestion des vagues pour préparer le lancement de la prochaine vague
                self.gestionnaire_vague.vague_terminee = False
                self.en_attente_lancement_vague = True
                self.ecran_fin_vague.ouvrir(self.gestionnaire_vague.numero_vague)

        for tour in self.liste_tours:
            tour.mettre_a_jour(delta_temps, self.liste_ennemis)

    def dessiner(self):
        self.fenetre.fill(couleur_fond)

        draw_decor(self.fenetre, pygame)
        draw_path(self.fenetre, pygame)

        for tour in self.liste_tours:
            tour.dessiner(self.fenetre)
        for ennemi in self.liste_ennemis:
            ennemi.dessiner(self.fenetre)

        # HUD vie et argent 
        self.fenetre.blit(self.police_hud.render(f"Vie : {self.points_de_vie_mur}", True, couleur_texte), (20, 20)) #   affiche les points de vie du mur en haut à gauche de l'écran pour que le joueur puisse facilement voir l'état de son mur et réagir en conséquence (en plaçant plus de tours, en améliorant les tours existantes, etc.)
        self.fenetre.blit(self.police_hud.render(f"Argent : {self.argent} ¤", True, couleur_texte), (20, 48))

        # Numéro de vague centré en haut
        if self.gestionnaire_vague.numero_vague > 0:
            texte_vague = f"— Vague {self.gestionnaire_vague.numero_vague} —"
        else:
            texte_vague = "— Prêt —"
        surface_vague = self.police_vague.render(texte_vague, True, (200, 180, 80))
        self.fenetre.blit(surface_vague, (largeur_ecran // 2 - surface_vague.get_width() // 2, 14))

        # Tour sélectionnée
        if self.tour_actuellement_selectionnee:
            self.dessiner_info_tour()

        # Menu choix type de tour
        if self.mode_placement_actif and self.type_tour_a_placer is None:
            self.dessiner_menu_type_tour()

        # UI
        self.telephone.dessiner(self.fenetre)
        self.panneau_amelioration.dessiner(self.fenetre)
        self.ecran_fin_vague.dessiner(self.fenetre)

    def dessiner_info_tour(self): # affiche les informations de la tour actuellement sélectionnée (type, niveau, portée, cadence de tir, coût d'amélioration) à côté de la tour pour que le joueur puisse facilement voir les caractéristiques de chaque tour et prendre des décisions éclairées sur les améliorations à effectuer ou les types de tours à placer en fonction des besoins de défense contre les vagues d'ennemis
        tour = self.tour_actuellement_selectionnee
        police_info = pygame.font.SysFont("consolas", 14) #consolas pour un style pixelisé

        taille_badge = 28
        badge_x = int(tour.x) - taille_badge // 2
        badge_y = int(tour.y) + tour.taille + 6 # le badge d'information de la tour est placé juste en dessous de la tour pour que le joueur puisse facilement associer les informations affichées avec la tour correspondante. La position du badge est calculée en fonction de la position de la tour et de sa taille pour que le badge soit centré horizontalement par rapport à la tour et légèrement espacé verticalement pour une meilleure lisibilité

        pygame.draw.rect(self.fenetre, (255, 190, 0), (badge_x, badge_y, taille_badge, taille_badge), border_radius=4)
        surface_a = police_info.render("A", True, (0, 0, 0))
        self.fenetre.blit(surface_a, (
            badge_x + taille_badge // 2 - surface_a.get_width() // 2,
            badge_y + taille_badge // 2 - surface_a.get_height() // 2
        )) # affiche un badge avec la lettre "A" en dessous de la tour sélectionnée pour indiquer au joueur que les informations affichées à côté de ce badge correspondent à la tour sélectionnée et que le joueur peut cliquer sur ce badge pour accéder au panneau d'amélioration de cette tour. Le badge est conçu pour être facilement identifiable et associé à la tour correspondante pour améliorer l'expérience utilisateur et la clarté des interactions avec le jeu

        info_x = int(tour.x) + tour.taille + 8
        info_y = int(tour.y) - 20
        for ligne in [tour.type_tour, f"Niv {tour.niveau}", f"Portée {int(tour.portee)}"]:
            surface_ligne = police_info.render(ligne, True, (230, 230, 230))
            self.fenetre.blit(surface_ligne, (info_x, info_y))
            info_y += 16

    def dessiner_menu_type_tour(self):
        police_menu = pygame.font.SysFont("consolas", 20) #consolas pour un style pixelisé
        zone_sniper = pygame.Rect(400, 200, 160, 50)
        zone_canonnier = pygame.Rect(400, 260, 160, 50)

        pygame.draw.rect(self.fenetre, (15, 15, 15), zone_sniper, border_radius=6) # dessine les rectangles de fond pour les options de type de tour dans le menu de placement de tour pour que les options soient clairement délimitées et facilement identifiables par le joueur. Les rectangles ont des couleurs différentes pour différencier visuellement les types de tours proposés et attirer l'attention du joueur sur ces options lors du choix du type de tour à placer
        pygame.draw.rect(self.fenetre, (110, 55, 10), zone_canonnier, border_radius=6)
        pygame.draw.rect(self.fenetre, (80, 80, 80), zone_sniper, width=1, border_radius=6)
        pygame.draw.rect(self.fenetre, (160, 100, 40), zone_canonnier, width=1, border_radius=6)

        self.fenetre.blit(police_menu.render("Sniper  (longue portée)", True, (255, 255, 255)), (408, 214))
        self.fenetre.blit(police_menu.render("Canonnier  (tir rapide)", True, (255, 220, 180)), (408, 274))


# aaaa
