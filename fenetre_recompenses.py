"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie fenetre recompenses du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from decoration_cadre_abysse import dessiner_cadre_panneau
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

class FenetreRecompenses:
    """
    Affiche les récompenses d'or débloquées à chaque niveau.
    Les récompenses sont infinies : tous les 8 niveaux on repart sur un cycle
    avec des montants un peu plus élevés.
    """

    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.rect = pygame.Rect(200, 80, 600, 420)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.police_petite = pygame.font.SysFont("consolas", 12)
        self.bouton_fermer = Bouton(self.rect.right - 100, self.rect.y + 12, 84, 30, "Fermer", 14)
        self.niveaux_recuperes = set()   # clés = (cycle, rang) pour être infini
        self._boutons_recompenses = []

    def _calcul_recompense(self, numero_niveau_joueur):
        """
        Explication de ce que fais la fonction : Cette fonction exécute calcul recompense.
        Les entrées : numero_niveau_joueur.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        cycle = (numero_niveau_joueur - 1) // 8       # 0, 1, 2 …
        rang = (numero_niveau_joueur - 1) % 8 + 1     # 1 à 8
        base = 8 + rang * 2                            # 10 à 24 comme avant
        bonus_cycle = cycle * 4                        # +4 par cycle
        return base + bonus_cycle

    def _generer_lignes(self, niveau_joueur):
        """
        Explication de ce que fais la fonction : Cette fonction exécute generer lignes.
        Les entrées : niveau_joueur.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        debut = max(1, niveau_joueur - 2)
        lignes = []
        for i in range(7):  # 7 niveaux maintenant
            numero_niveau = debut + i
            montant = self._calcul_recompense(numero_niveau)
            lignes.append((numero_niveau, montant))
        return lignes

    def ouvrir(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = True

    def gerer_clic(self, pos_clic, progression):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : pos_clic, progression.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(pos_clic):
            self.visible = False
            return ("fermer", None)
        for niv, montant, rect in self._boutons_recompenses:
            cle = niv   # chaque niveau = clé unique infinie
            peut_recuperer = progression.niveau >= niv and cle not in self.niveaux_recuperes
            if rect.collidepoint(pos_clic) and peut_recuperer:
                self.niveaux_recuperes.add(cle)
                return ("recompense", montant)
        if self.rect.collidepoint(pos_clic):
            return ("consomme", None)
        return None

    def dessiner(self, fenetre, progression):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre, progression.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA) #SRCALPHA pour transparence
        voile.fill((0, 0, 0, 150))
        fenetre.blit(voile, (0, 0)) 

        dessiner_cadre_panneau(fenetre, self.rect)

        titre = self.police_titre.render("Récompenses de niveau", True, (238, 218, 182))
        fenetre.blit(titre, (self.rect.x + 14, self.rect.y + 14))

        sous = self.police_petite.render(
            f"Niveau joueur actuel : {progression.niveau}  |  Points talent disponibles : {progression.points_talent}",
            True, (245, 205, 140)
        )
        fenetre.blit(sous, (self.rect.x + 14, self.rect.y + 44))
        self.bouton_fermer.dessiner(fenetre)

        lignes = self._generer_lignes(progression.niveau)
        self._boutons_recompenses = []
        y = self.rect.y + 72

        for niv, montant in lignes:
            rect_btn = pygame.Rect(self.rect.x + 20, y, self.rect.width - 40, 32)
            self._boutons_recompenses.append((niv, montant, rect_btn))

            deja = niv in self.niveaux_recuperes
            peut = progression.niveau >= niv and not deja

            if deja:
                couleur = (45, 86, 58)
            elif peut:
                couleur = (22, 102, 68)
            else:
                couleur = (60, 60, 70)

            pygame.draw.rect(fenetre, couleur, rect_btn, border_radius=6)
            pygame.draw.rect(fenetre, (166, 130, 86), rect_btn, width=1, border_radius=6)

            texte = f"Niveau {niv:3}  →  +{montant} or"
            if deja:
                texte += "  ✓ récupéré"
            elif not peut:
                texte += "  (verrouillé)"

            coul_txt = (200, 210, 200) if deja else (230, 235, 230) if peut else (130, 130, 140)
            fenetre.blit(self.police_texte.render(texte, True, coul_txt), (rect_btn.x + 12, rect_btn.y + 8))
            y += 40


