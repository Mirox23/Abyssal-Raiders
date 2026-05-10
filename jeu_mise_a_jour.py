"""
Qu'est-ce que le fichier gère : Ce fichier gère la mise à jour du jeu.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import math
import pygame


class JeuMiseAJour:
    """
    Classe qui gère la mise à jour du jeu.
    Séparée de la classe principale Jeu pour respecter la limite de 300 lignes.
    """
    
    def __init__(self, jeu_instance):
        """
        Explication de ce que fais la fonction : Cette fonction initialise la mise à jour du jeu.
        Les entrées : jeu_instance.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.jeu = jeu_instance
        self._alarme_clignotement = 0.0
        self._timer_message_fidelite = 0.0
        self._timer_message_victoire = 0.0
        self._shake_timer = 0.0
        self._shake_amplitude = 0
        self._shake_offset = (0, 0)
        
    def mettre_a_jour(self, delta_temps):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour tous les éléments du jeu.
        Les entrées : delta_temps.
        Le résultat : Met à jour l'état du jeu.
        """
        if self.jeu.est_mort or self.jeu.echec_vague:
            return
        
        self.jeu.progression.mettre_a_jour(delta_temps)
        self.jeu.gestionnaire_competences.mettre_a_jour(delta_temps)
        
        # Mise à jour du tutoriel
        if self.jeu.tutoriel:
            self.jeu.tutoriel.mettre_a_jour(delta_temps)
            if self.jeu.tutoriel.etape_actuelle == etape_lancer_vague and self.jeu.gestionnaire_vague.vague_en_cours:
                if self.jeu.argent >= 15 and self.jeu.liste_tours:
                    self.jeu.tutoriel.etape_actuelle = etape_ameliorer_tour
            if self.jeu.tutoriel.est_termine():
                if self.jeu.progression_monde:
                    self.jeu.progression_monde.tutoriel_termine = True
                self.jeu.tutoriel = None

        # Timers divers
        self._alarme_clignotement += delta_temps
        if self._timer_message_fidelite > 0:
            self._timer_message_fidelite = max(0.0, self._timer_message_fidelite - delta_temps)
        
        # Mise à jour du timer de victoire
        if self._timer_message_victoire > 0:
            self._timer_message_victoire -= delta_temps

        # Screen shake : décrémente et recalcule l'offset à appliquer au dessin
        if self._shake_timer > 0:
            self._shake_timer = max(0.0, self._shake_timer - delta_temps)
            amp = self._shake_amplitude
            import random as _rand
            self._shake_offset = (_rand.randint(-amp, amp), _rand.randint(-amp, amp))
        else:
            self._shake_offset = (0, 0)

        # On avance la simulation seulement quand une vague est active et qu'aucune fenêtre pause la partie.
        if not self.jeu.en_attente_lancement_vague and not self.jeu.ecran_fin_vague.visible and not self.jeu.fenetre_marche.visible:
            self.jeu.temps_vague_actuelle += delta_temps
            
            # Compter le nombre de mobs spawnés pour désactiver l'indicateur après le 4ème
            if self.jeu._indicateur_direction_actif:
                mobs_avant = len(self.jeu.liste_ennemis)
                self.jeu.gestionnaire_vague.mettre_a_jour(delta_temps, self.jeu.liste_ennemis, CHEMIN)
                mobs_apres = len(self.jeu.liste_ennemis)
                self.jeu._nombre_mobs_spawnes_indicateur += (mobs_apres - mobs_avant)
                
                # Désactiver l'indicateur après le spawn du 4ème mob
                if self.jeu._nombre_mobs_spawnes_indicateur >= 4:
                    self.jeu._indicateur_direction_actif = False
            else:
                self.jeu.gestionnaire_vague.mettre_a_jour(delta_temps, self.jeu.liste_ennemis, CHEMIN)
            
            for ennemi in self.jeu.liste_ennemis:
                if isinstance(ennemi, MobSoigneur):
                    ennemi.soigner_alentours(delta_temps, self.jeu.liste_ennemis)

            self._mettre_a_jour_vague(delta_temps)
            self._mettre_a_jour_tours(delta_temps)
            self._mettre_a_jour_effets(delta_temps)
    
    def _mettre_a_jour_vague(self, delta_temps):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour la vague.
        Les entrées : delta_temps.
        Le résultat : Met à jour les ennemis et la vague.
        """
        mobs_a_spawner_apres = []   # mobs issus de la mort du boss
        survivants = []
        for ennemi in self.jeu.liste_ennemis:
            if ennemi.vie <= 0:
                # Bonus chasseur : prime doublée sur rapides/kamikazes
                bonus_chasseur = self.jeu.talents_appliques.get("chasseur", 0)
                if isinstance(ennemi, (MobRapide, MobKamikaze)):
                    self.jeu.argent += ennemi.recompense + bonus_chasseur
                else:
                    self.jeu.argent += ennemi.recompense
                # Primes doubles si carte marché "argent_double" active
                if self.jeu._primes_doubles_vague:
                    self.jeu.argent += ennemi.recompense
                self.jeu.progression.gagner_xp(self.jeu.progression.xp_pour_kill() + ennemi.xp)
                self.jeu.mobs_tues_vague += 1
                # Particules de mort enrichies (5 éclats colorés) 
                self.jeu._ajouter_particules_mort(ennemi.x, ennemi.y, ennemi.couleur)
                # Boss : spawner 3 mobs normaux à sa mort 
                if isinstance(ennemi, MobBoss):
                    for _ in range(3):  # Le boss relâche 3 mobs de base à sa mort.
                        mobs_a_spawner_apres.append(type("_SpawnMob", (), {"classe": __import__("mobs").Mob, "pos": CHEMIN[0]})())
                continue

            if ennemi.avancer(delta_temps, CHEMIN):
                # Ennemi a atteint le mur
                if isinstance(ennemi, MobKamikaze):
                    degats = max(1, ennemi.degats_explosion - self.jeu.talents_appliques["resistance_mur"])
                elif isinstance(ennemi, MobBoss):
                    degats = max(1, ennemi.degats_mur - self.jeu.talents_appliques["resistance_mur"])
                else:
                    degats = max(1, 1 - self.jeu.talents_appliques["resistance_mur"])
                self.jeu.points_de_vie_mur -= degats
                if self.jeu.points_de_vie_mur <= 0:
                    self.jeu.points_de_vie_mur = 0
                    self.jeu.est_mort = True
                    self.jeu._jouer_son_effet("mort")
                    self.jeu.en_attente_lancement_vague = True
                    self.jeu.gestionnaire_vague.vague_en_cours = False
                    self.jeu.fenetre_marche.fermer()
                    self.jeu.ecran_fin_vague.fermer()
                    break
                if self.jeu.points_de_vie_mur <= 0:
                    self.jeu.points_de_vie_mur = 0
                    self.jeu.est_mort = True
                    self.jeu._jouer_son_effet("mort")
                    self.jeu.en_attente_lancement_vague = True
                    self.jeu.gestionnaire_vague.vague_en_cours = False
                    self.jeu.fenetre_marche.fermer()
                    self.jeu.ecran_fin_vague.fermer()
                    break
                self.jeu._ajouter_effet((position_mur, ennemi.y), (255, 120, 80), 28 + degats * 4, 0.5)
                self.jeu._ajouter_effet((position_mur, ennemi.y), (255, 220, 180), 16, 0.25)
                self.jeu._jouer_son_effet("explosion_fin")
                # Screen shake quand le mur est touché : plus fort si les dégâts sont importants
                self._shake_timer = 0.25 + degats * 0.05
                self._shake_amplitude = 4 + degats
                continue

            survivants.append(ennemi)

        # Spawn des mobs issus de la mort du boss
        import mobs as _mob_module
        for spawn in mobs_a_spawner_apres:
            survivants.append(_mob_module.Mob(CHEMIN[0]))

        self.jeu.liste_ennemis = survivants

        if self.jeu.gestionnaire_vague.vague_terminee:
            self.jeu.gestionnaire_vague.vague_terminee = False
            self.jeu._lancer_musique_continent()
            # On signale au tutoriel que la vague est finie pour passer a l'etape modification
            if self.jeu.tutoriel:
                self.jeu.tutoriel.notifier_vague_terminee()
            self.jeu._primes_doubles_vague = False   # reset effet carte
            self.jeu.en_attente_lancement_vague = True
            xp = self.jeu.progression.xp_pour_vague(self.jeu.vague_locale)
            self.jeu.progression.gagner_xp(xp)
            facteur_equilibrage = 5.0
            score_vague = int((self.jeu.temps_vague_actuelle * max(1, self.jeu.mobs_tues_vague)) / facteur_equilibrage)  # Évite un score nul si aucun mob n'est tué.
            self.jeu.score_total_partie += score_vague
            self.jeu.ecran_fin_vague.ouvrir(self.jeu.vague_locale, xp, score_vague)
            enregistrer_score(
                self.jeu.continent,
                self.jeu.niveau,
                score_vague,
                self.jeu.progression.niveau,
                numero_vague=self.jeu.vague_locale,
                temps_vague=self.jeu.temps_vague_actuelle,
                nom_joueur="Joueur",
            )
            degats_vague = max(0, self.jeu.vie_debut_vague - self.jeu.points_de_vie_mur)
            if self.jeu.vague_locale <= 3:
                if degats_vague < 3:
                    self.jeu.panneau_achevement.marquer_vague(self.jeu.continent, self.jeu.niveau, self.jeu.vague_locale)
                else:
                    self.jeu.echec_vague = True
                    self.jeu.vague_echec_numero = self.jeu.vague_locale
                    self.jeu.ecran_fin_vague.fermer()
            if self.jeu.vague_locale >= self.jeu.vague_max:
                if self.jeu.progression_monde:
                    self.jeu.progression_monde.marquer_conquis(self.jeu.continent, self.jeu.niveau)
                self.jeu.panneau_achevement.marquer_niveau_conquis(self.jeu.continent, self.jeu.niveau)
                self.jeu._jouer_son_effet("victoire")
                
                # Animation de victoire spéciale pour le niveau 8 du continent démoniaque
                if self.jeu.continent == "demoniaque" and self.jeu.niveau == 8:
                    self.jeu._lancer_animation_victoire_finale()
                
                # Enregistrer le score total dans le leaderboard local 
                enregistrer_score(self.jeu.continent, self.jeu.niveau, self.jeu.score_total_partie, self.jeu.progression.niveau)
                self.jeu.fenetre_niveau_conquis.ouvrir()
    
    def _mettre_a_jour_tours(self, delta_temps):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour les tours.
        Les entrées : delta_temps.
        Le résultat : Met à jour les tours et leurs projectiles.
        """
        # Bonus temporaire de cadence lancé par la compétence de buff.
        mult = 1.0
        if self.jeu.gestionnaire_competences.buff_actif():
            mult = self.jeu.gestionnaire_competences.competences["buff_tours"]["multiplicateur_cadence"]
        for tour in self.jeu.liste_tours:
            c0 = tour.cadence
            tour.cadence = max(0.08, c0 * mult)
            nb_projectiles_avant = len(tour.liste_projectiles)
            tour.mettre_a_jour(delta_temps, self.jeu.liste_ennemis)
            if len(tour.liste_projectiles) > nb_projectiles_avant:
                self.jeu._ajouter_effet((tour.x, tour.y), (255, 230, 120), 10, 0.12)
                if tour.type_tour == "Canonnier":
                    self.jeu._jouer_son_effet("tir")
            tour.cadence = c0
        for tour in self.jeu.liste_tours:
            if tour.type_tour == "Support":
                tour.appliquer_buff(self.jeu.liste_tours)
    
    def _mettre_a_jour_effets(self, delta_temps):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour les effets visuels.
        Les entrées : delta_temps.
        Le résultat : Met à jour les effets visuels.
        """
        restants = []
        for effet in self.jeu.effets_visuels:
            effet["temps"] -= delta_temps
            if effet["temps"] > 0:
                restants.append(effet)
        self.jeu.effets_visuels = restants
