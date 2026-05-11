"""
A quoi sert le fichier : Ce fichier contient tous les éléments d'interface utilisateur de base du jeu. Il définit la classe Bouton pour créer des boutons interactifs, la classe AffichageXP pour gérer l'affichage de l'expérience et des niveaux, et la classe PanneauTelephone qui simule un téléphone avec des applications. Ces composants sont utilisés partout dans le jeu pour créer des interfaces interactives et responsives.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from setting import largeur_ecran, hauteur_ecran, couleur_bouton, couleur_bouton_survol


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, taille_police=20):
        """
        A quoi sert la fonction : Crée un nouveau bouton interactif avec sa position, sa taille et son texte.
        Entrée : x (position horizontale du bouton), y (position verticale du bouton), largeur (largeur du bouton), hauteur (hauteur du bouton), texte (texte affiché sur le bouton), taille_police (taille de la police du texte).
        Sortie : Initialise un objet bouton prêt à être utilisé dans l'interface.
        """
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.police = pygame.font.SysFont("consolas", taille_police)

    def dessiner(self, fenetre, couleur_fond=None, couleur_texte=(255, 255, 255)):
        """
        A quoi sert la fonction : Dessine le bouton à l'écran avec un effet de survol et le texte centré.
        Entrée : fenetre (la surface où dessiner le bouton), couleur_fond (couleur de fond personnalisée optionnelle), couleur_texte (couleur du texte optionnelle).
        Sortie : Dessine le bouton sur la fenêtre avec les couleurs appropriées.
        """
        position_souris = pygame.mouse.get_pos()
        if couleur_fond is None:
            couleur = couleur_bouton_survol if self.rect.collidepoint(position_souris) else couleur_bouton
        else:
            couleur = couleur_fond
        pygame.draw.rect(fenetre, couleur, self.rect, border_radius=5)
        surface_texte = self.police.render(self.texte, True, couleur_texte)
        fenetre.blit(surface_texte, (self.rect.centerx - surface_texte.get_width() // 2, self.rect.centery - surface_texte.get_height() // 2))


class AffichageXP:
    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.police_niveau = pygame.font.SysFont("consolas", 18, bold=True)
        self.police_xp = pygame.font.SysFont("consolas", 13)
        self.police_message = pygame.font.SysFont("consolas", 22, bold=True)

    def dessiner(self, fenetre, progression):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre, progression.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        largeur_barre = 180
        hauteur_barre = 14
        barre_x = largeur_ecran - largeur_barre - 20
        barre_y = 20
        pygame.draw.rect(fenetre, (40, 40, 50), (barre_x, barre_y, largeur_barre, hauteur_barre), border_radius=6)
        largeur_remplie = int(largeur_barre * progression.ratio_xp())
        if largeur_remplie > 0:
            pygame.draw.rect(fenetre, (80, 180, 240), (barre_x, barre_y, largeur_remplie, hauteur_barre), border_radius=6)
        pygame.draw.rect(fenetre, (100, 120, 160), (barre_x, barre_y, largeur_barre, hauteur_barre), width=1, border_radius=6)
        surface_niveau = self.police_niveau.render(f"Niv. {progression.niveau}", True, (220, 220, 255))
        fenetre.blit(surface_niveau, (barre_x - surface_niveau.get_width() - 8, barre_y - 2))
        surface_xp = self.police_xp.render(f"{progression.xp_actuelle} / {progression.xp_necessaire} XP", True, (160, 180, 200))
        fenetre.blit(surface_xp, (barre_x + largeur_barre // 2 - surface_xp.get_width() // 2, barre_y + hauteur_barre + 2))
        if progression.message_niveau_up:
            surface_msg = self.police_message.render(f"⬆ {progression.message_niveau_up}", True, (255, 230, 50))
            fenetre.blit(surface_msg, (largeur_ecran // 2 - surface_msg.get_width() // 2, 70))


class PanneauTelephone:
    noms_boutons = ["Tourelle", "Info", "Objets", "Competence", "Succes", "New vague", "Parametre", "Map", "Scores"]

    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.largeur = 210
        self.hauteur = 360  # Hauteur augmentée pour mieux aligner les icônes sur l'image du téléphone
        self.taille_icone = 52
        self.taille_zone_clic = 46
        self.marge = 12
        self.x = largeur_ecran - self.largeur - 14
        self.y = hauteur_ecran - self.hauteur - 14
        self.ouvert = False
        self.bouton_principal = pygame.Rect(self.x + 70, self.y + self.hauteur - 44, 70, 32)
        self.liste_boutons = []
        self.image_telephone = None
        if pygame.image.get_extended():
            for chemin in ["telephone.png", "image/telephone.png"]:
                try:
                    image_brute = pygame.image.load(chemin).convert_alpha()
                    # On recadre l'image sur la zone non-transparente (le téléphone réel),
                    # car certains fichiers contiennent une grande toile autour.
                    masque = pygame.mask.from_surface(image_brute)
                    zones = masque.get_bounding_rects()
                    if zones:
                        zone = zones[0]
                        self.image_telephone = image_brute.subsurface(zone).copy()
                    else:
                        self.image_telephone = image_brute
                    break
                except Exception:
                    self.image_telephone = None
        self._creer_grille_boutons()

    def _creer_grille_boutons(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute creer grille boutons.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.liste_boutons = []
        colonnes = 3
        # On décale de 84px depuis le haut du téléphone pour que les icônes invisibles
        # correspondent bien à l'emplacement des icônes sur l'image du téléphone.
        decalage_haut = 104
        for i, nom in enumerate(self.noms_boutons):
            col = i % colonnes
            lig = i // colonnes
            bx = self.x + 16 + col * (self.taille_icone + self.marge)

            by = self.y + decalage_haut + lig * (self.taille_icone + 28)
            if lig == 0:
                by += 25  
            
            # Zone invisible reduite pour mieux correspondre à la taille des icônes sur l'image du téléphone
            self.liste_boutons.append((nom, pygame.Rect(bx, by, self.taille_zone_clic, self.taille_zone_clic)))

    def gerer_clic(self, position_clic):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : position_clic.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if self.bouton_principal.collidepoint(position_clic):
            self.ouvert = not self.ouvert
            return None
        if self.ouvert:
            for nom, rect in self.liste_boutons:
                if rect.collidepoint(position_clic):
                    return nom
        return None

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        hauteur_coque = self.hauteur if self.ouvert else 70
        y_coque = self.y if self.ouvert else self.y + self.hauteur - 70
        coque = pygame.Rect(self.x, y_coque, self.largeur, hauteur_coque)
        image_active = self.image_telephone is not None and self.ouvert
        if image_active:
            image = pygame.transform.smoothscale(self.image_telephone, (self.largeur, self.hauteur))
            fenetre.blit(image, (self.x, self.y))
        else:
            pygame.draw.rect(fenetre, (12, 14, 20), coque, border_radius=18)
            pygame.draw.rect(fenetre, (70, 88, 125), coque, width=2, border_radius=18)
        pygame.draw.circle(fenetre, (30, 38, 55), (coque.centerx, coque.y + 10), 4)
        if self.ouvert:
            if not image_active:
                police_icone = pygame.font.SysFont("consolas", 17, bold=True)
                police_nom = pygame.font.SysFont("consolas", 11)
                for nom, rect in self.liste_boutons:
                    survol = rect.collidepoint(pygame.mouse.get_pos())
                    pygame.draw.rect(fenetre, (62, 92, 140) if survol else (40, 60, 88), rect, border_radius=13)
                    pygame.draw.rect(fenetre, (120, 160, 220), rect, width=1, border_radius=13)
                    abreviation = nom[0].upper() if nom else "?"
                    if nom == "New vague":
                        abreviation = "V"
                    if nom == "Parametre":
                        abreviation = "P"
                    if nom == "Map":
                        abreviation = "M"
                    if nom == "Scores":
                        abreviation = "S"
                    texte_icone = police_icone.render(abreviation, True, (235, 245, 255))
                    fenetre.blit(texte_icone, (rect.centerx - texte_icone.get_width() // 2, rect.centery - texte_icone.get_height() // 2))
                    texte_nom = police_nom.render(nom, True, (210, 225, 250))
                    fenetre.blit(texte_nom, (rect.centerx - texte_nom.get_width() // 2, rect.bottom + 4))

        if not image_active:
            pygame.draw.rect(fenetre, (42, 84, 110), self.bouton_principal, border_radius=10)
            pygame.draw.rect(fenetre, (120, 180, 225), self.bouton_principal, width=1, border_radius=10)
            texte_bouton = "FERMER" if self.ouvert else "OUVRIR"
            texte_bouton = pygame.font.SysFont("consolas", 12, bold=True).render(texte_bouton, True, (220, 245, 255))
            fenetre.blit(texte_bouton, (self.bouton_principal.centerx - texte_bouton.get_width() // 2, self.bouton_principal.centery - texte_bouton.get_height() // 2))
