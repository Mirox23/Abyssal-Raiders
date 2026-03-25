import pygame
from setting import largeur_ecran, hauteur_ecran


class Menu:
    """Menu principal minimaliste : Jouer / Quitter."""

    FOND        = (14, 22, 18)
    TITRE_COL   = (210, 140, 35)
    SOUS_COL    = (90, 110, 95)
    BTN_NORMAL  = (38, 70, 48)
    BTN_SURVOL  = (60, 110, 72)
    BTN_TEXTE   = (220, 235, 220)
    SEPARATEUR  = (50, 80, 55)

    def __init__(self, ecran):
        self.ecran = ecran
        self.police_titre    = pygame.font.SysFont("consolas", 52, bold=True)
        self.police_sous     = pygame.font.SysFont("consolas", 15)
        self.police_bouton   = pygame.font.SysFont("consolas", 24, bold=True)

        cx = largeur_ecran // 2

        self.boutons = [
            {"texte": "Jouer",   "rect": pygame.Rect(cx - 110, 290, 220, 54), "action": "jouer"},
            {"texte": "Quitter", "rect": pygame.Rect(cx - 110, 365, 220, 54), "action": "quitter"},
        ]

        # animation pulsation du titre
        self._tick = 0.0

    def gerer_evenement(self, evenement):
        """Retourne 'jouer', 'quitter', ou None."""
        if evenement.type != pygame.MOUSEBUTTONDOWN:
            return None
        for b in self.boutons:
            if b["rect"].collidepoint(evenement.pos):
                return b["action"]
        return None

    def mise_a_jour(self, dt):
        self._tick += dt

    def dessiner(self):
        self.ecran.fill(self.FOND)

        # grille décorative légère
        for x in range(0, largeur_ecran, 60):
            pygame.draw.line(self.ecran, (20, 32, 24), (x, 0), (x, hauteur_ecran))
        for y in range(0, hauteur_ecran, 60):
            pygame.draw.line(self.ecran, (20, 32, 24), (0, y), (largeur_ecran, y))

        # titre avec légère pulsation de luminosité 
        import math
        pulse = int(10 * math.sin(self._tick * 2.0))
        r = min(255, self.TITRE_COL[0] + pulse)
        g = min(255, self.TITRE_COL[1] + pulse)
        b = min(255, self.TITRE_COL[2])
        surf_titre = self.police_titre.render("ABYSSAL RAIDERS", True, (r, g, b))
        self.ecran.blit(surf_titre, (largeur_ecran // 2 - surf_titre.get_width() // 2, 140))

        # sous-titre 
        surf_sous = self.police_sous.render("~ Un tower defense démoniaque ~", True, self.SOUS_COL)
        self.ecran.blit(surf_sous, (largeur_ecran // 2 - surf_sous.get_width() // 2, 205))

        # séparateur 
        sep_y = 255
        pygame.draw.line(self.ecran, self.SEPARATEUR,
                         (largeur_ecran // 2 - 120, sep_y),
                         (largeur_ecran // 2 + 120, sep_y), 1)

        # boutons 
        pos_souris = pygame.mouse.get_pos()
        for b in self.boutons:
            survol  = b["rect"].collidepoint(pos_souris)
            couleur = self.BTN_SURVOL if survol else self.BTN_NORMAL

            # ombre portée
            ombre = b["rect"].move(3, 3)
            pygame.draw.rect(self.ecran, (8, 14, 10), ombre, border_radius=6)

            pygame.draw.rect(self.ecran, couleur, b["rect"], border_radius=6)

            # contour discret
            pygame.draw.rect(self.ecran, self.SEPARATEUR, b["rect"], width=1, border_radius=6)

            surf_txt = self.police_bouton.render(b["texte"], True, self.BTN_TEXTE)
            tx = b["rect"].x + (b["rect"].width  - surf_txt.get_width())  // 2
            ty = b["rect"].y + (b["rect"].height - surf_txt.get_height()) // 2
            self.ecran.blit(surf_txt, (tx, ty))

        # version en bas
        surf_ver = self.police_sous.render("v0.1", True, (45, 60, 48))
        self.ecran.blit(surf_ver, (largeur_ecran - surf_ver.get_width() - 12,
                                   hauteur_ecran - surf_ver.get_height() - 8))