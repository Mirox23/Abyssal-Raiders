import pygame
from setting import largeur_ecran, hauteur_ecran, couleur_bouton, couleur_bouton_survol


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, taille_police=20):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.police = pygame.font.SysFont("consolas", taille_police)

    def dessiner(self, fenetre, couleur_fond=None, couleur_texte=(255, 255, 255)):
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
        self.police_niveau = pygame.font.SysFont("consolas", 18, bold=True)
        self.police_xp = pygame.font.SysFont("consolas", 13)
        self.police_message = pygame.font.SysFont("consolas", 22, bold=True)

    def dessiner(self, fenetre, progression):
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
    noms_boutons = ["Tourelle", "Info", "Objets", "Competence", "Achèvement", "New vague", "Parametre", "Map"]

    def __init__(self):
        self.largeur = 210
        self.hauteur = 250
        self.taille_icone = 52
        self.marge = 12
        self.x = largeur_ecran - self.largeur - 14
        self.y = hauteur_ecran - self.hauteur - 14
        self.ouvert = False
        self.bouton_principal = pygame.Rect(self.x + 70, self.y + self.hauteur - 44, 70, 32)
        self.liste_boutons = []
        self._creer_grille_boutons()

    def _creer_grille_boutons(self):
        self.liste_boutons = []
        colonnes = 3
        for i, nom in enumerate(self.noms_boutons):
            col = i % colonnes 
            lig = i // colonnes
            bx = self.x + 16 + col * (self.taille_icone + self.marge)
            by = self.y + 20 + lig * (self.taille_icone + 28)
            self.liste_boutons.append((nom, pygame.Rect(bx, by, self.taille_icone, self.taille_icone)))

    def gerer_clic(self, position_clic):
        if self.bouton_principal.collidepoint(position_clic):
            self.ouvert = not self.ouvert
            return None
        if self.ouvert:
            for nom, rect in self.liste_boutons:
                if rect.collidepoint(position_clic):
                    return nom
        return None

    def dessiner(self, fenetre):
        coque = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)
        pygame.draw.rect(fenetre, (12, 14, 20), coque, border_radius=18)
        pygame.draw.rect(fenetre, (70, 88, 125), coque, width=2, border_radius=18)
        pygame.draw.circle(fenetre, (30, 38, 55), (coque.centerx, coque.y + 10), 4)
        if self.ouvert:
            police_icone = pygame.font.SysFont("consolas", 17, bold=True)
            police_nom = pygame.font.SysFont("consolas", 11)
            for nom, rect in self.liste_boutons:
                survol = rect.collidepoint(pygame.mouse.get_pos())
                pygame.draw.rect(fenetre, (62, 92, 140) if survol else (40, 60, 88), rect, border_radius=13)
                pygame.draw.rect(fenetre, (120, 160, 220), rect, width=1, border_radius=13)
                abrev = nom[0].upper() if nom else "?"
                if nom == "New vague":
                    abreviation = "V"
                if nom == "Parametre":
                    abreviation = "P"
                if nom == "Map":
                    abreviation = "M"
                texte_icone = police_icone.render(abreviation, True, (235, 245, 255))
                fenetre.blit(texte_icone, (rect.centerx - texte_icone.get_width() // 2, rect.centery - texte_icone.get_height() // 2))
                texte_nom = police_nom.render(nom, True, (210, 225, 250))
                fenetre.blit(texte_nom, (rect.centerx - texte_nom.get_width() // 2, rect.bottom + 4))

        pygame.draw.rect(fenetre, (42, 84, 110), self.bouton_principal, border_radius=10)
        pygame.draw.rect(fenetre, (120, 180, 225), self.bouton_principal, width=1, border_radius=10)
        texte_bouton = pygame.font.SysFont("consolas", 12, bold=True).render("APPLIS", True, (220, 245, 255))
        fenetre.blit(texte_bouton, (self.bouton_principal.centerx - texte_bouton.get_width() // 2, self.bouton_principal.centery - texte_bouton.get_height() // 2))

