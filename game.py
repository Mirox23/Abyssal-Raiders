import pygame
from setting import *
from chemin import CHEMIN, draw_decor, draw_path
from mob import Mob, MobRapide, MobTank, MobKamikaze, MobSoigneur
from tower import Tour, TourSniper, TourCanonnier, TourRalentissement, TourSupport
from ui import Bouton, PanneauTelephone, PanneauInfos, PanneauAchevement, EcranFinVague, AffichageXP, FenetreRecompensesTalents, PanneauCompetences, PanneauObjets
from vague import GestionnaireVague
from progression import Progression
from competence import GestionnaireCompetences


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
        self.fenetre_recompenses = FenetreRecompensesTalents()
        self.panneau_competences = PanneauCompetences()
        self.panneau_objets = PanneauObjets()

        self.mode_placement_actif = False
        self.type_tour_a_placer = None
        self.tour_actuellement_selectionnee = None

        self.gestionnaire_vague = GestionnaireVague()
        self.en_attente_lancement_vague = True

        self.progression = Progression()
        self.gestionnaire_competences = GestionnaireCompetences()
        self.journal_effets = []
        self.mode_fete = False
        self.sequence_easter_egg = []
        self.talents_appliques = {"degats_competence": 0, "reduction_cout": 0, "prime_or": 0, "resistance_mur": 0}
        self.inventaire_objets = {"potion_mur": 2, "bourse_or": 2, "totem_froid": 1}
        self.bouton_recompense = pygame.Rect(largeur_ecran - 200, 46, 170, 30)
        self.couts_tours = {TourSniper: 14, TourCanonnier: 10, TourRalentissement: 12, TourSupport: 11}

    def ajouter_effet(self, position, couleur, rayon_depart=8, rayon_fin=50, duree=0.35):
        self.journal_effets.append({
            "x": position[0],
            "y": position[1],
            "couleur": couleur,
            "rayon_depart": rayon_depart,
            "rayon_fin": rayon_fin,
            "duree": duree,
            "temps": 0.0,
        })

    def mettre_a_jour_effets(self, delta_temps):
        effets_restants = []
        for effet in self.journal_effets:
            effet["temps"] += delta_temps
            if effet["temps"] < effet["duree"]:
                effets_restants.append(effet)
        self.journal_effets = effets_restants

    def dessiner_effets(self):
        for effet in self.journal_effets:
            progression = effet["temps"] / effet["duree"]
            rayon = int(effet["rayon_depart"] + (effet["rayon_fin"] - effet["rayon_depart"]) * progression)
            alpha = max(0, int(180 * (1 - progression)))

            surface = pygame.Surface((rayon * 2 + 6, rayon * 2 + 6), pygame.SRCALPHA)
            pygame.draw.circle(
                surface,
                (effet["couleur"][0], effet["couleur"][1], effet["couleur"][2], alpha),
                (rayon + 3, rayon + 3),
                rayon,
                3
            )
            self.fenetre.blit(surface, (effet["x"] - rayon - 3, effet["y"] - rayon - 3))

    def gerer_competence(self, touche):
        cle_competence = self.gestionnaire_competences.obtenir_competence_par_touche(touche)
        if not cle_competence:
            return

        donnees = self.gestionnaire_competences.competences[cle_competence]
        cout_reel = max(1, donnees["cout"] - self.talents_appliques["reduction_cout"])
        if not (donnees["cooldown"] <= 0 and self.argent >= cout_reel):
            return

        if cle_competence == "tir_puissant":
            if not self.liste_ennemis:
                return
            cible = max(self.liste_ennemis, key=lambda ennemi: ennemi.etape)
            cible.vie -= 8 + self.talents_appliques["degats_competence"]
            self.ajouter_effet((cible.x, cible.y), (255, 220, 80), rayon_depart=12, rayon_fin=65, duree=0.28)

        elif cle_competence == "pluie_bombes":
            if not self.liste_ennemis:
                return
            position_souris = pygame.mouse.get_pos()
            rayon_explosion = 95
            for ennemi in self.liste_ennemis:
                distance = ((ennemi.x - position_souris[0]) ** 2 + (ennemi.y - position_souris[1]) ** 2) ** 0.5
                if distance <= rayon_explosion:
                    ennemi.vie -= 4 + self.talents_appliques["degats_competence"]
            self.ajouter_effet(position_souris, (255, 120, 60), rayon_depart=18, rayon_fin=120, duree=0.45)

        elif cle_competence == "buff_tours":
            self.ajouter_effet((largeur_ecran // 2, hauteur_ecran // 2), (255, 220, 80), rayon_depart=35, rayon_fin=220, duree=0.6)

        elif cle_competence == "ralentissement_zone":
            position_souris = pygame.mouse.get_pos()
            for ennemi in self.liste_ennemis:
                distance = ((ennemi.x - position_souris[0]) ** 2 + (ennemi.y - position_souris[1]) ** 2) ** 0.5
                if distance <= 130:
                    ennemi.appliquer_ralentissement(0.35, 2.8)
            self.ajouter_effet(position_souris, (120, 200, 255), rayon_depart=16, rayon_fin=145, duree=0.55)

        self.argent -= cout_reel
        self.gestionnaire_competences.activer(cle_competence)

    def gerer_easter_eggs(self, touche):
        "Easter egg pour gagner de l'argent : en appuyant sur P, le joueur reçoit 25¤ et une animation dorée apparaît à côté du montant d'argent"
        if touche == pygame.K_p:
            self.argent += 25
            self.ajouter_effet((120, 70), (255, 215, 0), rayon_depart=10, rayon_fin=70, duree=0.6)

        self.sequence_easter_egg.append(touche)
        self.sequence_easter_egg = self.sequence_easter_egg[-6:]
        code_fete = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        if self.sequence_easter_egg == code_fete:
            self.mode_fete = not self.mode_fete
            couleur = (255, 120, 220) if self.mode_fete else (150, 150, 150)
            self.ajouter_effet((largeur_ecran // 2, 100), couleur, rayon_depart=20, rayon_fin=260, duree=0.8)

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
                if evenement.type == pygame.KEYDOWN:
                    self.gerer_competence(evenement.key)
                    self.gerer_easter_eggs(evenement.key)

            self.mettre_a_jour(delta_temps)
            self.dessiner()
            pygame.display.flip()

        pygame.quit()

    def gerer_clic(self, position_clic):
        if self.bouton_recompense.collidepoint(position_clic):
            self.fenetre_recompenses.ouvrir()
            return

        action_recompense = self.fenetre_recompenses.gerer_clic(position_clic, self.progression)
        if action_recompense:
            type_action, valeur = action_recompense
            if type_action == "recompense":
                self.argent += valeur
                self.ajouter_effet((self.bouton_recompense.centerx, self.bouton_recompense.centery), (255, 220, 80), 8, 55, 0.4)
            elif type_action == "talent":
                self.talents_appliques[valeur] = self.fenetre_recompenses.talents[valeur]["niveau"]
            return

        action_competence = self.panneau_competences.gerer_clic(position_clic)
        if action_competence:
            if action_competence != "consomme":
                touche = self.gestionnaire_competences.competences[action_competence]["touche"]
                self.gerer_competence(touche)
            return

        action_objet = self.panneau_objets.gerer_clic(position_clic)
        if action_objet:
            if action_objet != "consomme":
                self.utiliser_objet(action_objet)
            return

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
        if action_telephone == "Competence":
            self.panneau_competences.ouvrir()
            return
        if action_telephone == "Objets":
            self.panneau_objets.ouvrir()
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
            zone_sniper = pygame.Rect(330, 180, 340, 56)
            zone_canonnier = pygame.Rect(330, 243, 340, 56)
            zone_ralentissement = pygame.Rect(330, 306, 340, 56)
            zone_support = pygame.Rect(330, 369, 340, 56)

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
            cout_tour = self.couts_tours.get(self.type_tour_a_placer, prix_tour)
            peut_placer = (
                len(self.liste_tours) < nb_tours_max
                and not self.est_sur_chemin(position_clic)
                and position_clic[0] < pos_mur - 10
                and position_clic[1] > 80
                and self.argent >= cout_tour
            ) # conditions de placement : pas plus que le nombre max de tours, pas sur le chemin, pas trop proche du mur, et assez d'argent
            if peut_placer:
                nouvelle_tour = self.type_tour_a_placer(position_clic)
                self.liste_tours.append(nouvelle_tour)
                self.argent -= cout_tour

                for tour in self.liste_tours:
                    if tour.type_tour == "Support":
                        tour.appliquer_buff(self.liste_tours)

            self.mode_placement_actif = False
            self.type_tour_a_placer = None


    def mettre_a_jour(self, delta_temps):
        self.progression.mettre_a_jour(delta_temps)
        self.gestionnaire_competences.mettre_a_jour(delta_temps)
        self.mettre_a_jour_effets(delta_temps)

        multiplicateur_buff = 1.0
        if self.gestionnaire_competences.buff_actif():
            multiplicateur_buff = self.gestionnaire_competences.competences["buff_tours"]["multiplicateur_cadence"]

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
                    self.argent += ennemi.recompense + self.talents_appliques["prime_or"]
                    xp_gagnee = self.progression.xp_pour_kill()
                    self.progression.gagner_xp(xp_gagnee)
                    self.ajouter_effet((ennemi.x, ennemi.y), (255, 80, 80), rayon_depart=8, rayon_fin=30, duree=0.25)
                    continue

                a_atteint_le_mur = ennemi.avancer(delta_temps, CHEMIN)

                if a_atteint_le_mur:
                    if isinstance(ennemi, MobKamikaze): # isintance de MobKamikaze inflige des dégâts d'explosion au mur
                        self.points_de_vie_mur -= max(1, ennemi.degats_explosion - self.talents_appliques["resistance_mur"])
                        self.ajouter_effet((pos_mur, hauteur_ecran // 2), (255, 120, 60), rayon_depart=12, rayon_fin=80, duree=0.35)
                    else:
                        self.points_de_vie_mur -= max(1, 1 - self.talents_appliques["resistance_mur"])
                        self.ajouter_effet((pos_mur, hauteur_ecran // 2), (230, 80, 80), rayon_depart=8, rayon_fin=55, duree=0.25)
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
            cadence_originale = tour.cadence
            tour.cadence = max(0.08, tour.cadence * multiplicateur_buff)
            tour.mettre_a_jour(delta_temps, self.liste_ennemis)
            tour.cadence = cadence_originale

        # Les tours support appliquent leur buff en continu
        for tour in self.liste_tours:
            if tour.type_tour == "Support":
                tour.appliquer_buff(self.liste_tours)

    def dessiner(self):
        if self.mode_fete:
            temps = pygame.time.get_ticks() * 0.002
            fond = (
                int(45 + 30 * (1 + pygame.math.Vector2(1, 0).rotate(temps * 40).x)),
                int(35 + 30 * (1 + pygame.math.Vector2(1, 0).rotate(temps * 65).y)),
                int(55 + 20 * (1 + pygame.math.Vector2(1, 0).rotate(temps * 90).x)),
            )
            self.fenetre.fill(fond)
        else:
            self.fenetre.fill(couleur_fond)

        draw_decor(self.fenetre, pygame)
        draw_path(self.fenetre, pygame)

        for tour in self.liste_tours:
            tour.dessiner(self.fenetre)
        for ennemi in self.liste_ennemis:
            ennemi.dessiner(self.fenetre)
        self.dessiner_effets()

        self.fenetre.blit(self.police_hud.render(f"Vie : {self.points_de_vie_mur}", True, couleur_texte), (20, 20))
        self.fenetre.blit(self.police_hud.render(f"Argent : {self.argent} ¤", True, couleur_texte), (20, 48))

        if self.gestionnaire_vague.numero_vague > 0:
            texte_vague = f"— Vague {self.gestionnaire_vague.numero_vague} —"
        else:
            texte_vague = "— Prêt —"
        surface_vague = self.police_vague.render(texte_vague, True, (200, 180, 80))
        self.fenetre.blit(surface_vague, (largeur_ecran // 2 - surface_vague.get_width() // 2, 14))

        self.affichage_xp.dessiner(self.fenetre, self.progression)
        self.dessiner_bouton_recompense()

        if self.tour_actuellement_selectionnee:
            self.dessiner_info_tour()

        if self.mode_placement_actif and self.type_tour_a_placer is None:
            self.dessiner_menu_type_tour()

        self.telephone.dessiner(self.fenetre)
        self.panneau_infos.dessiner(self.fenetre)
        self.panneau_achevement.dessiner(self.fenetre)  
        self.ecran_fin_vague.dessiner(self.fenetre)
        self.panneau_competences.dessiner(self.fenetre, self.gestionnaire_competences, self.argent)
        self.panneau_objets.dessiner(self.fenetre, self.inventaire_objets)
        self.fenetre_recompenses.dessiner(self.fenetre, self.progression)

    def dessiner_bouton_recompense(self):
        survol = self.bouton_recompense.collidepoint(pygame.mouse.get_pos())
        couleur = (70, 130, 70) if survol else (45, 95, 52)
        pygame.draw.rect(self.fenetre, couleur, self.bouton_recompense, border_radius=7)
        pygame.draw.rect(self.fenetre, (150, 220, 150), self.bouton_recompense, width=1, border_radius=7)
        texte = pygame.font.SysFont("consolas", 14, bold=True).render("Recompense", True, (235, 255, 235))
        self.fenetre.blit(texte, (self.bouton_recompense.centerx - texte.get_width() // 2, self.bouton_recompense.y + 7))

    def utiliser_objet(self, cle_objet):
        if self.inventaire_objets.get(cle_objet, 0) <= 0:
            return
        self.inventaire_objets[cle_objet] -= 1
        if cle_objet == "potion_mur":
            self.points_de_vie_mur = min(vie_mur_depart + 10, self.points_de_vie_mur + 2)
            self.ajouter_effet((90, 30), (80, 255, 120), 8, 45, 0.45)
        elif cle_objet == "bourse_or":
            self.argent += 6
            self.ajouter_effet((120, 62), (255, 230, 120), 8, 55, 0.45)
        elif cle_objet == "totem_froid":
            for ennemi in self.liste_ennemis:
                ennemi.appliquer_ralentissement(0.45, 1.2)
            self.ajouter_effet((largeur_ecran // 2, hauteur_ecran // 2), (130, 210, 255), 20, 260, 0.55)

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
        police_desc = pygame.font.SysFont("consolas", 11)

        donnees_menu = [
            (pygame.Rect(330, 180, 340, 56), (15, 15, 15),   (80, 80, 80),   "Sniper",         (255, 255, 255), "Longue portee, degats x3", self.couts_tours[TourSniper]),
            (pygame.Rect(330, 243, 340, 56), (110, 55, 10),  (160, 100, 40), "Canonnier",      (255, 220, 180), "Courte portee, cadence elevee", self.couts_tours[TourCanonnier]),
            (pygame.Rect(330, 306, 340, 56), (20, 100, 160), (40, 150, 210), "Ralentissement", (180, 230, 255), "Ralenti les groupes ennemis", self.couts_tours[TourRalentissement]),
            (pygame.Rect(330, 369, 340, 56), (140, 120, 10), (200, 180, 30), "Support",        (255, 240, 150), "Boost cadence tours proches", self.couts_tours[TourSupport]),
        ]

        rect_fond_menu = pygame.Rect(320, 170, 360, 265)
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
            self.fenetre.blit(surface_prix, (zone.right - 55, zone.y + 8))

            # Description coupée en plusieurs lignes si besoin
            lignes = self.couper_texte(description, police_desc, zone.width - 90)
            y_offset = 30
            for ligne in lignes:
                surface_desc = police_desc.render(ligne, True, (180, 180, 180))
                self.fenetre.blit(surface_desc, (zone.x + 8, zone.y + y_offset))
                y_offset += 14

            dispo = self.argent >= prix
            texte_dispo = "OK" if dispo else "Pas assez"
            couleur_dispo = (120, 240, 120) if dispo else (240, 120, 120)
            self.fenetre.blit(police_desc.render(texte_dispo, True, couleur_dispo), (zone.right - 76, zone.y + 36))