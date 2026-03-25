import pygame
from setting import largeur_ecran, hauteur_ecran, couleur_bouton, couleur_bouton_survol, cout_amelioration, niveau_max


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, taille_police=20): #taille_police par défaut à 20, mais peut être ajustée pour les boutons plus petits
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.police = pygame.font.SysFont("consolas", taille_police) #consolas pour un style pixelisé

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
        pos_x = self.rect.x + (self.rect.width - surface_texte.get_width()) // 2 #centrage horizontal du texte
        pos_y = self.rect.y + (self.rect.height - surface_texte.get_height()) // 2 #centrage vertical du texte
        fenetre.blit(surface_texte, (pos_x, pos_y)) # affiche le texte du bouton centré à l'intérieur du rectangle du bouton pour une meilleure esthétique et lisibilité, en calculant la position du texte en fonction de la taille du bouton et de la taille du texte pour que le texte soit toujours parfaitement centré quelle que soit la taille du bouton ou du texte

    def est_survole(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


class PanneauTelephone:
    """
    Téléphone rétractable en bas à droite.
    Amélioration, Objets, Compétence, Infos, New vague, Paramètre
    + bouton Phone pour ouvrir/fermer.
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

        self.ouvert = False #le téléphone commence fermé

        self.bouton_principal = Bouton(self.x, self.y, self.largeur, self.hauteur_ferme, "☰  Phone")

        self.bouton_tourelle = Bouton(self.x, self.y - self.hauteur_ferme - 8, self.largeur, self.hauteur_ferme - 5, "Tourelle")

        self.liste_boutons = []
        nombre_boutons = len(self.noms_boutons)
        for indice, nom in enumerate(self.noms_boutons):
            position_depuis_bas = nombre_boutons - indice
            decalage = position_depuis_bas * (self.hauteur_bouton + self.marge)
            self.liste_boutons.append(
                Bouton(self.x, self.y - decalage, self.largeur, self.hauteur_bouton, nom)
            ) #les boutons sont créés de bas en haut pour éviter de s'embrouiller dans le calcul de leur position

    def gerer_clic(self, position_clic):
        if self.bouton_principal.rect.collidepoint(position_clic): #si le clic est sur le bouton principal, on ouvre ou ferme le téléphone
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
            hauteur_panneau = len(self.noms_boutons) * (self.hauteur_bouton + self.marge) + self.marge #calcul de la hauteur totale du panneau en fonction du nombre de boutons
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
        self.police_info = pygame.font.SysFont("consolas", 18) #consolas pour un style pixelisé
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)

        largeur_panneau = 280
        hauteur_panneau = 180
        self.rect = pygame.Rect(
            largeur_ecran // 2 - largeur_panneau // 2,
            hauteur_ecran // 2 - hauteur_panneau // 2,
            largeur_panneau,
            hauteur_panneau,
        )

        base_x = self.rect.x + 20
        base_y = self.rect.y + self.rect.height - 55
        self.bouton_ameliorer = Bouton(base_x, base_y, 110, 38, "Améliorer")
        self.bouton_fermer = Bouton(base_x + 130, base_y, 110, 38, "Fermer")

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
            nouvel_argent = self.tour_selectionnee.ameliorer(argent_joueur) #la méthode ameliorer de la tour retourne le nouvel argent du joueur après amélioration, ou -1 si l'amélioration n'est pas possible
            if nouvel_argent >= 0:
                return "ameliore", nouvel_argent
            return None, argent_joueur
        """
        Problème avec le système d'amélioration qui ne fonctionne pas

        """
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
        self.police_titre = pygame.font.SysFont("consolas", 30, bold=True) #consolas pour un style pixelisé
        self.police_message = pygame.font.SysFont("consolas", 20)

        centre_x = largeur_ecran // 2
        centre_y = hauteur_ecran // 2

        self.rect = pygame.Rect(centre_x - 230, centre_y - 100, 460, 200)

        self.bouton_nouvelle_vague = Bouton(centre_x - 210, centre_y + 40, 190, 44, "Nouvelle vague", 18)
        self.bouton_modification = Bouton(centre_x + 20, centre_y + 40, 190, 44, "Modification", 18)

    def ouvrir(self, numero):
        self.numero_vague = numero
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
        fenetre.blit(surface_message, (centre_x - surface_message.get_width() // 2, self.rect.y + 62)) #message centré horizontalement

        self.bouton_nouvelle_vague.dessiner(fenetre)
        self.bouton_modification.dessiner(fenetre)