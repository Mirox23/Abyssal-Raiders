import os
import pygame
from setting import *
from chemin import CHEMIN, draw_decor, draw_path, configurer_chemin_niveau_vague
from mob import MobKamikaze, MobSoigneur, MobBoss, MobRapide, definir_continent_mob
from tower import TourSniper, TourCanonnier, TourRalentissement, TourSupport
from ui import (
    PanneauTelephone, PanneauInfos, PanneauAchevement, EcranFinVague, AffichageXP,
    FenetreRecompensesTalents, PanneauCompetences, PanneauObjets, PanneauParametresMusique,
    FenetreNiveauConquis, FenetreMarcheVague, FenetreScores
)
from vague import GestionnaireVague
from progression import Progression
from competence import GestionnaireCompetences
from musique import MusiqueManager
from scores import enregistrer_score
from tutoriel import GestionnaireTutoriel, etape_ameliorer_tour, etape_lancer_vague


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
        self.image_fond = self._charger_image_fond()  # fond spécifique au continent
        self.reinitialiser()

    def _lancer_musique_continent(self):
        # Musique de jeu normale (vagues simples et modifications)
        self.musique.jouer("jeu")  # appelle musique/jeu.mp3

    def _lancer_musique_boss(self):
        """Musique spéciale pour les vagues de boss uniquement."""
        self.musique.jouer("boss")  # appelle musique/boss.mp3
    def _charger_image_fond(self):
        """
        Charge l'image de fond correspondant au continent actif.
        Si l'image n'existe pas, retourne None (on utilisera la couleur unie de secours).
        """
        # Chemins possibles pour chaque continent
        chemins_fond = {
            "pirate": ["image/pirates/fond.png"],
            "samourai": ["image/samourai/fond.png"],
            "medieval": ["image/medieval/fond.png"],
            "demoniaque": ["image/demoniaque/fond.png"],
        }
        essais = chemins_fond.get(self.continent, [])
        for chemin in essais:
            if os.path.exists(chemin):
                try:
                    img = pygame.image.load(chemin).convert()
                    # On redimensionne pour couvrir tout l'écran
                    return pygame.transform.scale(img, (largeur_ecran, hauteur_ecran))
                except Exception:
                    pass
        return None  # pas d'image trouvée, on utilisera la couleur unie

    def reinitialiser(self):
        self.liste_ennemis, self.liste_tours = [], []
        self.points_de_vie_mur = vie_mur_depart
        self.argent = argent_depart
        # Bonus de fidélité inter-sessions (augmente avec la progression dans le monde, réinitialisé à 0 si pas de progression fournie)
        if self.progression_monde:
            self.argent += self.progression_monde.bonus_fidelite_argent(self.continent, self.niveau)
            self.points_de_vie_mur += self.progression_monde.bonus_fidelite_vie(self.continent, self.niveau)
            self._bonus_fidelite_argent = self.progression_monde.bonus_fidelite_argent(self.continent, self.niveau)
            self._bonus_fidelite_vie = self.progression_monde.bonus_fidelite_vie(self.continent, self.niveau)
        else:
            self._bonus_fidelite_argent = 0
            self._bonus_fidelite_vie = 0
        self.telephone = PanneauTelephone()
        self.panneau_infos = PanneauInfos()
        self.panneau_achevement = PanneauAchevement()
        self.panneau_achevement.lier_progression_monde(self.progression_monde)
        self.ecran_fin_vague = EcranFinVague()
        self.affichage_xp = AffichageXP()
        self.fenetre_recompenses = FenetreRecompensesTalents()
        self.panneau_competences = PanneauCompetences()
        self.panneau_objets = PanneauObjets()
        self.panneau_parametres = PanneauParametresMusique()
        self.fenetre_niveau_conquis = FenetreNiveauConquis()
        # Marché et Scores
        self.fenetre_marche = FenetreMarcheVague()
        self.fenetre_scores = FenetreScores()
        self._primes_doubles_vague = False   # effet de carte "argent_double"
        self._bonus_portee_cartes = 0        # effet de carte "portee_bonus"
        self._bonus_cadence_cartes = 0.0     # effet de carte "cadence_bonus" (%)
        self.mode_placement_actif, self.type_tour_a_placer = False, None
        self.tour_actuellement_selectionnee = None
        self.gestionnaire_vague = GestionnaireVague()
        # 1 niveau = 3 vagues + 1 vague boss finale (vague 4 = boss)
        self.vague_locale = 0
        self.vague_max = 4
        self.en_attente_lancement_vague = True
        self.demande_retour_map = False
        self.volume_effets = 0.6
        self.musique.regler_volume_effets(self.volume_effets)
        self.progression = Progression()
        self.gestionnaire_competences = GestionnaireCompetences()
        self.mode_fete, self.sequence_easter_egg = False, []
        self.talents_appliques = {
            "degats_competence": 0, "reduction_cout": 0,
            "prime_or": 0, "resistance_mur": 0,
            # Nouveaux talents à implémenter dans progression.py et appliquer dans les méthodes correspondantes :
            "chasseur": 0, "ingenieur": 0, "alchimiste": 0,
        }
        self.inventaire_objets = {"potion_mur": 2, "bourse_or": 2, "totem_froid": 1}
        self.bouton_recompense = pygame.Rect(largeur_ecran - 200, 46, 170, 30)
        self.couts_tours = {TourSniper: 14, TourCanonnier: 10, TourRalentissement: 12, TourSupport: 11}
        self.effets_visuels = []
        self.map_jeu_ouverte = False
        self.bouton_retour_jeu = pygame.Rect(largeur_ecran // 2 - 120, hauteur_ecran - 92, 240, 44)
        self.temps_vague_actuelle = 0.0
        self.score_total_partie = 0
        # Screen shake
        self._shake_timer = 0.0
        self._shake_amplitude = 0
        self._shake_offset = (0, 0)
        # Alarme visuelle mobs proches du mur
        self._alarme_clignotement = 0.0
        self.vitesse_jeu = 1.0
        self.est_mort = False
        self.bouton_rejouer_payant = pygame.Rect(largeur_ecran // 2 - 180, hauteur_ecran // 2 + 40, 170, 44)
        self.bouton_recommencer = pygame.Rect(largeur_ecran // 2 + 10, hauteur_ecran // 2 + 40, 170, 44)
        self.vie_debut_vague = self.points_de_vie_mur
        self.echec_vague = False
        self.vague_echec_numero = 0
        self.bouton_payer_passer = pygame.Rect(largeur_ecran // 2 - 180, hauteur_ecran // 2 + 40, 170, 44)
        self.bouton_relancer_vague = pygame.Rect(largeur_ecran // 2 + 10, hauteur_ecran // 2 + 40, 170, 44)
        configurer_chemin_niveau_vague(self.continent, self.niveau, 1)
        definir_continent_mob(self.continent)
        # Le tutoriel ne se lance qu'a la toute premiere vague (niveau 1, pas encore joue)
        tutoriel_deja_fait = False
        if self.progression_monde:
            tutoriel_deja_fait = getattr(self.progression_monde, "tutoriel_termine", False)
        if self.niveau == 1 and not tutoriel_deja_fait:
            self.tutoriel = GestionnaireTutoriel()
        else:
            self.tutoriel = None
        # Afficher le bonus de fidélité si présent
        self._message_fidelite = ""
        self._timer_message_fidelite = 0.0
        if self._bonus_fidelite_argent > 0 or self._bonus_fidelite_vie > 0:
            parties = []
            if self._bonus_fidelite_argent > 0:
                parties.append(f"+{self._bonus_fidelite_argent} or")
            if self._bonus_fidelite_vie > 0:
                parties.append(f"+{self._bonus_fidelite_vie} PV mur")
            self._message_fidelite = "Bonus fidélité : " + " & ".join(parties)
            self._timer_message_fidelite = 4.0

    def lancer(self):
        jeu_en_cours = True
        while jeu_en_cours:
            delta_temps = (self.horloge.tick(FPS) / 1000) * self.vitesse_jeu
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
            self._jouer_son_effet("explosion")
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
        if self.est_mort:
            if self.bouton_rejouer_payant.collidepoint(clic) and self.argent >= 200:
                self.argent -= 200
                self.points_de_vie_mur = max(3, vie_mur_depart // 2)
                self.liste_ennemis = []
                self.en_attente_lancement_vague = True
                self.ecran_fin_vague.fermer()
                self.fenetre_marche.fermer()
                self.est_mort = False
            elif self.bouton_recommencer.collidepoint(clic):
                self.reinitialiser()
            return
        if self.echec_vague:
            if self.bouton_payer_passer.collidepoint(clic) and self.argent >= 100:
                self.argent -= 100
                self.echec_vague = False
                if self.vague_locale < self.vague_max:
                    self.fenetre_marche.ouvrir()
                else:
                    self.fenetre_niveau_conquis.ouvrir()
            elif self.bouton_relancer_vague.collidepoint(clic):
                self.echec_vague = False
                self.liste_ennemis = []
                self.vague_locale = max(0, self.vague_echec_numero - 1)
                self.lancer_nouvelle_vague()
            return
        self._ajouter_effet(clic, (130, 210, 255), 16, 0.2)
        self._jouer_son_effet("clic")
        if self.map_jeu_ouverte:
            if self.bouton_retour_jeu.collidepoint(clic):
                self.map_jeu_ouverte = False
            return

        action_niveau = self.fenetre_niveau_conquis.gerer_clic(clic)
        if action_niveau == "retour_map":
            self.demande_retour_map = True
            return
        if action_niveau == "niveau_suivant":
            self.niveau = min(8, self.niveau + 1)
            self.reinitialiser()
            return
        if self.bouton_recompense.collidepoint(clic):
            self.fenetre_recompenses.ouvrir()
            if self.tutoriel:
                self.tutoriel.notifier_action("bouton_recompense_clique")
            return
        action = self.fenetre_recompenses.gerer_clic(clic, self.progression)
        if action:
            if action[0] == "recompense":
                self.argent += action[1]
            elif action[0] == "talent":
                cle_t = action[1]
                niv_t = self.fenetre_recompenses.talents[cle_t]["niveau"]
                # Tous les talents connus (anciens + nouveaux)
                if cle_t in self.talents_appliques:
                    self.talents_appliques[cle_t] = niv_t
                # Talent ingenieur : augmenter portee de toutes les tours existantes
                if cle_t == "ingenieur":
                    for tour in self.liste_tours:
                        tour.portee += 8
            elif action[0] == "onglet_talent":
                if self.tutoriel:
                    self.tutoriel.notifier_action("onglet_talent_clique")
            return

        # Marché entre vagues
        id_carte = self.fenetre_marche.gerer_clic(clic)
        if id_carte is not None:
            self._appliquer_carte_marche(id_carte)
            self.lancer_nouvelle_vague()
            return
        if self.fenetre_marche.visible and self.fenetre_marche.rect.collidepoint(clic):
            return

        # Scores
        if self.fenetre_scores.gerer_clic(clic):
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
            elif action_param == "vitesse_x15":
                self.vitesse_jeu = 1.5
            elif action_param == "vitesse_x2":
                self.vitesse_jeu = 2.0
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
            # ouvrir le marché avant la prochaine vague
            self.ecran_fin_vague.fermer()
            if self.vague_locale < self.vague_max:
                self.fenetre_marche.ouvrir()
            else:
                self.lancer_nouvelle_vague()
            return
        if fin == "modification":
            self.ecran_fin_vague.fermer()
            self.en_attente_lancement_vague = True
            if self.tutoriel:
                self.tutoriel.notifier_action("modification_cliquee")
            return
        if self.panneau_achevement.gerer_clic(clic):
            return
        if self.panneau_infos.visible:
            action_info, self.argent = self.panneau_infos.gerer_clic(clic, self.argent)
            if action_info == "revendre" and self.panneau_infos.tour_selectionnee:
                tour = self.panneau_infos.tour_selectionnee
                if tour in self.liste_tours:
                    self.liste_tours.remove(tour)
                    self._ajouter_effet((tour.x, tour.y), (255, 210, 120), 26, 0.25)
                self.panneau_infos.fermer()
            return

        action_tel = self.telephone.gerer_clic(clic)
        if action_tel == "Tourelle":
            self.mode_placement_actif, self.type_tour_a_placer, self.tour_actuellement_selectionnee = True, None, None
            if self.tutoriel:
                self.tutoriel.notifier_action("telephone_tourelle_clique")
            return
        if action_tel == "New vague" and self.en_attente_lancement_vague:
            self.lancer_nouvelle_vague()
            if self.tutoriel:
                self.tutoriel.notifier_action("vague_lancee")
            return
        if action_tel == "Succes":
            self.panneau_achevement.ouvrir()
            if self.tutoriel:
                self.tutoriel.notifier_action("telephone_succes_clique")
            return
        if action_tel == "Info" and self.tour_actuellement_selectionnee:
            self.panneau_infos.ouvrir(self.tour_actuellement_selectionnee)
            if self.tutoriel:
                self.tutoriel.notifier_action("telephone_info_clique")
            return
        if action_tel == "Competence":
            self.panneau_competences.ouvrir()
            if self.tutoriel:
                self.tutoriel.notifier_action("telephone_competence_clique")
            return
        if action_tel == "Objets":
            self.panneau_objets.ouvrir()
            if self.tutoriel:
                self.tutoriel.notifier_action("telephone_objet_clique")
            return
        if action_tel == "Parametre":
            self.panneau_parametres.ouvrir()
            return
        if action_tel == "Map":
            self.demande_retour_map = True
            return
        if action_tel == "Scores":
            self.fenetre_scores.ouvrir(self.continent)
            return

        if not self.mode_placement_actif:
            self.tour_actuellement_selectionnee = None
            for tour in self.liste_tours:
                if ((clic[0] - tour.x) ** 2 + (clic[1] - tour.y) ** 2) ** 0.5 <= tour.taille + 4:
                    self.tour_actuellement_selectionnee = tour
                    if self.tutoriel:
                        self.tutoriel.notifier_action("tour_selectionnee")
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
        emplacement_libre = True
        for tour in self.liste_tours:
            if ((clic[0] - tour.x) ** 2 + (clic[1] - tour.y) ** 2) ** 0.5 < (tour.taille + 24):
                emplacement_libre = False
                break
        peut = (
            len(self.liste_tours) < nb_tours_max
            and clic[0] < pos_mur - 10
            and clic[1] > 80
            and self.argent >= cout
            and emplacement_libre
            and not self.est_sur_chemin(clic)
        )
        if peut:
            self.liste_tours.append(self.type_tour_a_placer(clic))
            self.argent -= cout
            for tour in self.liste_tours:
                if tour.type_tour == "Support":
                    tour.appliquer_buff(self.liste_tours)
            if self.tutoriel:
                self.tutoriel.notifier_action("tour_placee")
        self.mode_placement_actif = False
        self.type_tour_a_placer = None

    def est_sur_chemin(self, pos):
        # Test géométrique précis pour éviter les faux positifs de placement.
        largeur_interdite = 18
        for i in range(len(CHEMIN) - 1):
            x1, y1 = CHEMIN[i]
            x2, y2 = CHEMIN[i + 1]
            dist = self._distance_point_segment(pos[0], pos[1], x1, y1, x2, y2)
            if dist <= largeur_interdite:
                return True
        return False

    def _distance_point_segment(self, px, py, x1, y1, x2, y2):
        vx = x2 - x1
        vy = y2 - y1
        wx = px - x1
        wy = py - y1
        long2 = vx * vx + vy * vy
        if long2 == 0:
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
        t = max(0.0, min(1.0, (wx * vx + wy * vy) / long2)) # projection du point sur le segment, limitée à [0,1]
        proj_x = x1 + t * vx
        proj_y = y1 + t * vy
        return ((px - proj_x) ** 2 + (py - proj_y) ** 2) ** 0.5

    def lancer_nouvelle_vague(self):
        if self.vague_locale >= self.vague_max:
            return
        self.vague_locale += 1
        # Le dossier niveau_chemin fournit un chemin différent pour chaque vague.
        configurer_chemin_niveau_vague(self.continent, self.niveau, self.vague_locale)
        self.argent += argent_par_vague
        # la dernière vague est une vague boss 
        est_boss = (self.vague_locale == self.vague_max)
        self.gestionnaire_vague.demarrer_vague(CHEMIN[0], est_boss=est_boss)
        # Musique spéciale pour le boss, musique normale sinon
        if est_boss:
            self._lancer_musique_boss()
        else:
            self._lancer_musique_continent()
        self.vie_debut_vague = self.points_de_vie_mur
        self.en_attente_lancement_vague = False
        self.ecran_fin_vague.fermer()
        self.fenetre_marche.fermer()
        self.temps_vague_actuelle = 0.0
        # Appliquer bonus de portée issu des cartes marché
        if self._bonus_portee_cartes > 0:
            for tour in self.liste_tours:
                tour.portee += self._bonus_portee_cartes
            self._bonus_portee_cartes = 0

    def mettre_a_jour(self, delta_temps):
        import math as _math
        if self.est_mort or self.echec_vague:
            return
        if self.est_mort or self.echec_vague:
            return
        self.progression.mettre_a_jour(delta_temps)
        self.gestionnaire_competences.mettre_a_jour(delta_temps)
        # Mise a jour du tutoriel
        if self.tutoriel:
            self.tutoriel.mettre_a_jour(delta_temps)
            # On propose l'amelioration quand le joueur a assez d'or pendant la vague
            if self.tutoriel.etape_actuelle == etape_lancer_vague and self.gestionnaire_vague.vague_en_cours:
                if self.argent >= 15 and self.liste_tours:
                    self.tutoriel.etape_actuelle = etape_ameliorer_tour
            # Quand le tutoriel est fini on le note dans la progression pour ne plus le relancer
            if self.tutoriel.est_termine():
                if self.progression_monde:
                    self.progression_monde.tutoriel_termine = True
                self.tutoriel = None

        # Timers divers
        self._alarme_clignotement += delta_temps
        if self._timer_message_fidelite > 0:
            self._timer_message_fidelite = max(0.0, self._timer_message_fidelite - delta_temps)

        # Screen shake : décrémente et recalcule l'offset à appliquer au dessin
        if self._shake_timer > 0:
            self._shake_timer = max(0.0, self._shake_timer - delta_temps)
            amp = self._shake_amplitude
            import random as _rand
            self._shake_offset = (_rand.randint(-amp, amp), _rand.randint(-amp, amp))
        else:
            self._shake_offset = (0, 0)

        if not self.en_attente_lancement_vague and not self.ecran_fin_vague.visible and not self.fenetre_marche.visible:
            self.temps_vague_actuelle += delta_temps
            self.gestionnaire_vague.mettre_a_jour(delta_temps, self.liste_ennemis, CHEMIN)
            for ennemi in self.liste_ennemis:
                if isinstance(ennemi, MobSoigneur):
                    ennemi.soigner_alentours(delta_temps, self.liste_ennemis)

            mobs_a_spawner_apres = []   # mobs issus de la mort du boss
            survivants = []
            for ennemi in self.liste_ennemis:
                if ennemi.vie <= 0:
                    # Bonus chasseur : prime doublée sur rapides/kamikazes
                    bonus_chasseur = self.talents_appliques.get("chasseur", 0)
                    if isinstance(ennemi, (MobRapide, MobKamikaze)):
                        self.argent += ennemi.recompense + bonus_chasseur
                    else:
                        self.argent += ennemi.recompense
                    # Primes doubles si carte marché "argent_double" active
                    if self._primes_doubles_vague:
                        self.argent += ennemi.recompense
                    self.progression.gagner_xp(self.progression.xp_pour_kill() + ennemi.xp)
                    # Particules de mort enrichies (5 éclats colorés) 
                    self._ajouter_particules_mort(ennemi.x, ennemi.y, ennemi.couleur)
                    self._jouer_son_effet("explosion")
                    # Boss : spawner 3 mobs normaux à sa mort 
                    if isinstance(ennemi, MobBoss):
                        for _ in range(3):
                            mobs_a_spawner_apres.append(type("_SpawnMob", (), {"classe": __import__("mob").Mob, "pos": CHEMIN[0]})())
                    continue

                if ennemi.avancer(delta_temps, CHEMIN):
                    # Ennemi a atteint le mur
                    if isinstance(ennemi, MobKamikaze):
                        degats = max(1, ennemi.degats_explosion - self.talents_appliques["resistance_mur"])
                    elif isinstance(ennemi, MobBoss):
                        degats = max(1, ennemi.degats_mur - self.talents_appliques["resistance_mur"])
                    else:
                        degats = max(1, 1 - self.talents_appliques["resistance_mur"])
                    self.points_de_vie_mur -= degats
                    if self.points_de_vie_mur <= 0:
                        self.points_de_vie_mur = 0
                        self.est_mort = True
                        self.en_attente_lancement_vague = True
                        self.gestionnaire_vague.vague_en_cours = False
                        self.fenetre_marche.fermer()
                        self.ecran_fin_vague.fermer()
                        break
                    if self.points_de_vie_mur <= 0:
                        self.points_de_vie_mur = 0
                        self.est_mort = True
                        self.en_attente_lancement_vague = True
                        self.gestionnaire_vague.vague_en_cours = False
                        self.fenetre_marche.fermer()
                        self.ecran_fin_vague.fermer()
                        break
                    self._ajouter_effet((position_mur, ennemi.y), (255, 120, 80), 28 + degats * 4, 0.5)
                    self._ajouter_effet((position_mur, ennemi.y), (255, 220, 180), 16, 0.25)
                    self._jouer_son_effet("mur")
                    # Screen shake quand le mur est touché : plus fort si les dégâts sont importants
                    self._shake_timer = 0.25 + degats * 0.05
                    self._shake_amplitude = 4 + degats
                    continue

                survivants.append(ennemi)

            # Spawn des mobs issus de la mort du boss
            import mob as _mob_module
            for spawn in mobs_a_spawner_apres:
                survivants.append(_mob_module.Mob(CHEMIN[0]))

            self.liste_ennemis = survivants

            if self.gestionnaire_vague.vague_terminee:
                self.gestionnaire_vague.vague_terminee = False
                self._lancer_musique_continent()
                # On signale au tutoriel que la vague est finie pour passer a l'etape modification
                if self.tutoriel:
                    self.tutoriel.notifier_vague_terminee()
                self._primes_doubles_vague = False   # reset effet carte
                self.en_attente_lancement_vague = True
                xp = self.progression.xp_pour_vague(self.vague_locale)
                self.progression.gagner_xp(xp)
                score_vague = int(self.points_de_vie_mur * 120 + max(0, 2000 - self.temps_vague_actuelle * 80))
                self.score_total_partie += score_vague
                self.ecran_fin_vague.ouvrir(self.vague_locale, xp, score_vague)
                degats_vague = max(0, self.vie_debut_vague - self.points_de_vie_mur)
                if self.vague_locale <= 3:
                    if degats_vague < 3:
                        self.panneau_achevement.marquer_vague(self.continent, self.niveau, self.vague_locale)
                    else:
                        self.echec_vague = True
                        self.vague_echec_numero = self.vague_locale
                        self.ecran_fin_vague.fermer()
                degats_vague = max(0, self.vie_debut_vague - self.points_de_vie_mur)
                if self.vague_locale <= 3:
                    if degats_vague < 3:
                        self.panneau_achevement.marquer_vague(self.continent, self.niveau, self.vague_locale)
                    else:
                        self.echec_vague = True
                        self.vague_echec_numero = self.vague_locale
                        self.ecran_fin_vague.fermer()
                if self.vague_locale >= self.vague_max:
                    if self.progression_monde:
                        self.progression_monde.marquer_conquis(self.continent, self.niveau)
                    self.panneau_achevement.marquer_niveau_conquis(self.continent, self.niveau)
                    # Enregistrer le score total dans le leaderboard local 
                    enregistrer_score(self.continent, self.niveau, self.score_total_partie, self.progression.niveau)
                    self.fenetre_niveau_conquis.ouvrir()

        mult = self.gestionnaire_competences.competences["buff_tours"]["multiplicateur_cadence"] if self.gestionnaire_competences.buff_actif() else 1.0
        for tour in self.liste_tours:
            c0 = tour.cadence
            tour.cadence = max(0.08, c0 * mult)
            nb_projectiles_avant = len(tour.liste_projectiles)
            tour.mettre_a_jour(delta_temps, self.liste_ennemis)
            if len(tour.liste_projectiles) > nb_projectiles_avant:
                self._ajouter_effet((tour.x, tour.y), (255, 230, 120), 10, 0.12)
                self._jouer_son_effet("tir")
            tour.cadence = c0
        for tour in self.liste_tours:
            if tour.type_tour == "Support":
                tour.appliquer_buff(self.liste_tours)
        self._mettre_a_jour_effets(delta_temps)

    def dessiner(self):
        import math as _math

        # Screen shake : décaler toute la surface de rendu 
        ox, oy = self._shake_offset

        # Fond : image du continent si dispo, sinon couleur unie de secours
        if self.image_fond:
            self.fenetre.blit(self.image_fond, (0, 0))
        else:
            self.fenetre.fill((32, 35, 55) if self.mode_fete else couleur_fond)
        draw_decor(self.fenetre, pygame)
        draw_path(self.fenetre, pygame)

        # Alarme visuelle : flash rouge sur le bord droit quand ennemi proche du mur 
        mobs_danger = [e for e in self.liste_ennemis if e.x >= position_mur - 200]
        if mobs_danger:
            alpha = int(55 + 45 * _math.sin(self._alarme_clignotement * 7))
            alpha = max(0, min(140, alpha))
            surf_alarme = pygame.Surface((220, hauteur_ecran), pygame.SRCALPHA)
            surf_alarme.fill((255, 40, 40, alpha))
            self.fenetre.blit(surf_alarme, (position_mur - 200 + ox, oy))

        for tour in self.liste_tours:
            tour.dessiner(self.fenetre)
        for ennemi in self.liste_ennemis:
            ennemi.dessiner(self.fenetre)

        # HUD principal (avec shake)
        self.fenetre.blit(self.police_hud.render(f"Vie : {self.points_de_vie_mur}", True, couleur_texte), (20 + ox, 20 + oy))
        self.fenetre.blit(self.police_hud.render(f"Argent : {self.argent} ¤", True, couleur_texte), (20 + ox, 48 + oy))

        # Compteur de mobs restants
        total_restants = len(self.liste_ennemis) + len(self.gestionnaire_vague.mobs_a_spawner)
        if self.gestionnaire_vague.vague_en_cours:
            surf_mobs = pygame.font.SysFont("consolas", 14).render(f"{total_restants} ennemi(s) restant(s)", True, (200, 180, 140))
            self.fenetre.blit(surf_mobs, (20 + ox, 74 + oy))

        # Titre vague
        if self.gestionnaire_vague.est_vague_boss and self.gestionnaire_vague.vague_en_cours:
            texte_vague = f"⚔ VAGUE BOSS {self.vague_locale}/{self.vague_max} ⚔"
            couleur_vague = (255, 80, 80)
        else:
            texte_vague = f"— Vague {self.vague_locale}/{self.vague_max} —" if self.vague_locale > 0 else "— Pret —"
            couleur_vague = (200, 180, 80)
        surf_vague = self.police_vague.render(texte_vague, True, couleur_vague)
        self.fenetre.blit(surf_vague, (largeur_ecran // 2 - surf_vague.get_width() // 2 + ox, 14 + oy))

        self._dessiner_effets()
        self.affichage_xp.dessiner(self.fenetre, self.progression)
        self._dessiner_bouton_recompense()

        # Message bonus fidélité 
        if self._timer_message_fidelite > 0:
            alpha_fid = min(255, int(self._timer_message_fidelite * 80))
            surf_fid = pygame.font.SysFont("consolas", 16, bold=True).render(self._message_fidelite, True, (255, 220, 80))
            surf_fid.set_alpha(alpha_fid)
            self.fenetre.blit(surf_fid, (largeur_ecran // 2 - surf_fid.get_width() // 2, 50))

        if self.tour_actuellement_selectionnee:
            self._dessiner_info_tour()
        if self.mode_placement_actif and self.type_tour_a_placer is None:
            self._dessiner_menu_type_tour()
        self.telephone.dessiner(self.fenetre)
        self.panneau_infos.dessiner(self.fenetre)
        self.panneau_achevement.dessiner(self.fenetre)
        self.ecran_fin_vague.dessiner(self.fenetre)
        # marché et scores 
        self.fenetre_marche.dessiner(self.fenetre)
        self.fenetre_scores.dessiner(self.fenetre)
        self.panneau_competences.dessiner(
            self.fenetre,
            self.gestionnaire_competences,
            self.argent,
            self.talents_appliques["reduction_cout"],
        )
        self.panneau_objets.dessiner(self.fenetre, self.inventaire_objets)
        self.panneau_parametres.dessiner(self.fenetre, self.volume_musique, self.volume_effets, self.vitesse_jeu)
        if self.est_mort:
            self._dessiner_ecran_defaite()
        if self.echec_vague:
            self._dessiner_ecran_echec_vague()
        self.panneau_parametres.dessiner(self.fenetre, self.volume_musique, self.volume_effets, self.vitesse_jeu)
        if self.est_mort:
            self._dessiner_ecran_defaite()
        if self.echec_vague:
            self._dessiner_ecran_echec_vague()
        self.fenetre_recompenses.dessiner(self.fenetre, self.progression)
        self.fenetre_niveau_conquis.dessiner(self.fenetre)
        # Dessin du tutoriel par dessus tout le reste
        if self.tutoriel:
            self.tutoriel.dessiner(self.fenetre)
        if self.map_jeu_ouverte:
            self._dessiner_map_jeu()

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
        # Intégré à la zone XP sans trou visuel.
        x = largeur_ecran - 200
        y = 34
        self.bouton_recompense = pygame.Rect(x, y, 180, 26)
        survol = self.bouton_recompense.collidepoint(pygame.mouse.get_pos())
        couleur_fond = (68, 128, 82) if survol else (40, 90, 58)
        pygame.draw.rect(self.fenetre, couleur_fond, self.bouton_recompense, border_radius=6)
        pygame.draw.rect(self.fenetre, (170, 230, 180), self.bouton_recompense, width=1, border_radius=6)
        txt = pygame.font.SysFont("consolas", 11, bold=True).render(f"Recompenses • Talents {self.progression.points_talent}", True, (235, 255, 235))
        self.fenetre.blit(txt, (self.bouton_recompense.centerx - txt.get_width() // 2, self.bouton_recompense.y + 6))

    def _dessiner_map_jeu(self):
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 165))
        self.fenetre.blit(voile, (0, 0))
        rect = pygame.Rect(120, 70, largeur_ecran - 240, hauteur_ecran - 140)
        pygame.draw.rect(self.fenetre, (22, 30, 44), rect, border_radius=12)
        pygame.draw.rect(self.fenetre, (100, 130, 190), rect, width=2, border_radius=12)
        titre = pygame.font.SysFont("consolas", 24, bold=True).render("Map generale", True, (220, 230, 255))
        self.fenetre.blit(titre, (rect.centerx - titre.get_width() // 2, rect.y + 20))
        info = pygame.font.SysFont("consolas", 15).render("Partie en pause visuelle - retour possible", True, (200, 210, 225))
        self.fenetre.blit(info, (rect.centerx - info.get_width() // 2, rect.y + 58))
        pygame.draw.rect(self.fenetre, (50, 88, 130), self.bouton_retour_jeu, border_radius=8)
        pygame.draw.rect(self.fenetre, (140, 190, 235), self.bouton_retour_jeu, width=1, border_radius=8)
        txt = pygame.font.SysFont("consolas", 18, bold=True).render("Retour jeu", True, (230, 245, 255))
        self.fenetre.blit(txt, (self.bouton_retour_jeu.centerx - txt.get_width() // 2, self.bouton_retour_jeu.centery - txt.get_height() // 2))

    def _jouer_son_effet(self, type_effet):
        sons = {
            "tir": "musique/effets/tir.mp3", # ne fonctionne pas sur tous les systèmes, à cause de la polyphonie limitée de pygame.mixer. À revoir.
            "explosion": "musique/effets/explosion.mp3",
            "mur": "musique/effets/mur.mp3",
            "clic": "musique/effets/clic.mp3",
        }
        chemin = sons.get(type_effet)
        if chemin:
            self.musique.jouer_effet(chemin)

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
        # Talent alchimiste : multiplicateur sur les effets d'objets 
        mult = 1.0 + 0.5 * self.talents_appliques.get("alchimiste", 0)
        if cle_objet == "potion_mur":
            soin = int(2 * mult)
            self.points_de_vie_mur = min(vie_mur_depart + 10, self.points_de_vie_mur + soin)
            self._ajouter_effet((position_mur - 30, hauteur_ecran // 2), (80, 220, 120), 30, 0.4)
        elif cle_objet == "bourse_or":
            or_gagne = int(6 * mult)
            self.argent += or_gagne
            self._ajouter_effet((80, 48), (255, 215, 0), 20, 0.35)
        elif cle_objet == "totem_froid":
            duree = 1.2 * mult
            for ennemi in self.liste_ennemis:
                ennemi.appliquer_ralentissement(0.45, duree)

    def _appliquer_carte_marche(self, id_carte):
        """Applique l'effet d'une carte choisie dans le marché."""
        mult = 1.0 + 0.5 * self.talents_appliques.get("alchimiste", 0)
        if id_carte == "or_bonus":
            self.argent += int(20 * mult)
            self._ajouter_effet((largeur_ecran // 2, hauteur_ecran // 2), (255, 215, 0), 50, 0.4)
        elif id_carte == "soin_mur":
            soin = int(3 * mult)
            self.points_de_vie_mur = min(vie_mur_depart + 10, self.points_de_vie_mur + soin)
            self._ajouter_effet((position_mur - 20, hauteur_ecran // 2), (80, 220, 120), 40, 0.4)
        elif id_carte == "tour_gratuite":
            # Rend toutes les tours gratuites pour le prochain placement
            self.couts_tours = {k: 0 for k in self.couts_tours}
        elif id_carte == "cadence_bonus":
            # Améliore la cadence de toutes les tours de 15%
            for tour in self.liste_tours:
                tour.cadence = max(0.1, tour.cadence * 0.85)
        elif id_carte == "portee_bonus":
            # +20 portée sur toutes les tours existantes
            bonus = int(20 * mult)
            for tour in self.liste_tours:
                tour.portee += bonus
            self._bonus_portee_cartes = bonus  # aussi pour les tours futures
        elif id_carte == "xp_bonus":
            xp = int(25 * mult)
            self.progression.gagner_xp(xp)
        elif id_carte == "argent_double":
            # Les primes sont doublées pendant la prochaine vague
            self._primes_doubles_vague = True
        elif id_carte == "gel_global":
            duree = 2.0 * mult
            for ennemi in self.liste_ennemis:
                ennemi.appliquer_ralentissement(0.3, duree)

    def _ajouter_particules_mort(self, x, y, couleur):
        """5 éclats colorés qui explosent à la mort d'un ennemi."""
        import random as _rand
        # Particule centrale claire
        self._ajouter_effet((x, y), (255, 255, 200), 18, 0.3)
        # 4 éclats dans des directions aléatoires
        for _ in range(4):
            dx = _rand.randint(-30, 30)
            dy = _rand.randint(-30, 30)
            taille = _rand.randint(6, 14)
            self._ajouter_effet((x + dx, y + dy), couleur, taille, 0.25)
        # Anneau extérieur de la couleur du mob
        self._ajouter_effet((x, y), couleur, 28, 0.2)

    def _dessiner_ecran_defaite(self):
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 170))
        self.fenetre.blit(voile, (0, 0))
        rect = pygame.Rect(largeur_ecran // 2 - 230, hauteur_ecran // 2 - 120, 460, 220)
        pygame.draw.rect(self.fenetre, (30, 24, 30), rect, border_radius=12)
        pygame.draw.rect(self.fenetre, (180, 90, 100), rect, width=2, border_radius=12)
        titre = pygame.font.SysFont("consolas", 36, bold=True).render("Vous avez perdu !", True, (255, 190, 190))
        self.fenetre.blit(titre, (rect.centerx - titre.get_width() // 2, rect.y + 24))
        txt = pygame.font.SysFont("consolas", 16).render("Choisissez une action :", True, (230, 220, 220))
        self.fenetre.blit(txt, (rect.centerx - txt.get_width() // 2, rect.y + 82))
        pygame.draw.rect(self.fenetre, (80, 120, 70), self.bouton_rejouer_payant, border_radius=8)
        pygame.draw.rect(self.fenetre, (150, 200, 130), self.bouton_rejouer_payant, width=1, border_radius=8)
        pygame.draw.rect(self.fenetre, (100, 70, 70), self.bouton_recommencer, border_radius=8)
        pygame.draw.rect(self.fenetre, (190, 130, 130), self.bouton_recommencer, width=1, border_radius=8)
        t1 = pygame.font.SysFont("consolas", 16, bold=True).render("Payer 200 pour rejouer", True, (240, 255, 240))
        t2 = pygame.font.SysFont("consolas", 16, bold=True).render("Recommencer", True, (255, 235, 235))
        self.fenetre.blit(t1, (self.bouton_rejouer_payant.centerx - t1.get_width() // 2, self.bouton_rejouer_payant.y + 12))
        self.fenetre.blit(t2, (self.bouton_recommencer.centerx - t2.get_width() // 2, self.bouton_recommencer.y + 12))

    def _dessiner_ecran_echec_vague(self):
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 170))
        self.fenetre.blit(voile, (0, 0))
        rect = pygame.Rect(largeur_ecran // 2 - 280, hauteur_ecran // 2 - 120, 560, 220)
        pygame.draw.rect(self.fenetre, (35, 30, 30), rect, border_radius=12)
        pygame.draw.rect(self.fenetre, (190, 120, 90), rect, width=2, border_radius=12)
        titre = pygame.font.SysFont("consolas", 24, bold=True).render("Vous n'avez pas reussi a finir cette vague", True, (255, 210, 180))
        self.fenetre.blit(titre, (rect.centerx - titre.get_width() // 2, rect.y + 30))
        pygame.draw.rect(self.fenetre, (90, 120, 70), self.bouton_payer_passer, border_radius=8)
        pygame.draw.rect(self.fenetre, (170, 220, 140), self.bouton_payer_passer, width=1, border_radius=8)
        pygame.draw.rect(self.fenetre, (90, 70, 70), self.bouton_relancer_vague, border_radius=8)
        pygame.draw.rect(self.fenetre, (200, 150, 150), self.bouton_relancer_vague, width=1, border_radius=8)
        t1 = pygame.font.SysFont("consolas", 16, bold=True).render("Payer 100 pour passer", True, (240, 255, 240))
        t2 = pygame.font.SysFont("consolas", 16, bold=True).render("Relancer la vague", True, (255, 235, 235))
        self.fenetre.blit(t1, (self.bouton_payer_passer.centerx - t1.get_width() // 2, self.bouton_payer_passer.y + 12))
        self.fenetre.blit(t2, (self.bouton_relancer_vague.centerx - t2.get_width() // 2, self.bouton_relancer_vague.y + 12))

    def _dessiner_ecran_defaite(self):
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 170))
        self.fenetre.blit(voile, (0, 0))
        rect = pygame.Rect(largeur_ecran // 2 - 230, hauteur_ecran // 2 - 120, 460, 220)
        pygame.draw.rect(self.fenetre, (30, 24, 30), rect, border_radius=12)
        pygame.draw.rect(self.fenetre, (180, 90, 100), rect, width=2, border_radius=12)
        titre = pygame.font.SysFont("consolas", 36, bold=True).render("Vous avez perdu !", True, (255, 190, 190))
        self.fenetre.blit(titre, (rect.centerx - titre.get_width() // 2, rect.y + 24))
        txt = pygame.font.SysFont("consolas", 16).render("Choisissez une action :", True, (230, 220, 220))
        self.fenetre.blit(txt, (rect.centerx - txt.get_width() // 2, rect.y + 82))
        pygame.draw.rect(self.fenetre, (80, 120, 70), self.bouton_rejouer_payant, border_radius=8)
        pygame.draw.rect(self.fenetre, (150, 200, 130), self.bouton_rejouer_payant, width=1, border_radius=8)
        pygame.draw.rect(self.fenetre, (100, 70, 70), self.bouton_recommencer, border_radius=8)
        pygame.draw.rect(self.fenetre, (190, 130, 130), self.bouton_recommencer, width=1, border_radius=8)
        t1 = pygame.font.SysFont("consolas", 16, bold=True).render("Payer 200 pour rejouer", True, (240, 255, 240))
        t2 = pygame.font.SysFont("consolas", 16, bold=True).render("Recommencer", True, (255, 235, 235))
        self.fenetre.blit(t1, (self.bouton_rejouer_payant.centerx - t1.get_width() // 2, self.bouton_rejouer_payant.y + 12))
        self.fenetre.blit(t2, (self.bouton_recommencer.centerx - t2.get_width() // 2, self.bouton_recommencer.y + 12))

    def _dessiner_ecran_echec_vague(self):
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 170))
        self.fenetre.blit(voile, (0, 0))
        rect = pygame.Rect(largeur_ecran // 2 - 280, hauteur_ecran // 2 - 120, 560, 220)
        pygame.draw.rect(self.fenetre, (35, 30, 30), rect, border_radius=12)
        pygame.draw.rect(self.fenetre, (190, 120, 90), rect, width=2, border_radius=12)
        titre = pygame.font.SysFont("consolas", 24, bold=True).render("Vous n'avez pas réussi a finir cette vague", True, (255, 210, 180))
        self.fenetre.blit(titre, (rect.centerx - titre.get_width() // 2, rect.y + 30))
        pygame.draw.rect(self.fenetre, (90, 120, 70), self.bouton_payer_passer, border_radius=8)
        pygame.draw.rect(self.fenetre, (170, 220, 140), self.bouton_payer_passer, width=1, border_radius=8)
        pygame.draw.rect(self.fenetre, (90, 70, 70), self.bouton_relancer_vague, border_radius=8)
        pygame.draw.rect(self.fenetre, (200, 150, 150), self.bouton_relancer_vague, width=1, border_radius=8)
        t1 = pygame.font.SysFont("consolas", 16, bold=True).render("Payer 100 pour passer", True, (240, 255, 240))
        t2 = pygame.font.SysFont("consolas", 16, bold=True).render("Relancer la vague", True, (255, 235, 235))
        self.fenetre.blit(t1, (self.bouton_payer_passer.centerx - t1.get_width() // 2, self.bouton_payer_passer.y + 12))
        self.fenetre.blit(t2, (self.bouton_relancer_vague.centerx - t2.get_width() // 2, self.bouton_relancer_vague.y + 12))