"""
A quoi sert le fichier : Ce fichier gère le système de compétences du jeu. Il permet de créer différentes compétences spéciales que le joueur peut utiliser pendant la partie, comme des tirs puissants, des pluies de bombes, des buffs pour les tours ou des ralentissements de zone. Il gère aussi les temps d'attente entre chaque utilisation et les coûts en argent.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame


class GestionnaireCompetences:
    # Classe qui gère toutes les compétences du jeu
    
    def __init__(self):
        """
        A quoi sert la fonction : Crée le gestionnaire de compétences et initialise toutes les compétences disponibles avec leurs caractéristiques.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Initialise correctement les attributs de l'objet.
        """
        # Dictionnaire qui contient toutes les compétences du jeu
        self.competences = {
            "tir_puissant": {
                "nom": "Tir Puissant",
                "touche": pygame.K_a,  # Touche A pour activer
                "cooldown_max": 5.0,   # Temps d'attente de 5 secondes
                "cooldown": 0.0,       # Temps d'attente actuel
                "cout": 6,            # Coûte 6 pièces d'or
            },
            "pluie_bombes": {
                "nom": "Pluie de Bombes",
                "touche": pygame.K_z,  # Touche Z pour activer
                "cooldown_max": 8.0,   # Temps d'attente de 8 secondes
                "cooldown": 0.0,       # Temps d'attente actuel
                "cout": 10,           # Coûte 10 pièces d'or
            },
            "buff_tours": {
                "nom": "Buff de Tours",
                "touche": pygame.K_e,  # Touche E pour activer
                "cooldown_max": 15.0,  # Temps d'attente de 15 secondes
                "cooldown": 0.0,        # Temps d'attente actuel
                "cout": 12,            # Coûte 12 pièces d'or
                "duree": 5.0,          # Durée du buff de 5 secondes
                "duree_restante": 0.0, # Temps restant du buff
                "multiplicateur_cadence": 0.65,  # Les tours tirent 35% plus vite
            },
            "ralentissement_zone": {
                "nom": "Ralentissement Zone",
                "touche": pygame.K_r,  # Touche R pour activer
                "cooldown_max": 10.0,  # Temps d'attente de 10 secondes
                "cooldown": 0.0,       # Temps d'attente actuel
                "cout": 8,            # Coûte 8 pièces d'or
            },
        }

    def mettre_a_jour(self, delta_temps):
        """
        A quoi sert la fonction : Met à jour les temps d'attente et les durées des compétences à chaque frame du jeu.
        Entrée : delta_temps.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Parcourt toutes les compétences pour mettre à jour leurs temps
        for donnees in self.competences.values():
            # Réduit le temps d'attente si nécessaire
            if donnees["cooldown"] > 0:
                donnees["cooldown"] = max(0.0, donnees["cooldown"] - delta_temps)
            # Réduit la durée restante pour les compétences qui ont une durée
            if "duree_restante" in donnees and donnees["duree_restante"] > 0:
                donnees["duree_restante"] = max(0.0, donnees["duree_restante"] - delta_temps)

    def peut_activer(self, cle_competence, argent_joueur):
        """
        A quoi sert la fonction : Vérifie si le joueur peut utiliser une compétence en vérifiant si elle n'est pas en attente et si le joueur a assez d'argent.
        Entrée : cle_competence, argent_joueur.
        Sortie : Retourne True ou False selon la condition vérifiée.
        """
        # Récupère les données de la compétence demandée
        donnees = self.competences[cle_competence]
        # Vérifie si le cooldown est terminé ET si le joueur a assez d'argent
        return donnees["cooldown"] <= 0 and argent_joueur >= donnees["cout"]

    def activer(self, cle_competence):
        """
        A quoi sert la fonction : Active une compétence en lançant son temps d'attente et sa durée si elle en a une.
        Entrée : cle_competence.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Récupère les données de la compétence à activer
        donnees = self.competences[cle_competence]
        # Lance le temps d'attente maximal
        donnees["cooldown"] = donnees["cooldown_max"]
        # Si la compétence a une durée, lance la durée restante
        if "duree" in donnees:
            donnees["duree_restante"] = donnees["duree"]

    def obtenir_competence_par_touche(self, touche):
        """
        A quoi sert la fonction : Trouve quelle compétence correspond à la touche pressée par le joueur.
        Entrée : touche.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Cherche la compétence qui correspond à la touche pressée
        for cle, donnees in self.competences.items():
            if donnees["touche"] == touche:
                return cle  # Retourne le nom de la compétence
        return None  # Aucune compétence trouvée pour cette touche

    def buff_actif(self):
        """
        A quoi sert la fonction : Vérifie si le buff de tours est actuellement actif dans le jeu.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Vérifie si le buff de tours a encore de la durée restante
        return self.competences["buff_tours"]["duree_restante"] > 0
