"""
Qu'est-ce que le fichier gère : Ce fichier gère la gestion des événements du jeu.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame


class JeuEvenements:
    """
    Classe qui gère les événements du jeu.
    Séparée de la classe principale Jeu pour respecter la limite de 300 lignes.
    """
    
    def __init__(self, jeu_instance):
        """
        Explication de ce que fais la fonction : Cette fonction initialise la gestion des événements.
        Les entrées : jeu_instance.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.jeu = jeu_instance
        self.mode_placement_actif = False
        self.type_tour_a_placer = None
        self.tour_actuellement_selectionnee = None
        
    def gerer_evenements(self, evenements):
        """
        Explication de ce que fais la fonction : Cette fonction gère tous les événements du jeu.
        Les entrées : evenements.
        Le résultat : Traite les événements et retourne les actions.
        """
        for evenement in evenements:
            if evenement.type == pygame.QUIT:
                return "quitter"
            
            elif evenement.type == pygame.KEYDOWN:
                action = self._gerer_touche_clavier(evenement)
                if action:
                    return action
            
            elif evenement.type == pygame.MOUSEBUTTONDOWN:
                action = self._gerer_clic_souris(evenement)
                if action:
                    return action
        
        return None
    
    def _gerer_touche_clavier(self, evenement):
        """
        Explication de ce que fais la fonction : Cette fonction gère les touches du clavier.
        Les entrées : evenement.
        Le résultat : Retourne l'action correspondante.
        """
        if evenement.key == pygame.K_ESCAPE:
            if self.jeu.mode_placement_actif:
                self.jeu.mode_placement_actif = False
                self.jeu.type_tour_a_placer = None
                return None
            elif self.jeu.map_jeu_ouverte:
                self.jeu.map_jeu_ouverte = False
                return None
            elif self.jeu.en_attente_lancement_vague:
                self.jeu.demande_retour_map = True
                return None
            else:
                return "menu"
        
        # Compétences
        elif evenement.key == pygame.K_a and not self.jeu.en_attente_lancement_vague:
            self.jeu.gestionnaire_competences.lancer_competence("tir_puissant", self.jeu.liste_tours, self.jeu.liste_ennemis)
        elif evenement.key == pygame.K_z and not self.jeu.en_attente_lancement_vague:
            self.jeu.gestionnaire_competences.lancer_competence("pluie_bombes", self.jeu.liste_ennemis)
        elif evenement.key == pygame.K_e and not self.jeu.en_attente_lancement_vague:
            self.jeu.gestionnaire_competences.lancer_competence("buff_tours", self.jeu.liste_tours)
        elif evenement.key == pygame.K_r and not self.jeu.en_attente_lancement_vague:
            self.jeu.gestionnaire_competences.lancer_competence("ralentissement_zone", self.jeu.liste_ennemis)
        elif evenement.key == pygame.K_p:
            self.jeu._jouer_son_effet("piece")
            self.jeu.argent += 50
        
        return None
    
    def _gerer_clic_souris(self, evenement):
        """
        Explication de ce que fais la fonction : Cette fonction gère les clics de souris.
        Les entrées : evenement.
        Le résultat : Retourne l'action correspondante.
        """
        clic = evenement.pos
        
        # Gestion des fenêtres prioritaires
        if self.jeu.fenetre_niveau_conquis.visible:
            action_niveau = self.jeu.fenetre_niveau_conquis.gerer_clic(clic)
            if action_niveau == "retour_map":
                self.jeu.demande_retour_map = True
            elif action_niveau == "niveau_suivant":
                self.jeu.niveau = min(7, self.jeu.niveau + 1)  # 7 niveaux maintenant
                self.jeu.reinitialiser()
            return None
        
        if self.jeu.fenetre_recompenses.visible:
            action = self.jeu.fenetre_recompenses.gerer_clic(clic, self.jeu.progression)
            if action:
                if action[0] == "recompense":
                    self.jeu.argent += action[1]
                    self.jeu._jouer_son_effet("achat")
                elif action[0] == "competence":
                    self.jeu.gestionnaire_competences.debloquer_competence(action[1], action[2])
                    self.jeu._jouer_son_effet("debloquer")
            return None
        
        if self.jeu.fenetre_marche.visible:
            if self.jeu.fenetre_marche.gerer_clic(clic):
                self.jeu.argent += self.jeu.fenetre_marche.cout_total * 0.8  # Remboursement 80%
                self.jeu.fenetre_marche.fermer()
                self.jeu._jouer_son_effet("vente")
            return None
        
        if self.jeu.fenetre_scores.visible:
            self.jeu.fenetre_scores.fermer()
            return None
        
        if self.jeu.ecran_fin_vague.visible:
            if self.jeu.ecran_fin_vague.gerer_clic(clic):
                self.jeu.en_attente_lancement_vague = True
                self.jeu.ecran_fin_vague.fermer()
                self.jeu._jouer_son_effet("validation")
            return None
        
        # Gestion du téléphone et des panneaux
        action_tel = self.jeu.telephone.gerer_clic(clic)
        if action_tel:
            return self._gerer_action_telephone(action_tel, clic)
        
        # Gestion du placement et sélection des tours
        return self._gerer_interaction_tours(clic)
    
    def _gerer_action_telephone(self, action_tel, clic):
        """
        Explication de ce que fais la fonction : Cette fonction gère les actions du téléphone.
        Les entrées : action_tel, clic.
        Le résultat : Traite l'action du téléphone.
        """
        if action_tel == "Tourelle":
            self.jeu.mode_placement_actif = True
            self.jeu.type_tour_a_placer = None
            if self.jeu.tutoriel:
                self.jeu.tutoriel.notifier_action("telephone_tourelle_clique")
            return None
        elif action_tel == "New vague" and self.jeu.en_attente_lancement_vague:
            self.jeu.lancer_nouvelle_vague()
            if self.jeu.tutoriel:
                self.jeu.tutoriel.notifier_action("vague_lancee")
            return None
        elif action_tel == "Succes":
            self.jeu.panneau_achevement.ouvrir()
            if self.jeu.tutoriel:
                self.jeu.tutoriel.notifier_action("telephone_succes_clique")
            return None
        elif action_tel == "Info" and self.jeu.tour_actuellement_selectionnee:
            self.jeu.panneau_infos.ouvrir(self.jeu.tour_actuellement_selectionnee)
            if self.jeu.tutoriel:
                self.jeu.tutoriel.notifier_action("telephone_info_clique")
            return None
        elif action_tel == "Competence":
            self.jeu.panneau_competences.ouvrir()
            if self.jeu.tutoriel:
                self.jeu.tutoriel.notifier_action("telephone_competence_clique")
            return None
        elif action_tel == "Objets":
            self.jeu.panneau_objets.ouvrir()
            if self.jeu.tutoriel:
                self.jeu.tutoriel.notifier_action("telephone_objet_clique")
            return None
        elif action_tel == "Parametre":
            self.jeu.panneau_parametres_musique.ouvrir()
            return None
        elif action_tel == "Map":
            self.jeu.demande_retour_map = True
            return None
        elif action_tel == "Scores":
            self.jeu.fenetre_scores.ouvrir(self.jeu.continent)
            return None
        
        return None
    
    def _gerer_interaction_tours(self, clic):
        """
        Explication de ce que fais la fonction : Cette fonction gère les interactions avec les tours.
        Les entrées : clic.
        Le résultat : Traite le placement et la sélection des tours.
        """
        if not self.jeu.mode_placement_actif:
            self.jeu.tour_actuellement_selectionnee = None
            for tour in self.jeu.liste_tours:
                if ((clic[0] - tour.x) ** 2 + (clic[1] - tour.y) ** 2) ** 0.5 <= tour.taille + 4:
                    self.jeu.tour_actuellement_selectionnee = tour
                    if self.jeu.tutoriel:
                        self.jeu.tutoriel.notifier_action("tour_selectionnee")
                    break
            return None
        
        if self.jeu.mode_placement_actif and self.jeu.type_tour_a_placer is None:
            self.jeu._selectionner_tour_menu(clic)
            return None
        
        if self.jeu.mode_placement_actif and self.jeu.type_tour_a_placer:
            self.jeu._placer_tour(clic)
            return None
        
        return None
