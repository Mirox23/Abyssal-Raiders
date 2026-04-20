import pygame
from setting import largeur_ecran, hauteur_ecran, couleur_bouton, couleur_bouton_survol, cout_amelioration, niveau_max


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, taille_police=20):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.police = pygame.font.SysFont("consolas", taille_police)

    def dessiner(self, fenetre, couleur_fond=None, couleur_texte=(255, 255, 255)):
        position_souris = pygame.mouse.get_pos()
        if couleur_fond is None:
            if self.rect.collidepoint(position_souris):
                couleur = couleur_bouton_survol
            else:
                couleur = couleur_bouton
        else:
            couleur = couleur_fond
        pygame.draw.rect(fenetre, couleur, self.rect, border_radius=5)
        surface_texte = self.police.render(self.texte, True, couleur_texte)
        pos_x = self.rect.x + (self.rect.width - surface_texte.get_width()) // 2
        pos_y = self.rect.y + (self.rect.height - surface_texte.get_height()) // 2
        fenetre.blit(surface_texte, (pos_x, pos_y))

    def est_survole(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


class AffichageXP:
    """Barre XP et niveau affichée en haut à droite de l'écran."""

    def __init__(self):
        self.police_niveau = pygame.font.SysFont("consolas", 18, bold=True)
        self.police_xp = pygame.font.SysFont("consolas", 13)
        self.police_message = pygame.font.SysFont("consolas", 22, bold=True)

    def dessiner(self, fenetre, progression):
        largeur_barre = 180
        hauteur_barre = 14
        barre_x = largeur_ecran - largeur_barre - 20
        barre_y = 20

        # Fond de la barre
        pygame.draw.rect(fenetre, (40, 40, 50), (barre_x, barre_y, largeur_barre, hauteur_barre), border_radius=6)

        # Partie remplie
        largeur_remplie = int(largeur_barre * progression.ratio_xp())
        if largeur_remplie > 0:
            pygame.draw.rect(fenetre, (80, 180, 240), (barre_x, barre_y, largeur_remplie, hauteur_barre), border_radius=6)

        # Contour
        pygame.draw.rect(fenetre, (100, 120, 160), (barre_x, barre_y, largeur_barre, hauteur_barre), width=1, border_radius=6)

        # Texte niveau
        texte_niveau = f"Niv. {progression.niveau}"
        surface_niveau = self.police_niveau.render(texte_niveau, True, (220, 220, 255))
        fenetre.blit(surface_niveau, (barre_x - surface_niveau.get_width() - 8, barre_y - 2))

        # Texte XP
        texte_xp = f"{progression.xp_actuelle} / {progression.xp_necessaire} XP"
        surface_xp = self.police_xp.render(texte_xp, True, (160, 180, 200))
        fenetre.blit(surface_xp, (barre_x + largeur_barre // 2 - surface_xp.get_width() // 2, barre_y + hauteur_barre + 2))

        # Message de montée de niveau
        if progression.message_niveau_up:
            surface_msg = self.police_message.render(f"⬆ {progression.message_niveau_up}", True, (255, 230, 50))
            pos_msg_x = largeur_ecran // 2 - surface_msg.get_width() // 2
            fenetre.blit(surface_msg, (pos_msg_x, 70))


class PanneauTelephone:
    """
    Téléphone rétractable en bas à droite.
    Ordre du haut vers le bas : Amélioration, Objets, Compétence, Infos, New vague, Paramètre.
    + Bouton Tourelle juste au-dessus du bouton Phone.
    """

    noms_boutons = [
        "Amelioration",
        "Objets",
        "Competence",
        "Infos",
        "New vague",
        "Parametre",
    ]

    def __init__(self):
        self.largeur = 175
        self.hauteur_bouton = 40
        self.marge = 6
        self.hauteur_ferme = 45

        self.x = largeur_ecran - 195
        self.y = hauteur_ecran - 55

        self.ouvert = False

        self.bouton_principal = Bouton(self.x, self.y, self.largeur, self.hauteur_ferme, "☰  Phone")
        self.bouton_tourelle = Bouton(self.x, self.y - self.hauteur_ferme - 8, self.largeur, self.hauteur_ferme - 5, "Tourelle")

        self.liste_boutons = []
        nombre_boutons = len(self.noms_boutons)
        for indice, nom in enumerate(self.noms_boutons):
            position_depuis_bas = nombre_boutons - indice
            decalage = position_depuis_bas * (self.hauteur_bouton + self.marge)
            self.liste_boutons.append(
                Bouton(self.x, self.y - decalage, self.largeur, self.hauteur_bouton, nom)
            )

    def gerer_clic(self, position_clic):
        if self.bouton_principal.rect.collidepoint(position_clic):
            self.ouvert = not self.ouvert
            return None

        if self.bouton_tourelle.rect.collidepoint(position_clic):
            return "Tourelle"

        if self.ouvert:
            for bouton in self.liste_boutons:
                if bouton.rect.collidepoint(position_clic):
                    return bouton.texte
        return None

    def dessiner(self, fenetre):
        if self.ouvert:
            hauteur_panneau = len(self.noms_boutons) * (self.hauteur_bouton + self.marge) + self.marge
            rect_fond = pygame.Rect(
                self.x - 4,
                self.y - hauteur_panneau,
                self.largeur + 8,
                hauteur_panneau,
            )
            pygame.draw.rect(fenetre, (30, 32, 42), rect_fond, border_radius=8)
            pygame.draw.rect(fenetre, (60, 65, 90), rect_fond, width=1, border_radius=8)

            for bouton in self.liste_boutons:
                bouton.dessiner(fenetre)

        self.bouton_tourelle.dessiner(fenetre)
        self.bouton_principal.dessiner(fenetre)


class PanneauAmelioration:
    def __init__(self):
        self.visible = False
        self.tour_selectionnee = None
        self.police_info = pygame.font.SysFont("consolas", 18)
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)

        largeur_panneau = 300
        hauteur_panneau = 210
        self.rect = pygame.Rect(
            largeur_ecran // 2 - largeur_panneau // 2,
            hauteur_ecran // 2 - hauteur_panneau // 2,
            largeur_panneau,
            hauteur_panneau,
        )

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

        surface_titre = self.police_titre.render(f"Tour : {tour.type_tour}", True, (220, 220, 255))
        fenetre.blit(surface_titre, (pos_x, pos_y))
        pos_y += 30

        fenetre.blit(self.police_info.render(f"Niveau  : {tour.niveau} / {niveau_max}", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24
        fenetre.blit(self.police_info.render(f"Portée  : {int(tour.portee)}", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24
        fenetre.blit(self.police_info.render(f"Cadence : {tour.cadence:.2f} s", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24

        # Infos spécifiques selon le type
        if tour.type_tour == "Ralentissement":
            texte_special = f"Ralenti  : {int((1 - tour.facteur_ralentissement) * 100)}% / {tour.duree_ralentissement:.1f}s"
            fenetre.blit(self.police_info.render(texte_special, True, (100, 200, 255)), (pos_x, pos_y))
            pos_y += 24
        elif tour.type_tour == "Support":
            texte_special = f"Rayon buff : {int(tour.rayon_buff)} / Bonus : {int(tour.bonus_cadence_buff * 100)}%"
            fenetre.blit(self.police_info.render(texte_special, True, (255, 220, 80)), (pos_x, pos_y))
            pos_y += 24

        if tour.niveau >= niveau_max:
            surface_cout = self.police_info.render("Niveau maximum !", True, (255, 180, 50))
        else:
            surface_cout = self.police_info.render(f"Coût amélioration : {cout_amelioration} ¤", True, (130, 210, 130))
        fenetre.blit(surface_cout, (pos_x, pos_y))

        self.bouton_ameliorer.dessiner(fenetre)
        self.bouton_fermer.dessiner(fenetre)


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

        surface_message = self.police_message.render(
            f"Vous avez terminé la vague {self.numero_vague} !",
            True, (200, 200, 200)
        )
        fenetre.blit(surface_message, (centre_x - surface_message.get_width() // 2, self.rect.y + 62))

        surface_xp = self.police_xp.render(
            f"+ {self.xp_gagnee} XP gagnés pour cette vague",
            True, (100, 210, 255)
        )
        fenetre.blit(surface_xp, (centre_x - surface_xp.get_width() // 2, self.rect.y + 90))

        self.bouton_nouvelle_vague.dessiner(fenetre)
        self.bouton_modification.dessiner(fenetre)