from setting import (
    niveau_joueur_depart,
    xp_par_kill,
    xp_par_vague_base,
    xp_pour_niveau_suivant_base,
)


class Progression:
    """Gère le niveau, l'XP et les points de talent du joueur.
    Le niveau monte à l'infini — il ne se remet jamais à zéro en cours de partie.
    À chaque montée de niveau, le joueur gagne 1 point de talent.
    """

    def __init__(self):
        self.niveau = niveau_joueur_depart
        self.xp_actuelle = 0
        self.xp_necessaire = xp_pour_niveau_suivant_base
        self.message_niveau_up = ""
        self.minuterie_message = 0.0
        self.points_talent = 0
        # Petits bonus permanents gardés quand l'arbre à talents se reset
        self.bonus_degats_permanent = 0   # +degats compétences conservé entre resets
        self.bonus_portee_permanent = 0   # +portée conservée entre resets

    def xp_necessaire_pour(self, niv):
        """XP requise pour passer du niveau niv au suivant. Ça monte progressivement."""
        return xp_pour_niveau_suivant_base + (niv - 1) * 10

    def gagner_xp(self, quantite):
        """Ajoute de l'XP et gère les montées de niveau à l'infini."""
        self.xp_actuelle += quantite
        messages = []

        # Boucle infinie : on monte de niveau tant qu'on a assez d'XP
        while self.xp_actuelle >= self.xp_necessaire:
            self.xp_actuelle -= self.xp_necessaire
            self.niveau += 1
            self.xp_necessaire = self.xp_necessaire_pour(self.niveau)
            self.points_talent += 1
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

    def appliquer_bonus_niveau_precedent(self, niv_avant_reset):
        """
        Appelé par game.py quand l'arbre à talents se reset (passage de niveau de jeu).
        On garde un tout petit avantage basé sur le niveau atteint avant le reset.
        """
        self.bonus_degats_permanent += niv_avant_reset // 3   # +1 tous les 3 niveaux
        self.bonus_portee_permanent += niv_avant_reset // 4   # +1 tous les 4 niveaux