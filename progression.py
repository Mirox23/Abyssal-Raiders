"""
A quoi sert le fichier : Ce fichier gère le système de progression du joueur. Il contient la classe Progression qui gère le niveau, l'expérience (XP), les points de talent et les bonus permanents. Il calcule l'XP nécessaire pour chaque niveau, gère les montées de niveau, et distribue les points de talent. Il conserve aussi des bonus entre les réinitialisations de l'arbre de talents.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

# Importe les constantes de progression depuis les settings
from setting import (
    niveau_joueur_depart,
    xp_par_kill,
    xp_par_vague_base,
    xp_pour_niveau_suivant_base,
)


class Progression:
    # Classe qui gère le niveau, l'XP et les points de talent du joueur
    """Gère le niveau, l'XP et les points de talent du joueur.
    Le niveau monte à l'infini — il ne se remet jamais à zéro en cours de partie.
    À chaque montée de niveau, le joueur gagne 1 point de talent.
    """

    def __init__(self):
        """
        A quoi sert la fonction : Initialise les attributs de progression du joueur.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Initialise correctement les attributs de l'objet.
        """
        # Initialise les attributs de base
        self.niveau = niveau_joueur_depart  # Niveau de départ
        self.xp_actuelle = 0  # XP actuelle du joueur
        self.xp_necessaire = xp_pour_niveau_suivant_base  # XP nécessaire pour le prochain niveau
        self.message_niveau_up = ""  # Message quand on monte de niveau
        self.minuterie_message = 0.0  # Timer pour afficher le message
        self.points_talent = 0  # Points de talent disponibles
        
        # Petits bonus permanents gardés quand l'arbre à talents se reset
        self.bonus_degats_permanent = 0   # +dégâts compétences conservé entre resets
        self.bonus_portee_permanent = 0   # +portée conservée entre resets

    def xp_necessaire_pour(self, niv):
        """
        A quoi sert la fonction : Calcule l'XP nécessaire pour un niveau donné.
        Entrée : niv.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Calcule l'XP nécessaire : base + 10 par niveau au-dessus du premier
        return xp_pour_niveau_suivant_base + (niv - 1) * 10

    def gagner_xp(self, quantite):
        """
        A quoi sert la fonction : Ajoute de l'XP au joueur et gère les montées de niveau.
        Entrée : quantite.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.xp_actuelle += quantite  # Ajoute l'XP
        messages = []  # Liste des messages de montée de niveau

        # Boucle infinie : on monte de niveau tant qu'on a assez d'XP
        while self.xp_actuelle >= self.xp_necessaire:
            self.xp_actuelle -= self.xp_necessaire  # Consomme l'XP nécessaire
            self.niveau += 1  # Monte le niveau
            self.xp_necessaire = self.xp_necessaire_pour(self.niveau)  # Recalcule l'XP nécessaire
            self.points_talent += 1  # Donne 1 point de talent
            messages.append(f"Niveau {self.niveau} !")  # Ajoute le message

        # Affiche les messages de montée de niveau
        if messages:
            self.message_niveau_up = " | ".join(messages)  # Combine tous les messages
            self.minuterie_message = 3.0  # Timer d'affichage (3 secondes)

        return messages

    def xp_pour_kill(self):
        """
        A quoi sert la fonction : Retourne l'XP gagné par kill.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Retourne l'XP de base par kill (défini dans les settings)
        return xp_par_kill

    def xp_pour_vague(self, numero_vague):
        """
        A quoi sert la fonction : Calcule l'XP gagné pour une vague spécifique.
        Entrée : numero_vague.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Calcule l'XP pour la vague : base × numéro de vague
        return xp_par_vague_base * numero_vague

    def mettre_a_jour(self, delta_temps):
        """
        A quoi sert la fonction : Met à jour le timer d'affichage des messages.
        Entrée : delta_temps.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Gère le timer pour afficher/cacher les messages de montée de niveau
        if self.minuterie_message > 0:
            self.minuterie_message -= delta_temps  # Décrémente le timer
            if self.minuterie_message <= 0:
                self.message_niveau_up = ""  # Cache le message quand le timer est terminé

    def ratio_xp(self):
        """
        A quoi sert la fonction : Calcule le ratio d'XP actuel (entre 0 et 1).
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Calcule le pourcentage d'XP vers le prochain niveau
        if self.xp_necessaire == 0:
            return 1.0  # Évite la division par zéro
        return min(1.0, self.xp_actuelle / self.xp_necessaire)  # Limite à 1.0

    def appliquer_bonus_niveau_precedent(self, niv_avant_reset):
        """
        A quoi sert la fonction : Applique les bonus permanents selon le niveau avant reset.
        Entrée : niv_avant_reset.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Calcule les bonus permanents : +1 dégâts tous les 3 niveaux, +1 portée tous les 4 niveaux
        self.bonus_degats_permanent += niv_avant_reset // 3   # +1 tous les 3 niveaux
        self.bonus_portee_permanent += niv_avant_reset // 4   # +1 tous les 4 niveaux
