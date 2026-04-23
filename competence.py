import pygame


class GestionnaireCompetences:
    def __init__(self):
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
        for donnees in self.competences.values():
            if donnees["cooldown"] > 0:
                donnees["cooldown"] = max(0.0, donnees["cooldown"] - delta_temps)
            if "duree_restante" in donnees and donnees["duree_restante"] > 0:
                donnees["duree_restante"] = max(0.0, donnees["duree_restante"] - delta_temps)

    def peut_activer(self, cle_competence, argent_joueur):
        donnees = self.competences[cle_competence]
        return donnees["cooldown"] <= 0 and argent_joueur >= donnees["cout"]

    def activer(self, cle_competence):
        donnees = self.competences[cle_competence]
        donnees["cooldown"] = donnees["cooldown_max"]
        if "duree" in donnees:
            donnees["duree_restante"] = donnees["duree"]

    def obtenir_competence_par_touche(self, touche):
        for cle, donnees in self.competences.items():
            if donnees["touche"] == touche:
                return cle
        return None

    def buff_actif(self):
        return self.competences["buff_tours"]["duree_restante"] > 0
