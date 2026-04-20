import pygame
from setting import *
from chemin import CHEMIN, draw_decor, draw_path
from mob import Mob, MobRapide, MobTank, MobKamikaze, MobSoigneur
from tower import Tour, TourSniper, TourCanonnier, TourRalentissement, TourSupport
from ui import Bouton, PanneauTelephone, PanneauAmelioration, EcranFinVague, AffichageXP
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
        self.panneau_amelioration = PanneauAmelioration()
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

        # Panneau amélioration prioritaire si visible
        if self.panneau_amelioration.visible:
            action, self.argent = self.panneau_amelioration.gerer_clic(position_clic, self.argent)
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

        if action_telephone == "Amelioration":
            if self.tour_actuellement_selectionnee:
                self.panneau_amelioration.ouvrir(self.tour_actuellement_selectionnee)
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
            zone_sniper = pygame.Rect(330, 180, 180, 44)
            zone_canonnier = pygame.Rect(330, 230, 180, 44)
            zone_ralentissement = pygame.Rect(330, 280, 180, 44)
            zone_support = pygame.Rect(330, 330, 180, 44)

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
            )
            if peut_placer:
                nouvelle_tour = self.type_tour_a_placer(position_clic)
                self.liste_tours.append(nouvelle_tour)
                self.argent -= prix_tour

                # Appliquer immédiatement les buffs des tours support existantes
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
            for ennemi in self.liste_ennemis:
                if ennemi.vie <= 0:
                    self.argent += ennemi.recompense
                    xp_gagnee = self.progression.xp_pour_kill()
                    self.progression.gagner_xp(xp_gagnee)
                    continue

                a_atteint_le_mur = ennemi.avancer(delta_temps, CHEMIN)

                if a_atteint_le_mur:
                    if isinstance(ennemi, MobKamikaze):
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

        # HUD vie et argent
        self.fenetre.blit(self.police_hud.render(f"Vie : {self.points_de_vie_mur}", True, couleur_texte), (20, 20))
        self.fenetre.blit(self.police_hud.render(f"Argent : {self.argent} ¤", True, couleur_texte), (20, 48))

        # Numéro de vague centré en haut
        if self.gestionnaire_vague.numero_vague > 0:
            texte_vague = f"— Vague {self.gestionnaire_vague.numero_vague} —"
        else:
            texte_vague = "— Prêt —"
        surface_vague = self.police_vague.render(texte_vague, True, (200, 180, 80))
        self.fenetre.blit(surface_vague, (largeur_ecran // 2 - surface_vague.get_width() // 2, 14))

        # Barre XP
        self.affichage_xp.dessiner(self.fenetre, self.progression)

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

    def dessiner_info_tour(self):
        tour = self.tour_actuellement_selectionnee
        police_info = pygame.font.SysFont("consolas", 14)

        taille_badge = 28
        badge_x = int(tour.x) - taille_badge // 2
        badge_y = int(tour.y) + tour.taille + 6

        pygame.draw.rect(self.fenetre, (255, 190, 0), (badge_x, badge_y, taille_badge, taille_badge), border_radius=4)
        surface_a = police_info.render("A", True, (0, 0, 0))
        self.fenetre.blit(surface_a, (
            badge_x + taille_badge // 2 - surface_a.get_width() // 2,
            badge_y + taille_badge // 2 - surface_a.get_height() // 2
        ))

        info_x = int(tour.x) + tour.taille + 8
        info_y = int(tour.y) - 20
        for ligne in [tour.type_tour, f"Niv {tour.niveau}", f"Portée {int(tour.portee)}"]:
            surface_ligne = police_info.render(ligne, True, (230, 230, 230))
            self.fenetre.blit(surface_ligne, (info_x, info_y))
            info_y += 16

    def dessiner_menu_type_tour(self):
        police_menu = pygame.font.SysFont("consolas", 18)

        donnees_menu = [
            (pygame.Rect(330, 180, 180, 44), (15, 15, 15),    (80, 80, 80),    "Sniper",          (255, 255, 255), "Longue portée, dégâts x3"),
            (pygame.Rect(330, 230, 180, 44), (110, 55, 10),   (160, 100, 40),  "Canonnier",       (255, 220, 180), "Courte portée, très rapide"),
            (pygame.Rect(330, 280, 180, 44), (20, 100, 160),  (40, 150, 210),  "Ralentissement",  (180, 230, 255), "Ralentit les ennemis"),
            (pygame.Rect(330, 330, 180, 44), (140, 120, 10),  (200, 180, 30),  "Support",         (255, 240, 150), "Booste les tours proches"),
        ]

        # Fond général du menu
        rect_fond_menu = pygame.Rect(320, 170, 360, 215)
        pygame.draw.rect(self.fenetre, (20, 22, 35), rect_fond_menu, border_radius=10)
        pygame.draw.rect(self.fenetre, (70, 75, 110), rect_fond_menu, width=1, border_radius=10)

        police_titre_menu = pygame.font.SysFont("consolas", 14)
        surface_titre_menu = police_titre_menu.render("Choisir une tour :", True, (160, 160, 200))
        self.fenetre.blit(surface_titre_menu, (rect_fond_menu.x + 10, rect_fond_menu.y + 6))

        police_desc = pygame.font.SysFont("consolas", 12)

        for (zone, couleur_fond, couleur_bord, nom, couleur_texte_nom, description) in donnees_menu:
            pygame.draw.rect(self.fenetre, couleur_fond, zone, border_radius=6)
            pygame.draw.rect(self.fenetre, couleur_bord, zone, width=1, border_radius=6)

            surface_nom = police_menu.render(nom, True, couleur_texte_nom)
            self.fenetre.blit(surface_nom, (zone.x + 8, zone.y + 4))

            surface_desc = police_desc.render(description, True, (180, 180, 180))
            self.fenetre.blit(surface_desc, (zone.x + 8, zone.y + 24))

        self.fenetre.blit(police_menu.render("Sniper  (longue portée)", True, (255, 255, 255)), (408, 214))
        self.fenetre.blit(police_menu.render("Canonnier  (tir rapide)", True, (255, 220, 180)), (408, 274))

