import pygame
from setting import largeur_ecran, hauteur_ecran, cout_amelioration, niveau_max
from ui_noyau import Bouton


class PanneauInfos:
    def __init__(self):
        self.visible = False
        self.tour_selectionnee = None
        self.police_info = pygame.font.SysFont("consolas", 18)
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)
        self.rect = pygame.Rect(largeur_ecran // 2 - 150, hauteur_ecran // 2 - 105, 300, 210)
        base_x = self.rect.x + 20
        base_y = self.rect.y + self.rect.height - 55
        self.bouton_ameliorer = Bouton(base_x, base_y, 120, 38, "Améliorer")
        self.bouton_fermer = Bouton(base_x + 140, base_y, 120, 38, "Fermer")

    def ouvrir(self, tour):
        self.tour_selectionnee = tour
        self.visible = True

    def fermer(self):
        self.visible = False
        self.tour_selectionnee = None

    def gerer_clic(self, position_clic, argent_joueur):
        if not self.visible:
            return None, argent_joueur
        if self.bouton_ameliorer.rect.collidepoint(position_clic):
            nouvel_argent = self.tour_selectionnee.ameliorer(argent_joueur)
            if nouvel_argent >= 0:
                return "ameliore", nouvel_argent
            return None, argent_joueur
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.fermer()
            return "ferme", argent_joueur
        return None, argent_joueur

    def dessiner(self, fenetre):
        if not self.visible or not self.tour_selectionnee:
            return
        tour = self.tour_selectionnee
        pygame.draw.rect(fenetre, (28, 30, 44), self.rect, border_radius=10)
        pygame.draw.rect(fenetre, (80, 90, 140), self.rect, width=2, border_radius=10)
        pos_x = self.rect.x + 16
        pos_y = self.rect.y + 12
        fenetre.blit(self.police_titre.render(f"Tour : {tour.type_tour}", True, (220, 220, 255)), (pos_x, pos_y))
        pos_y += 30
        fenetre.blit(self.police_info.render(f"Niveau  : {tour.niveau} / {niveau_max}", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24
        fenetre.blit(self.police_info.render(f"Portée  : {int(tour.portee)}", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24
        fenetre.blit(self.police_info.render(f"Cadence : {tour.cadence:.2f} s", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24
        if tour.type_tour == "Ralentissement":
            special = f"Ralenti  : {int((1 - tour.facteur_ralentissement) * 100)}% / {tour.duree_ralentissement:.1f}s"
            fenetre.blit(self.police_info.render(special, True, (100, 200, 255)), (pos_x, pos_y))
            pos_y += 24
        elif tour.type_tour == "Support":
            special = f"Rayon buff : {int(tour.rayon_buff)} / Bonus : {int(tour.bonus_cadence_buff * 100)}%"
            fenetre.blit(self.police_info.render(special, True, (255, 220, 80)), (pos_x, pos_y))
            pos_y += 24
        if tour.niveau >= niveau_max:
            surface_cout = self.police_info.render("Niveau maximum !", True, (255, 180, 50))
        else:
            surface_cout = self.police_info.render(f"Coût amélioration : {cout_amelioration} ¤", True, (130, 210, 130))
        fenetre.blit(surface_cout, (pos_x, pos_y))
        self.bouton_ameliorer.dessiner(fenetre)
        self.bouton_fermer.dessiner(fenetre)


class PanneauAchevement:
    noms_mondes = ["Pirate", "Samouraï", "Médiéval", "Démoniaque"]
    cles_mondes = ["pirate", "Samouraï", "medieval", "Démoniaque"]

    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(largeur_ecran // 2 - 340, hauteur_ecran // 2 - 230, 680, 460)
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)
        self.police_onglet = pygame.font.SysFont("consolas", 15, bold=True)
        self.police_label = pygame.font.SysFont("consolas", 13)
        self.progression = {cle: [[False] * 4 for _ in range(8)] for cle in self.cles_mondes}
        self.onglet_actif = 0
        self.bouton_fermer = Bouton(self.rect.right - 90, self.rect.y + 8, 80, 30, "Fermer", 14)
        largeur_onglet = self.rect.width // 4
        self.rects_onglets = [pygame.Rect(self.rect.x + i * largeur_onglet, self.rect.y + 48, largeur_onglet, 30) for i in range(4)]

    def ouvrir(self):
        self.visible = True

    def fermer(self):
        self.visible = False

    def gerer_clic(self, position_clic):
        if not self.visible:
            return False
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.fermer()
            return True
        for i, rect_onglet in enumerate(self.rects_onglets):
            if rect_onglet.collidepoint(position_clic):
                self.onglet_actif = i
                return True
        return self.rect.collidepoint(position_clic)

    def dessiner(self, fenetre):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 120))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (22, 24, 38), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (80, 90, 150), self.rect, width=2, border_radius=12)
        fenetre.blit(self.police_titre.render("Achèvements", True, (220, 210, 255)), (self.rect.x + 16, self.rect.y + 12))
        self.bouton_fermer.dessiner(fenetre)
        for i, (nom, rect_onglet) in enumerate(zip(self.noms_mondes, self.rects_onglets)):
            actif = i == self.onglet_actif
            pygame.draw.rect(fenetre, (60, 70, 120) if actif else (35, 38, 60), rect_onglet)
            pygame.draw.rect(fenetre, (80, 90, 140), rect_onglet, width=1)
            couleur_texte = (255, 255, 255) if actif else (150, 150, 180)
            surf = self.police_onglet.render(nom, True, couleur_texte)
            fenetre.blit(surf, (rect_onglet.centerx - surf.get_width() // 2, rect_onglet.centery - surf.get_height() // 2))
        zone_y_depart = self.rect.y + 88
        marge_gauche = self.rect.x + 30
        progression_monde = self.progression[self.cles_mondes[self.onglet_actif]]
        taille_rect_vague = 22
        espacement_vague = 6
        espacement_niveau = 10
        for v in range(4):
            x_entete = marge_gauche + 80 + v * (taille_rect_vague + espacement_vague)
            fenetre.blit(self.police_label.render(f"V{v+1}", True, (160, 160, 200)), (x_entete, zone_y_depart))
        for niv in range(8):
            y_ligne = zone_y_depart + 20 + niv * (taille_rect_vague + espacement_niveau)
            fenetre.blit(self.police_label.render(f"Niveau {niv + 1}", True, (200, 200, 200)), (marge_gauche, y_ligne + 3))
            for vague in range(4):
                x_rect = marge_gauche + 80 + vague * (taille_rect_vague + espacement_vague)
                couleur_rect = (0, 130, 0) if progression_monde[niv][vague] else (100, 100, 110)
                pygame.draw.rect(fenetre, couleur_rect, (x_rect, y_ligne, taille_rect_vague, taille_rect_vague), border_radius=3)
                pygame.draw.rect(fenetre, (60, 60, 80), (x_rect, y_ligne, taille_rect_vague, taille_rect_vague), width=1, border_radius=3)


class EcranFinVague:
    def __init__(self):
        self.visible = False
        self.numero_vague = 0
        self.xp_gagnee = 0
        self.police_titre = pygame.font.SysFont("consolas", 30, bold=True)
        self.police_message = pygame.font.SysFont("consolas", 19)
        self.police_xp = pygame.font.SysFont("consolas", 16)
        centre_x = largeur_ecran // 2
        centre_y = hauteur_ecran // 2
        self.rect = pygame.Rect(centre_x - 250, centre_y - 115, 500, 230)
        self.bouton_nouvelle_vague = Bouton(centre_x - 230, centre_y + 60, 210, 44, "Nouvelle vague", 18)
        self.bouton_modification = Bouton(centre_x + 20, centre_y + 60, 210, 44, "Modification", 18)

    def ouvrir(self, numero, xp_gagnee):
        self.numero_vague = numero
        self.xp_gagnee = xp_gagnee
        self.visible = True

    def fermer(self):
        self.visible = False

    def gerer_clic(self, position_clic):
        if not self.visible:
            return None
        if self.bouton_nouvelle_vague.rect.collidepoint(position_clic):
            return "nouvelle_vague"
        if self.bouton_modification.rect.collidepoint(position_clic):
            return "modification"
        return None

    def dessiner(self, fenetre):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 140))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (28, 32, 46), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (100, 120, 200), self.rect, width=2, border_radius=12)
        centre_x = self.rect.centerx
        surface_titre = self.police_titre.render("Félicitations !", True, (210, 200, 80))
        fenetre.blit(surface_titre, (centre_x - surface_titre.get_width() // 2, self.rect.y + 18))
        surface_message = self.police_message.render(f"Vous avez terminé la vague {self.numero_vague} !", True, (200, 200, 200))
        fenetre.blit(surface_message, (centre_x - surface_message.get_width() // 2, self.rect.y + 62))
        surface_xp = self.police_xp.render(f"+ {self.xp_gagnee} XP gagnés pour cette vague", True, (100, 210, 255))
        fenetre.blit(surface_xp, (centre_x - surface_xp.get_width() // 2, self.rect.y + 90))
        self.bouton_nouvelle_vague.dessiner(fenetre)
        self.bouton_modification.dessiner(fenetre)
