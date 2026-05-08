"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie competence du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame


class GestionnaireCompetences:
    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.competences = {
            "tir_puissant": {
                "nom": "Tir Puissant",
                "touche": pygame.K_a,
                "cooldown_max": 5.0,
                "cooldown": 0.0,
                "cout": 6,
            },
            "pluie_bombes": {
                "nom": "Pluie de Bombes",
                "touche": pygame.K_z,
                "cooldown_max": 8.0,
                "cooldown": 0.0,
                "cout": 10,
            },
            "buff_tours": {
                "nom": "Buff de Tours",
                "touche": pygame.K_e,
                "cooldown_max": 15.0,
                "cooldown": 0.0,
                "cout": 12,
                "duree": 5.0,
                "duree_restante": 0.0,
                "multiplicateur_cadence": 0.65,
            },
            "ralentissement_zone": {
                "nom": "Ralentissement Zone",
                "touche": pygame.K_r,
                "cooldown_max": 10.0,
                "cooldown": 0.0,
                "cout": 8,
            },
        }

    def mettre_a_jour(self, delta_temps):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour mettre a jour pendant la partie.
        Les entrées : delta_temps.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        for donnees in self.competences.values():
            if donnees["cooldown"] > 0:
                donnees["cooldown"] = max(0.0, donnees["cooldown"] - delta_temps)
            if "duree_restante" in donnees and donnees["duree_restante"] > 0:
                donnees["duree_restante"] = max(0.0, donnees["duree_restante"] - delta_temps)

    def peut_activer(self, cle_competence, argent_joueur):
        """
        Explication de ce que fais la fonction : Cette fonction vérifie peut activer.
        Les entrées : cle_competence, argent_joueur.
        Le résultat : Retourne True ou False selon la condition vérifiée.
        """
        donnees = self.competences[cle_competence]
        return donnees["cooldown"] <= 0 and argent_joueur >= donnees["cout"]

    def activer(self, cle_competence):
        """
        Explication de ce que fais la fonction : Cette fonction exécute activer.
        Les entrées : cle_competence.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        donnees = self.competences[cle_competence]
        donnees["cooldown"] = donnees["cooldown_max"]
        if "duree" in donnees:
            donnees["duree_restante"] = donnees["duree"]

    def obtenir_competence_par_touche(self, touche):
        """
        Explication de ce que fais la fonction : Cette fonction récupère obtenir competence par touche.
        Les entrées : touche.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        for cle, donnees in self.competences.items():
            if donnees["touche"] == touche:
                return cle
        return None

    def buff_actif(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute buff actif.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        return self.competences["buff_tours"]["duree_restante"] > 0
