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
    noms_boutons = ["Tourelle", "Info", "Objets", "Competence", "Achèvement", "New vague", "Parametre"]

    def __init__(self):
        self.largeur = 190
        self.hauteur_bouton = 40
        self.marge = 7
        self.hauteur_ferme = 46
        self.x = largeur_ecran - 210
        self.y = hauteur_ecran - 58
        self.ouvert = False
        self.bouton_principal = Bouton(self.x, self.y, self.largeur, self.hauteur_ferme, "Telephone")
        self.liste_boutons = []
        nombre_boutons = len(self.noms_boutons)
        for indice, nom in enumerate(self.noms_boutons):
            position_depuis_bas = nombre_boutons - indice
            decalage = position_depuis_bas * (self.hauteur_bouton + self.marge)
            self.liste_boutons.append(Bouton(self.x, self.y - decalage, self.largeur, self.hauteur_bouton, nom))

    def gerer_clic(self, position_clic):
        if self.bouton_principal.rect.collidepoint(position_clic):
            self.ouvert = not self.ouvert
            return None
        if self.ouvert:
            for bouton in self.liste_boutons:
                if bouton.rect.collidepoint(position_clic):
                    return bouton.texte
        return None

    def dessiner(self, fenetre):
        hauteur_coque = self.hauteur_ferme + 14
        if self.ouvert:
            hauteur_coque = len(self.noms_boutons) * (self.hauteur_bouton + self.marge) + self.hauteur_ferme + 20
        coque = pygame.Rect(self.x - 10, self.y + self.hauteur_ferme - hauteur_coque + 8, self.largeur + 20, hauteur_coque)
        pygame.draw.rect(fenetre, (12, 14, 20), coque, border_radius=18)
        pygame.draw.rect(fenetre, (70, 88, 125), coque, width=2, border_radius=18)
        if self.ouvert:
            hauteur_panneau = len(self.noms_boutons) * (self.hauteur_bouton + self.marge) + self.marge
            rect_fond = pygame.Rect(self.x - 4, self.y - hauteur_panneau, self.largeur + 8, hauteur_panneau)
            pygame.draw.rect(fenetre, (28, 35, 48), rect_fond, border_radius=10)
            pygame.draw.rect(fenetre, (90, 120, 170), rect_fond, width=2, border_radius=10)
            for bouton in self.liste_boutons:
                bouton.dessiner(fenetre, couleur_fond=(40, 60, 88), couleur_texte=(225, 235, 255))
        self.bouton_principal.dessiner(fenetre, couleur_fond=(42, 84, 110), couleur_texte=(220, 245, 255))

