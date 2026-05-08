"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie progression du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

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
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
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
        """
        Explication de ce que fais la fonction : Cette fonction exécute xp necessaire pour.
        Les entrées : niv.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        return xp_pour_niveau_suivant_base + (niv - 1) * 10

    def gagner_xp(self, quantite):
        """
        Explication de ce que fais la fonction : Cette fonction exécute gagner xp.
        Les entrées : quantite.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
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
        """
        Explication de ce que fais la fonction : Cette fonction exécute xp pour kill.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        return xp_par_kill

    def xp_pour_vague(self, numero_vague):
        """
        Explication de ce que fais la fonction : Cette fonction exécute xp pour vague.
        Les entrées : numero_vague.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        return xp_par_vague_base * numero_vague

    def mettre_a_jour(self, delta_temps):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour mettre a jour pendant la partie.
        Les entrées : delta_temps.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if self.minuterie_message > 0:
            self.minuterie_message -= delta_temps
            if self.minuterie_message <= 0:
                self.message_niveau_up = ""

    def ratio_xp(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ratio xp.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if self.xp_necessaire == 0:
            return 1.0
        return min(1.0, self.xp_actuelle / self.xp_necessaire)

    def appliquer_bonus_niveau_precedent(self, niv_avant_reset):
        """
        Explication de ce que fais la fonction : Cette fonction exécute appliquer bonus niveau precedent.
        Les entrées : niv_avant_reset.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.bonus_degats_permanent += niv_avant_reset // 3   # +1 tous les 3 niveaux
        self.bonus_portee_permanent += niv_avant_reset // 4   # +1 tous les 4 niveaux
