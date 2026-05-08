import pygame
from decoration_cadre_abysse import dessiner_cadre_panneau
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

class PanneauObjets:
    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(235, 120, 530, 320)
        self.police_titre = pygame.font.SysFont("consolas", 24, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.bouton_fermer = Bouton(self.rect.right - 96, self.rect.y + 12, 80, 30, "Fermer", 14)
        self.boutons = []

    def ouvrir(self):
        self.visible = True

    def gerer_clic(self, pos_clic):
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(pos_clic):
            self.visible = False
            return None
        for cle, rect in self.boutons:
            if rect.collidepoint(pos_clic):
                return cle
        if self.rect.collidepoint(pos_clic):
            return "consomme"
        return None

    def dessiner(self, fenetre, inventaire_objets):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 135))
        fenetre.blit(voile, (0, 0))
        dessiner_cadre_panneau(fenetre, self.rect, sous_zones_bleues=False)
        fenetre.blit(self.police_titre.render("Objets utiles", True, (238, 218, 182)), (self.rect.x + 16, self.rect.y + 16))
        self.bouton_fermer.dessiner(fenetre)
        definitions = [
            ("potion_mur",  "Potion de planches", "Restaure +2 vie au mur"),
            ("bourse_or",   "Bourse de secours",  "Gagne +6 or"),
            ("totem_froid", "Totem de givre",      "Ralentit tous les mobs 1.2s"),
        ]
        self.boutons = []
        y = self.rect.y + 72
        for cle, nom, desc in definitions:
            qte = inventaire_objets.get(cle, 0)
            utilisable = qte > 0
            rect = pygame.Rect(self.rect.x + 20, y, self.rect.width - 40, 60)
            self.boutons.append((cle, rect))
            pygame.draw.rect(fenetre, (77, 57, 35) if utilisable else (60, 47, 38), rect, border_radius=8)
            pygame.draw.rect(fenetre, (173, 132, 82), rect, width=1, border_radius=8)
            coul_qte = (255, 240, 200) if utilisable else (180, 160, 145)
            fenetre.blit(self.police_texte.render(f"{nom} x{qte}", True, coul_qte), (rect.x + 10, rect.y + 10))
            fenetre.blit(self.police_texte.render(desc, True, (230, 210, 170)), (rect.x + 10, rect.y + 32))
            statut = "Utilisable" if utilisable else "Stock vide"
            coul_s = (125, 230, 150) if utilisable else (230, 130, 120)
            fenetre.blit(self.police_texte.render(statut, True, coul_s), (rect.right - 120, rect.y + 10))
            y += 70

