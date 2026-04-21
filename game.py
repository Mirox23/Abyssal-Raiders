import pygame
from setting import *
from chemin import CHEMIN, draw_decor, draw_path
from mob import Mob, MobRapide, MobTank, MobKamikaze, MobSoigneur
from tower import Tour, TourSniper, TourCanonnier, TourRalentissement, TourSupport
from ui import Bouton, PanneauTelephone, PanneauInfos, PanneauAchevement, EcranFinVague, AffichageXP
from vague import GestionnaireVague
from progression import Progression


class Jeu:
    def __init__(self):
        pygame.init()

        self.fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
        pygame.display.set_caption("Abyssal Raiders")

        self.horloge = pygame.time.Clock()
        self.police_hud = pygame.font.SysFont("consolas", 22)
        self.police_vague = pygame.font.SysFont("consolas", 24, bold=True)

        self.reinitialiser()

    def reinitialiser(self):
        self.liste_ennemis = []
        self.liste_tours = []

        self.points_de_vie_mur = vie_mur_depart
        self.argent = argent_depart

        self.telephone = PanneauTelephone()
        self.panneau_infos = PanneauInfos()
        self.panneau_achevement = PanneauAchevement()
        self.ecran_fin_vague = EcranFinVague()
        self.affichage_xp = AffichageXP()

        self.mode_placement_actif = False
        self.type_tour_a_placer = None
        self.tour_actuellement_selectionnee = None

        self.gestionnaire_vague = GestionnaireVague()
        self.en_attente_lancement_vague = True

        self.progression = Progression()

    def est_sur_chemin(self, position):
        for indice in range(len(CHEMIN) - 1):
            zone = pygame.Rect(
                min(CHEMIN[indice][0], CHEMIN[indice+1][0]) - 30,
                min(CHEMIN[indice][1], CHEMIN[indice+1][1]) - 30,
                abs(CHEMIN[indice][0] - CHEMIN[indice+1][0]) + 60,
                abs(CHEMIN[indice][1] - CHEMIN[indice+1][1]) + 60,
            )
            if zone.collidepoint(position):
                return True
        return False

    def lancer_nouvelle_vague(self):
        self.argent += argent_par_vague
        self.gestionnaire_vague.demarrer_vague(CHEMIN[0])
        self.en_attente_lancement_vague = False
        self.ecran_fin_vague.fermer()

    def lancer(self):
        jeu_en_cours = True

        while jeu_en_cours:
            delta_temps = self.horloge.tick(FPS) / 1000

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
        resultat_fin_vague = self.ecran_fin_vague.gerer_clic(position_clic)
        if resultat_fin_vague == "nouvelle_vague":
            self.lancer_nouvelle_vague()
            return
        if resultat_fin_vague == "modification":
            self.ecran_fin_vague.fermer()
            self.en_attente_lancement_vague = True
            return

        # Panneau achèvement prioritaire si visible (bloque les clics derrière)
        if self.panneau_achevement.gerer_clic(position_clic):
            return

        # Panneau infos/amélioration prioritaire si visible (met au premier plan)
        if self.panneau_infos.visible:
            action, self.argent = self.panneau_infos.gerer_clic(position_clic, self.argent)
            return

        # Téléphone et bouton tourelle
        action_telephone = self.telephone.gerer_clic(position_clic)

        if action_telephone == "Tourelle":
            self.mode_placement_actif = True
            self.type_tour_a_placer = None
            self.tour_actuellement_selectionnee = None
            return

        if action_telephone == "New vague" and self.en_attente_lancement_vague:
            self.lancer_nouvelle_vague()
            return
        
        if action_telephone == "Achèvement":
            self.panneau_achevement.ouvrir()
            return

        # "Info" ouvre les infos de la tour sélectionnée
        if action_telephone == "Info":
            if self.tour_actuellement_selectionnee:
                self.panneau_infos.ouvrir(self.tour_actuellement_selectionnee)
            return

        # Sélection d'une tour existante
        if not self.mode_placement_actif:
            self.tour_actuellement_selectionnee = None
            for tour in self.liste_tours:
                distance = ((position_clic[0] - tour.x)**2 + (position_clic[1] - tour.y)**2) ** 0.5
                if distance <= tour.taille + 4:
                    self.tour_actuellement_selectionnee = tour
                    break

        # Choix du type de tour
        if self.mode_placement_actif and self.type_tour_a_placer is None:
            zone_sniper       = pygame.Rect(330, 180, 180, 44)
            zone_canonnier    = pygame.Rect(330, 230, 180, 44)
            zone_ralentissement = pygame.Rect(330, 280, 180, 44)
            zone_support      = pygame.Rect(330, 330, 180, 44)

            if zone_sniper.collidepoint(position_clic):
                self.type_tour_a_placer = TourSniper
            elif zone_canonnier.collidepoint(position_clic):
                self.type_tour_a_placer = TourCanonnier
            elif zone_ralentissement.collidepoint(position_clic):
                self.type_tour_a_placer = TourRalentissement
            elif zone_support.collidepoint(position_clic):
                self.type_tour_a_placer = TourSupport
            return

        # Placement effectif de la tour
        if self.mode_placement_actif and self.type_tour_a_placer:
            peut_placer = (
                len(self.liste_tours) < nb_tours_max
                and not self.est_sur_chemin(position_clic)
                and position_clic[0] < pos_mur - 10
                and self.argent >= prix_tour
            ) # conditions de placement : pas plus que le nombre max de tours, pas sur le chemin, pas trop proche du mur, et assez d'argent
            if peut_placer:
                nouvelle_tour = self.type_tour_a_placer(position_clic)
                self.liste_tours.append(nouvelle_tour)
                self.argent -= prix_tour

                for tour in self.liste_tours:
                    if tour.type_tour == "Support":
                        tour.appliquer_buff(self.liste_tours)

            self.mode_placement_actif = False
            self.type_tour_a_placer = None


    def mettre_a_jour(self, delta_temps):
        self.progression.mettre_a_jour(delta_temps)

        if not self.en_attente_lancement_vague and not self.ecran_fin_vague.visible:
            self.gestionnaire_vague.mettre_a_jour(delta_temps, self.liste_ennemis, CHEMIN)

            # Les soigneurs soignent leurs alliés
            for ennemi in self.liste_ennemis:
                if isinstance(ennemi, MobSoigneur):
                    ennemi.soigner_alentours(delta_temps, self.liste_ennemis)

            ennemis_survivants = []
            # Mise à jour des ennemis : déplacement, vérification des morts et des arrivées au mur
            for ennemi in self.liste_ennemis:
                if ennemi.vie <= 0:
                    self.argent += ennemi.recompense
                    xp_gagnee = self.progression.xp_pour_kill()
                    self.progression.gagner_xp(xp_gagnee)
                    continue

                a_atteint_le_mur = ennemi.avancer(delta_temps, CHEMIN)

                if a_atteint_le_mur:
                    if isinstance(ennemi, MobKamikaze): # isintance de MobKamikaze inflige des dégâts d'explosion au mur
                        self.points_de_vie_mur -= ennemi.degats_explosion
                    else:
                        self.points_de_vie_mur -= 1
                    continue

                ennemis_survivants.append(ennemi)
            self.liste_ennemis = ennemis_survivants

            if self.gestionnaire_vague.vague_terminee:
                self.gestionnaire_vague.vague_terminee = False
                self.en_attente_lancement_vague = True

                xp_vague = self.progression.xp_pour_vague(self.gestionnaire_vague.numero_vague)
                self.progression.gagner_xp(xp_vague)

                self.ecran_fin_vague.ouvrir(self.gestionnaire_vague.numero_vague, xp_vague)

        for tour in self.liste_tours:
            tour.mettre_a_jour(delta_temps, self.liste_ennemis)

        # Les tours support appliquent leur buff en continu
        for tour in self.liste_tours:
            if tour.type_tour == "Support":
                tour.appliquer_buff(self.liste_tours)

    def dessiner(self):
        self.fenetre.fill(couleur_fond)

        draw_decor(self.fenetre, pygame)
        draw_path(self.fenetre, pygame)

        for tour in self.liste_tours:
            tour.dessiner(self.fenetre)
        for ennemi in self.liste_ennemis:
            ennemi.dessiner(self.fenetre)

        self.fenetre.blit(self.police_hud.render(f"Vie : {self.points_de_vie_mur}", True, couleur_texte), (20, 20))
        self.fenetre.blit(self.police_hud.render(f"Argent : {self.argent} ¤", True, couleur_texte), (20, 48))

        if self.gestionnaire_vague.numero_vague > 0:
            texte_vague = f"— Vague {self.gestionnaire_vague.numero_vague} —"
        else:
            texte_vague = "— Prêt —"
        surface_vague = self.police_vague.render(texte_vague, True, (200, 180, 80))
        self.fenetre.blit(surface_vague, (largeur_ecran // 2 - surface_vague.get_width() // 2, 14))

        self.affichage_xp.dessiner(self.fenetre, self.progression)

        if self.tour_actuellement_selectionnee:
            self.dessiner_info_tour()

        if self.mode_placement_actif and self.type_tour_a_placer is None:
            self.dessiner_menu_type_tour()

        self.telephone.dessiner(self.fenetre)
        self.panneau_infos.dessiner(self.fenetre)
        self.panneau_achevement.dessiner(self.fenetre)  
        self.ecran_fin_vague.dessiner(self.fenetre)

    def dessiner_info_tour(self):
        tour = self.tour_actuellement_selectionnee
        police_info = pygame.font.SysFont("consolas", 14) # consolas : police à chasse fixe pour un rendu plus net et lisible, taille 14 pour que ça rentre bien dans l'espace à côté de la tour

        taille_badge = 28
        badge_x = int(tour.x) - taille_badge // 2
        badge_y = int(tour.y) + tour.taille + 6

        pygame.draw.rect(self.fenetre, (255, 190, 0), (badge_x, badge_y, taille_badge, taille_badge), border_radius=4)
        surface_a = police_info.render("A", True, (0, 0, 0)) # A pour "Améliorer", indique que le clic sur ce badge permet d'améliorer la tour 
        self.fenetre.blit(surface_a, (
            badge_x + taille_badge // 2 - surface_a.get_width() // 2,
            badge_y + taille_badge // 2 - surface_a.get_height() // 2
        ))

        info_x = int(tour.x) + tour.taille + 8
        info_y = int(tour.y) - 20
        # Affichage du type de tour, niveau et portée
        for ligne in [tour.type_tour, f"Niv {tour.niveau}", f"Portée {int(tour.portee)}"]: 
            surface_ligne = police_info.render(ligne, True, (230, 230, 230))
            self.fenetre.blit(surface_ligne, (info_x, info_y))
            info_y += 16
   
    # Permet de couper un texte en plusieurs lignes pour qu'il rentre dans une largeur donnée
    def couper_texte(self, texte, police, largeur_max): 
        mots = texte.split(" ")
        lignes = []
        ligne = ""

        for mot in mots:
            test = ligne + (" " if ligne else "") + mot
            if police.size(test)[0] <= largeur_max:
                ligne = test
            else:
                lignes.append(ligne)
                ligne = mot

        if ligne:
            lignes.append(ligne)

        return lignes
    
    def dessiner_menu_type_tour(self):
        police_menu = pygame.font.SysFont("consolas", 18)
        police_desc = pygame.font.SysFont("consolas", 12)
        # Petite police pour le signe d'achat
        police_achat = pygame.font.SysFont("consolas", 11, bold=True)

        donnees_menu = [
            (pygame.Rect(330, 180, 180, 44), (15, 15, 15),   (80, 80, 80),   "Sniper",          (255, 255, 255),   "Longue portée, dégâts x3",   100),
            (pygame.Rect(330, 230, 180, 44), (110, 55, 10),  (160, 100, 40), "Canonnier",       (255, 220, 180),   "Courte portée, très rapide",  80),
            (pygame.Rect(330, 280, 180, 44), (20, 100, 160), (40, 150, 210), "Ralentissement",  (180, 230, 255),   "Ralentit les ennemis",        90),
            (pygame.Rect(330, 330, 180, 44), (140, 120, 10), (200, 180, 30), "Support",         (255, 240, 150),   "Booste les tours proches",    70),
        ]

        rect_fond_menu = pygame.Rect(320, 170, 360, 215)
        pygame.draw.rect(self.fenetre, (20, 22, 35), rect_fond_menu, border_radius=10)
        pygame.draw.rect(self.fenetre, (70, 75, 110), rect_fond_menu, width=1, border_radius=10)

        police_titre_menu = pygame.font.SysFont("consolas", 14)
        surface_titre_menu = police_titre_menu.render("Choisir une tour :", True, (160, 160, 200))
        self.fenetre.blit(surface_titre_menu, (rect_fond_menu.x + 10, rect_fond_menu.y + 6))

        for (zone, couleur_fond, couleur_bord, nom, couleur_texte_nom, description, prix) in donnees_menu:
            pygame.draw.rect(self.fenetre, couleur_fond, zone, border_radius=6)
            pygame.draw.rect(self.fenetre, couleur_bord, zone, width=1, border_radius=6)

            # Nom de la tour
            surface_nom = police_menu.render(nom, True, couleur_texte_nom)
            self.fenetre.blit(surface_nom, (zone.x + 8, zone.y + 4))

            # Prix affiché
            surface_prix = police_desc.render(f"{prix} ¤", True, (255, 215, 0))
            self.fenetre.blit(surface_prix, (zone.right - 60, zone.y + 4))

            # Description coupée en plusieurs lignes si besoin
            lignes = self.couper_texte(description, police_desc, zone.width - 16)
            y_offset = 24
            for ligne in lignes:
                surface_desc = police_desc.render(ligne, True, (180, 180, 180))
                self.fenetre.blit(surface_desc, (zone.x + 8, zone.y + y_offset))
                y_offset += 14

            # AJOUT d'un petit signe d'achat en bas à droite du rectangle
            # Un petit "[ Acheter ]" pour indiquer que c'est cliquable
            signe_largeur = 62
            signe_hauteur = 14
            signe_x = zone.right - signe_largeur - 2
            signe_y = zone.bottom - signe_hauteur - 2

            # Fond du signe
            pygame.draw.rect(
                self.fenetre, (0, 100, 40),
                (signe_x, signe_y, signe_largeur, signe_hauteur),
                border_radius=3
            )
            # Texte du signe
            surface_achat = police_achat.render("+ Acheter", True, (180, 255, 180))
            self.fenetre.blit(surface_achat, (
                signe_x + (signe_largeur - surface_achat.get_width()) // 2,
                signe_y + (signe_hauteur - surface_achat.get_height()) // 2
            ))