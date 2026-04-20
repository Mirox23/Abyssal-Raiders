from setting import (
    niveau_joueur_depart,
    xp_par_kill,
    xp_par_vague_base,
    xp_pour_niveau_suivant_base,
)


class Progression:
    """Gère le niveau, l'XP et les seuils de montée de niveau du joueur."""

    def __init__(self):
        self.niveau = niveau_joueur_depart
        self.xp_actuelle = 0
        self.xp_necessaire = xp_pour_niveau_suivant_base
        self.message_niveau_up = ""
        self.minuterie_message = 0.0

    def calculer_xp_necessaire(self, niveau):
        # Chaque niveau demande un peu plus d'XP que le précédent
        return xp_pour_niveau_suivant_base + (niveau - 1) * 10

    def gagner_xp(self, quantite):
        """Ajoute de l'XP et gère les montées de niveau."""
        self.xp_actuelle += quantite
        messages = []

        while self.xp_actuelle >= self.xp_necessaire:
            self.xp_actuelle -= self.xp_necessaire
            self.niveau += 1
            self.xp_necessaire = self.calculer_xp_necessaire(self.niveau)
            messages.append(f"Niveau {self.niveau} !")

        if messages:
            self.message_niveau_up = " | ".join(messages)
            self.minuterie_message = 3.0

        return messages

    def xp_pour_kill(self):
        return xp_par_kill

    def xp_pour_vague(self, numero_vague):
        return xp_par_vague_base * numero_vague

    def mettre_a_jour(self, delta_temps):
        if self.minuterie_message > 0:
            self.minuterie_message -= delta_temps
            if self.minuterie_message <= 0:
                self.message_niveau_up = ""

    def ratio_xp(self):
        """Retourne la progression XP entre 0.0 et 1.0 pour la barre."""
        if self.xp_necessaire == 0:
            return 1.0
        return min(1.0, self.xp_actuelle / self.xp_necessaire)