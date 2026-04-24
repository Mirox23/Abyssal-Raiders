import pygame
from setting import *
from chemin import CHEMIN, draw_decor, draw_path, configurer_chemin_niveau_vague
from mob import MobKamikaze, MobSoigneur
from tower import TourSniper, TourCanonnier, TourRalentissement, TourSupport
from ui import (
    PanneauTelephone, PanneauInfos, PanneauAchevement, EcranFinVague, AffichageXP,
    FenetreRecompensesTalents, PanneauCompetences, PanneauObjets, PanneauParametresMusique, FenetreNiveauConquis
)
from vague import GestionnaireVague
from progression import Progression
from competence import GestionnaireCompetences
from musique import MusiqueManager


class Jeu:
    def __init__(self, continent="pirate", volume_musique=0.5, niveau=1, progression_monde=None):
        pygame.init()
        self.fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
        pygame.display.set_caption("Abyssal Raiders")
        self.horloge = pygame.time.Clock()
        self.police_hud = pygame.font.SysFont("consolas", 22)
        self.police_vague = pygame.font.SysFont("consolas", 24, bold=True)
        self.continent = continent
        self.volume_musique = volume_musique
        self.niveau = niveau
        self.progression_monde = progression_monde
        self.musique = MusiqueManager(self.volume_musique)
        self._lancer_musique_continent()
        self.reinitialiser()

    def _lancer_musique_continent(self):
        pistes = {
            "pirate": "musique/continent_pirate.wav",
            "samourai": "musique/continent_japonais.wav",
            "medieval": "musique/continent_medieval.wav",
            "demoniaque": "musique/continent_demoniaque.wav",
        }
        self.musique.jouer(pistes.get(self.continent, "musique/continent_pirate.wav"))

    def reinitialiser(self):
        self.liste_ennemis, self.liste_tours = [], []
        self.points_de_vie_mur, self.argent = vie_mur_depart, argent_depart
        self.telephone = PanneauTelephone()
        self.panneau_infos = PanneauInfos()
        self.panneau_achevement = PanneauAchevement()
        self.ecran_fin_vague = EcranFinVague()
        self.affichage_xp = AffichageXP()
        self.fenetre_recompenses = FenetreRecompensesTalents()
        self.panneau_competences = PanneauCompetences()
        self.panneau_objets = PanneauObjets()
        self.panneau_parametres = PanneauParametresMusique()
        self.fenetre_niveau_conquis = FenetreNiveauConquis()
        self.mode_placement_actif, self.type_tour_a_placer = False, None
        self.tour_actuellement_selectionnee = None
        self.gestionnaire_vague = GestionnaireVague()
        # 1 niveau = 4 vagues.
        self.vague_locale = 0
        self.vague_max = 4
        self.en_attente_lancement_vague = True
        self.demande_retour_map = False
        self.volume_effets = 0.6
        self.musique.regler_volume_effets(self.volume_effets)
        self.progression = Progression()
        self.gestionnaire_competences = GestionnaireCompetences()
        self.mode_fete, self.sequence_easter_egg = False, []
        self.talents_appliques = {"degats_competence": 0, "reduction_cout": 0, "prime_or": 0, "resistance_mur": 0}
        self.inventaire_objets = {"potion_mur": 2, "bourse_or": 2, "totem_froid": 1}
        self.bouton_recompense = pygame.Rect(largeur_ecran - 200, 46, 170, 30)
        self.couts_tours = {TourSniper: 14, TourCanonnier: 10, TourRalentissement: 12, TourSupport: 11}
        self.effets_visuels = []
        configurer_chemin_niveau_vague(self.continent, self.niveau, 1)

    def lancer(self):
        jeu_en_cours = True
        while jeu_en_cours:
            delta_temps = self.horloge.tick(FPS) / 1000
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    jeu_en_cours = False
                elif evenement.type == pygame.MOUSEBUTTONDOWN:
                    self.gerer_clic(evenement.pos)
                elif evenement.type == pygame.KEYDOWN:
                    self.gerer_competence(evenement.key)
                    self.gerer_easter_eggs(evenement.key)
            self.mettre_a_jour(delta_temps)
            self.dessiner()
            pygame.display.flip()
            if self.demande_retour_map:
                jeu_en_cours = False
        pygame.quit()
        return {
            "continent": self.continent,
            "niveau": self.niveau,
            "niveau_conquis": self.progression_monde.est_conquis(self.continent, self.niveau) if self.progression_monde else False,
            "ouvrir_map": self.demande_retour_map,
        }

    def gerer_competence(self, touche):
        cle = self.gestionnaire_competences.obtenir_competence_par_touche(touche)
        if not cle:
            return
        data = self.gestionnaire_competences.competences[cle]
        cout = self._cout_competence(cle)
        if data["cooldown"] > 0 or self.argent < cout:
            return
        if cle == "tir_puissant" and self.liste_ennemis:
            max(self.liste_ennemis, key=lambda e: e.etape).vie -= 8 + self.talents_appliques["degats_competence"]
        elif cle == "pluie_bombes" and self.liste_ennemis:
            pos = pygame.mouse.get_pos()
            self._ajouter_effet(pos, (255, 90, 80), 90, 0.3)
            for ennemi in self.liste_ennemis:
                if ((ennemi.x - pos[0]) ** 2 + (ennemi.y - pos[1]) ** 2) ** 0.5 <= 95:
                    ennemi.vie -= 4 + self.talents_appliques["degats_competence"]
        elif cle == "ralentissement_zone":
            pos = pygame.mouse.get_pos()
            for ennemi in self.liste_ennemis:
                if ((ennemi.x - pos[0]) ** 2 + (ennemi.y - pos[1]) ** 2) ** 0.5 <= 130:
                    ennemi.appliquer_ralentissement(0.35, 2.8)
        self.argent -= cout
        self.gestionnaire_competences.activer(cle)

    def _cout_competence(self, cle_competence):
        data = self.gestionnaire_competences.competences[cle_competence]
        return max(1, data["cout"] - self.talents_appliques["reduction_cout"])

    def gerer_easter_eggs(self, touche):
        if touche == pygame.K_p:
            self.argent += 25
        self.sequence_easter_egg.append(touche)
        self.sequence_easter_egg = self.sequence_easter_egg[-6:]
        if self.sequence_easter_egg == [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            self.mode_fete = not self.mode_fete

    def gerer_clic(self, clic):
        self._ajouter_effet(clic, (130, 210, 255), 16, 0.2)
        if self.fenetre_niveau_conquis.gerer_clic(clic):
            self.demande_retour_map = True
            return
        if self.bouton_recompense.collidepoint(clic):
            self.fenetre_recompenses.ouvrir()
            return
        action = self.fenetre_recompenses.gerer_clic(clic, self.progression)
        if action:
            if action[0] == "recompense":
                self.argent += action[1]
            elif action[0] == "talent":
                self.talents_appliques[action[1]] = self.fenetre_recompenses.talents[action[1]]["niveau"]
            return
        action_param = self.panneau_parametres.gerer_clic(clic)
        if action_param:
            if action_param == "moins":
                self.volume_musique = max(0.0, self.volume_musique - 0.1)
                self.musique.regler_volume(self.volume_musique)
            elif action_param == "plus":
                self.volume_musique = min(1.0, self.volume_musique + 0.1)
                self.musique.regler_volume(self.volume_musique)
            elif action_param == "moins_effets":
                self.volume_effets = max(0.0, self.volume_effets - 0.1)
                self.musique.regler_volume_effets(self.volume_effets)
            elif action_param == "plus_effets":
                self.volume_effets = min(1.0, self.volume_effets + 0.1)
                self.musique.regler_volume_effets(self.volume_effets)
            return
        action_comp = self.panneau_competences.gerer_clic(clic)
        if action_comp:
            if action_comp != "consomme":
                self.gerer_competence(self.gestionnaire_competences.competences[action_comp]["touche"])
            return
        action_obj = self.panneau_objets.gerer_clic(clic)
        if action_obj:
            if action_obj != "consomme":
                self.utiliser_objet(action_obj)
            return
        fin = self.ecran_fin_vague.gerer_clic(clic)
        if fin == "nouvelle_vague":
            self.lancer_nouvelle_vague()
            return
        if fin == "modification":
            self.ecran_fin_vague.fermer()
            self.en_attente_lancement_vague = True
            return
        if self.panneau_achevement.gerer_clic(clic):
            return
        if self.panneau_infos.visible:
            _, self.argent = self.panneau_infos.gerer_clic(clic, self.argent)
            return

        action_tel = self.telephone.gerer_clic(clic)
        if action_tel == "Tourelle":
            self.mode_placement_actif, self.type_tour_a_placer, self.tour_actuellement_selectionnee = True, None, None
            return
        if action_tel == "New vague" and self.en_attente_lancement_vague:
            self.lancer_nouvelle_vague()
            return
        if action_tel == "Achèvement":
            self.panneau_achevement.ouvrir()
            return
        if action_tel == "Info" and self.tour_actuellement_selectionnee:
            self.panneau_infos.ouvrir(self.tour_actuellement_selectionnee)
            return
        if action_tel == "Competence":
            self.panneau_competences.ouvrir()
            return
        if action_tel == "Objets":
            self.panneau_objets.ouvrir()
            return
        if action_tel == "Parametre":
            self.panneau_parametres.ouvrir()
            return
        if action_tel == "Map":
            self.demande_retour_map = True
            return

        if not self.mode_placement_actif:
            self.tour_actuellement_selectionnee = None
            for tour in self.liste_tours:
                if ((clic[0] - tour.x) ** 2 + (clic[1] - tour.y) ** 2) ** 0.5 <= tour.taille + 4:
                    self.tour_actuellement_selectionnee = tour
                    break
        if self.mode_placement_actif and self.type_tour_a_placer is None:
            self._selectionner_tour_menu(clic)
            return
        if self.mode_placement_actif and self.type_tour_a_placer:
            self._placer_tour(clic)

    def _selectionner_tour_menu(self, clic):
        zones = [
            (pygame.Rect(330, 180, 340, 56), TourSniper),
            (pygame.Rect(330, 243, 340, 56), TourCanonnier),
            (pygame.Rect(330, 306, 340, 56), TourRalentissement),
            (pygame.Rect(330, 369, 340, 56), TourSupport),
        ]
        for zone, classe in zones:
            if zone.collidepoint(clic):
                self.type_tour_a_placer = classe
                return

    def _placer_tour(self, clic):
        cout = self.couts_tours.get(self.type_tour_a_placer, prix_tour)
        peut = len(self.liste_tours) < nb_tours_max and clic[0] < pos_mur - 10 and clic[1] > 80 and self.argent >= cout and not self.est_sur_chemin(clic)
        if peut:
            self.liste_tours.append(self.type_tour_a_placer(clic))
            self.argent -= cout
            for tour in self.liste_tours:
                if tour.type_tour == "Support":
                    tour.appliquer_buff(self.liste_tours)
        self.mode_placement_actif = False
        self.type_tour_a_placer = None

    def est_sur_chemin(self, pos):
        for i in range(len(CHEMIN) - 1):
            zone = pygame.Rect(min(CHEMIN[i][0], CHEMIN[i + 1][0]) - 30, min(CHEMIN[i][1], CHEMIN[i + 1][1]) - 30, abs(CHEMIN[i][0] - CHEMIN[i + 1][0]) + 60, abs(CHEMIN[i][1] - CHEMIN[i + 1][1]) + 60)
            if zone.collidepoint(pos):
                return True
        return False

    def lancer_nouvelle_vague(self):
        if self.vague_locale >= self.vague_max:
            return
        self.vague_locale += 1
        # Le dossier niveau_chemin fournit un chemin différent pour chaque vague.
        configurer_chemin_niveau_vague(self.continent, self.niveau, self.vague_locale)
        self.argent += argent_par_vague
        self.gestionnaire_vague.demarrer_vague(CHEMIN[0])
        self.en_attente_lancement_vague = False
        self.ecran_fin_vague.fermer()

    def mettre_a_jour(self, delta_temps):
        self.progression.mettre_a_jour(delta_temps)
        self.gestionnaire_competences.mettre_a_jour(delta_temps)
        if not self.en_attente_lancement_vague and not self.ecran_fin_vague.visible:
            self.gestionnaire_vague.mettre_a_jour(delta_temps, self.liste_ennemis, CHEMIN)
            for ennemi in self.liste_ennemis:
                if isinstance(ennemi, MobSoigneur):
                    ennemi.soigner_alentours(delta_temps, self.liste_ennemis)
            survivants = []
            for ennemi in self.liste_ennemis:
                if ennemi.vie <= 0:
                    self.argent += ennemi.recompense + self.talents_appliques["prime_or"]
                    self.progression.gagner_xp(self.progression.xp_pour_kill())
                    self._ajouter_effet((ennemi.x, ennemi.y), (255, 145, 90), 22, 0.35)
                    continue
                if ennemi.avancer(delta_temps, CHEMIN):
                    if isinstance(ennemi, MobKamikaze):
                        self.points_de_vie_mur -= max(1, ennemi.degats_explosion - self.talents_appliques["resistance_mur"])
                        self._ajouter_effet((position_mur, ennemi.y), (255, 120, 80), 28, 0.5)
                    else:
                        self.points_de_vie_mur -= max(1, 1 - self.talents_appliques["resistance_mur"])
                        self._ajouter_effet((position_mur, ennemi.y), (255, 175, 100), 18, 0.35)
                    continue
                survivants.append(ennemi)
            self.liste_ennemis = survivants
            if self.gestionnaire_vague.vague_terminee:
                self.gestionnaire_vague.vague_terminee = False
                self.en_attente_lancement_vague = True
                xp = self.progression.xp_pour_vague(self.vague_locale)
                self.progression.gagner_xp(xp)
                self.ecran_fin_vague.ouvrir(self.vague_locale, xp)
                if self.vague_locale >= self.vague_max:
                    if self.progression_monde:
                        self.progression_monde.marquer_conquis(self.continent, self.niveau)
                    self.fenetre_niveau_conquis.ouvrir()
        mult = self.gestionnaire_competences.competences["buff_tours"]["multiplicateur_cadence"] if self.gestionnaire_competences.buff_actif() else 1.0
        for tour in self.liste_tours:
            c0 = tour.cadence
            tour.cadence = max(0.08, c0 * mult)
            nb_projectiles_avant = len(tour.liste_projectiles)
            tour.mettre_a_jour(delta_temps, self.liste_ennemis)
            if len(tour.liste_projectiles) > nb_projectiles_avant:
                self._ajouter_effet((tour.x, tour.y), (255, 230, 120), 10, 0.12)
            tour.cadence = c0
        for tour in self.liste_tours:
            if tour.type_tour == "Support":
                tour.appliquer_buff(self.liste_tours)
        self._mettre_a_jour_effets(delta_temps)

    def dessiner(self):
        self.fenetre.fill((32, 35, 55) if self.mode_fete else couleur_fond)
        draw_decor(self.fenetre, pygame)
        draw_path(self.fenetre, pygame)
        for tour in self.liste_tours:
            tour.dessiner(self.fenetre)
        for ennemi in self.liste_ennemis:
            ennemi.dessiner(self.fenetre)
        self.fenetre.blit(self.police_hud.render(f"Vie : {self.points_de_vie_mur}", True, couleur_texte), (20, 20))
        self.fenetre.blit(self.police_hud.render(f"Argent : {self.argent} ¤", True, couleur_texte), (20, 48))
        texte_vague = f"— Vague {self.vague_locale}/{self.vague_max} —" if self.vague_locale > 0 else "— Pret —"
        surf_vague = self.police_vague.render(texte_vague, True, (200, 180, 80))
        self.fenetre.blit(surf_vague, (largeur_ecran // 2 - surf_vague.get_width() // 2, 14))
        self._dessiner_effets()
        self.affichage_xp.dessiner(self.fenetre, self.progression)
        self._dessiner_bouton_recompense()
        if self.tour_actuellement_selectionnee:
            self._dessiner_info_tour()
        if self.mode_placement_actif and self.type_tour_a_placer is None:
            self._dessiner_menu_type_tour()
        self.telephone.dessiner(self.fenetre)
        self.panneau_infos.dessiner(self.fenetre)
        self.panneau_achevement.dessiner(self.fenetre)
        self.ecran_fin_vague.dessiner(self.fenetre)
        self.panneau_competences.dessiner(
            self.fenetre,
            self.gestionnaire_competences,
            self.argent,
            self.talents_appliques["reduction_cout"],
        )
        self.panneau_objets.dessiner(self.fenetre, self.inventaire_objets)
        self.panneau_parametres.dessiner(self.fenetre, self.volume_musique, self.volume_effets)
        self.fenetre_recompenses.dessiner(self.fenetre, self.progression)
        self.fenetre_niveau_conquis.dessiner(self.fenetre)

    def _ajouter_effet(self, pos, couleur, rayon, duree):
        self.effets_visuels.append({"x": float(pos[0]), "y": float(pos[1]), "couleur": couleur, "rayon": rayon, "duree": duree, "temps": duree})

    def _mettre_a_jour_effets(self, delta_temps):
        restants = []
        for effet in self.effets_visuels:
            effet["temps"] -= delta_temps
            if effet["temps"] > 0:
                restants.append(effet)
        self.effets_visuels = restants

    def _dessiner_effets(self):
        for effet in self.effets_visuels:
            ratio = effet["temps"] / effet["duree"]
            rayon = max(2, int(effet["rayon"] * (1 - ratio * 0.5)))
            pygame.draw.circle(self.fenetre, effet["couleur"], (int(effet["x"]), int(effet["y"])), rayon, max(1, int(3 * ratio)))

    def _dessiner_bouton_recompense(self):
        # Bouton aligné avec le système de progression du niveau (XP/talents).
        x = largeur_ecran - 200
        y = 44
        self.bouton_recompense = pygame.Rect(x, y, 176, 36)
        survol = self.bouton_recompense.collidepoint(pygame.mouse.get_pos())
        couleur_fond = (62, 118, 72) if survol else (34, 78, 44)
        pygame.draw.rect(self.fenetre, (18, 24, 38), self.bouton_recompense.move(2, 2), border_radius=8)
        pygame.draw.rect(self.fenetre, couleur_fond, self.bouton_recompense, border_radius=8)
        pygame.draw.rect(self.fenetre, (165, 225, 170), self.bouton_recompense, width=1, border_radius=8)

        police_titre = pygame.font.SysFont("consolas", 13, bold=True)
        police_detail = pygame.font.SysFont("consolas", 11)
        txt = police_titre.render("Recompenses", True, (235, 255, 235))
        txt_niveau = police_detail.render(f"Niv {self.progression.niveau}", True, (210, 240, 210))
        self.fenetre.blit(txt, (self.bouton_recompense.x + 10, self.bouton_recompense.y + 4))
        self.fenetre.blit(txt_niveau, (self.bouton_recompense.x + 10, self.bouton_recompense.y + 20))

    def _dessiner_info_tour(self):
        tour = self.tour_actuellement_selectionnee
        police = pygame.font.SysFont("consolas", 14)
        for i, ligne in enumerate([tour.type_tour, f"Niv {tour.niveau}", f"Portée {int(tour.portee)}"]):
            surf = police.render(ligne, True, (230, 230, 230))
            self.fenetre.blit(surf, (int(tour.x) + tour.taille + 8, int(tour.y) - 20 + i * 16))

    def _dessiner_menu_type_tour(self):
        police_menu = pygame.font.SysFont("consolas", 18)
        police_desc = pygame.font.SysFont("consolas", 11)
        donnees = [
            (pygame.Rect(330, 180, 340, 56), "Sniper", "Longue portee, degats x3", self.couts_tours[TourSniper], (15, 15, 15), (80, 80, 80), (255, 255, 255)),
            (pygame.Rect(330, 243, 340, 56), "Canonnier", "Courte portee, cadence elevee", self.couts_tours[TourCanonnier], (110, 55, 10), (160, 100, 40), (255, 220, 180)),
            (pygame.Rect(330, 306, 340, 56), "Ralentissement", "Ralenti les groupes ennemis", self.couts_tours[TourRalentissement], (20, 100, 160), (40, 150, 210), (180, 230, 255)),
            (pygame.Rect(330, 369, 340, 56), "Support", "Boost cadence tours proches", self.couts_tours[TourSupport], (140, 120, 10), (200, 180, 30), (255, 240, 150)),
        ]
        fond = pygame.Rect(320, 170, 360, 265)
        pygame.draw.rect(self.fenetre, (20, 22, 35), fond, border_radius=10)
        pygame.draw.rect(self.fenetre, (70, 75, 110), fond, width=1, border_radius=10)
        self.fenetre.blit(pygame.font.SysFont("consolas", 14).render("Choisir une tour :", True, (160, 160, 200)), (fond.x + 10, fond.y + 6))
        for zone, nom, desc, prix, cf, cb, ct in donnees:
            pygame.draw.rect(self.fenetre, cf, zone, border_radius=6)
            pygame.draw.rect(self.fenetre, cb, zone, width=1, border_radius=6)
            self.fenetre.blit(police_menu.render(nom, True, ct), (zone.x + 8, zone.y + 4))
            self.fenetre.blit(police_desc.render(f"{prix} ¤", True, (255, 215, 0)), (zone.right - 55, zone.y + 8))
            self.fenetre.blit(police_desc.render(desc, True, (180, 180, 180)), (zone.x + 8, zone.y + 31))
            self.fenetre.blit(police_desc.render("OK" if self.argent >= prix else "Pas assez", True, (120, 240, 120) if self.argent >= prix else (240, 120, 120)), (zone.right - 76, zone.y + 36))

    def utiliser_objet(self, cle_objet):
        if self.inventaire_objets.get(cle_objet, 0) <= 0:
            return
        self.inventaire_objets[cle_objet] -= 1
        if cle_objet == "potion_mur":
            self.points_de_vie_mur = min(vie_mur_depart + 10, self.points_de_vie_mur + 2)
        elif cle_objet == "bourse_or":
            self.argent += 6
        elif cle_objet == "totem_froid":
            for ennemi in self.liste_ennemis:
                ennemi.appliquer_ralentissement(0.45, 1.2)
