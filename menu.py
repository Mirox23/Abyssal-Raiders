import pygame
import math
from setting import largeur_ecran, hauteur_ecran


class Menu:
    couleur_fond_menu = (14, 22, 18)
    couleur_titre = (210, 140, 35)
    couleur_sous_titre = (90, 110, 95)
    couleur_bouton_normal = (38, 70, 48)
    couleur_bouton_survol = (60, 110, 72)
    couleur_texte_bouton = (220, 235, 220)
    couleur_separateur = (50, 80, 55)

    def __init__(self, ecran):
        self.ecran = ecran
        self.police_titre = pygame.font.SysFont("consolas", 52, bold=True)
        self.police_sous_titre = pygame.font.SysFont("consolas", 15)
        self.police_bouton = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_monde = pygame.font.SysFont("consolas", 17, bold=True)
        self.police_avertissement = pygame.font.SysFont("consolas", 13)
        self.police_retour = pygame.font.SysFont("consolas", 16)

        self.etat = "principal"
        self.minuterie_animation = 0.0
        self.image_map = None
        
        centre_x = largeur_ecran // 2

        self.boutons_menu_principal = [
            {"texte": "Jouer",      "rect": pygame.Rect(centre_x - 120, 210, 240, 50), "action": "ouvrir_mondes"},
            {"texte": "Map",        "rect": pygame.Rect(centre_x - 120, 272, 240, 50), "action": "ouvrir_map"},
            {"texte": "Options",    "rect": pygame.Rect(centre_x - 120, 334, 240, 50), "action": "options"},
            {"texte": "Sauvegarde", "rect": pygame.Rect(centre_x - 120, 396, 240, 50), "action": "sauvegarde"},
            {"texte": "Quitter",    "rect": pygame.Rect(centre_x - 120, 458, 240, 50), "action": "quitter"},
        ]

        self.donnees_mondes = [
            {
                "nom": "Monde Pirate",
                "couleur": (45, 85, 145),
                "couleur_survol": (65, 110, 180),
                "debloque": True,
                "rect": pygame.Rect(80, 200, 170, 160),
            },
            {
                "nom": "Monde Japonais",
                "couleur": (145, 45, 45),
                "couleur_survol": (180, 65, 65),
                "debloque": True,
                "rect": pygame.Rect(290, 200, 170, 160),
            },
            {
                "nom": "Monde Médiéval",
                "couleur": (45, 110, 55),
                "couleur_survol": (60, 140, 70),
                "debloque": True,
                "rect": pygame.Rect(500, 200, 170, 160),
            },
            {
                "nom": "Monde Démoniaque",
                "couleur": (55, 55, 55),
                "couleur_survol": (55, 55, 55),
                "debloque": False,
                "rect": pygame.Rect(710, 200, 170, 160),
            },
        ]

        self.bouton_retour = pygame.Rect(largeur_ecran - 160, hauteur_ecran - 60, 140, 40)

    def gerer_evenement(self, evenement):
        if evenement.type != pygame.MOUSEBUTTONDOWN:
            return None

        position_clic = evenement.pos

        if self.etat == "principal":
            for bouton in self.boutons_menu_principal:
                if bouton["rect"].collidepoint(position_clic):
                    if bouton["action"] == "quitter":
                        return "quitter"
                    elif bouton["action"] == "ouvrir_mondes":
                        self.etat = "mondes"
                    elif bouton["action"] == "ouvrir_map":
                        self.etat = "map"
                    return None

        elif self.etat == "mondes":
            if self.bouton_retour.collidepoint(position_clic):
                self.etat = "principal"
                return None
            for monde in self.donnees_mondes:
                if monde["rect"].collidepoint(position_clic) and monde["debloque"]:
                    return "lancer_jeu"

        elif self.etat == "map":
            if self.bouton_retour.collidepoint(position_clic):
                self.etat = "principal"
                return None

            # clic sur les points de la map
            if hasattr(self, "points_map"):
                for point in self.points_map:
                    px, py = point["pos"]
                    distance = ((position_clic[0] - px)**2 + (position_clic[1] - py)**2) ** 0.5

                    if distance <= 10:
                        if point["debloque"]:
                            return "lancer_jeu"
                        else:
                            print("Monde verrouillé")

        return None

    def mise_a_jour(self, delta_temps):
        self.minuterie_animation += delta_temps

    def dessiner(self):
        self.ecran.fill(self.couleur_fond_menu)

        for pos_x in range(0, largeur_ecran, 60):
            pygame.draw.line(self.ecran, (20, 32, 24), (pos_x, 0), (pos_x, hauteur_ecran))
        for pos_y in range(0, hauteur_ecran, 60):
            pygame.draw.line(self.ecran, (20, 32, 24), (0, pos_y), (largeur_ecran, pos_y))

        if self.etat == "principal":
            self.dessiner_menu_principal()
        elif self.etat == "mondes":
            self.dessiner_selection_monde()
        elif self.etat == "map":
            self.dessiner_map()

    def dessiner_menu_principal(self):
        pulsation = int(10 * math.sin(self.minuterie_animation * 2.0))
        rouge = min(255, self.couleur_titre[0] + pulsation)
        vert = min(255, self.couleur_titre[1] + pulsation)
        surface_titre = self.police_titre.render("ABYSSAL RAIDERS", True, (rouge, vert, self.couleur_titre[2]))
        self.ecran.blit(surface_titre, (largeur_ecran // 2 - surface_titre.get_width() // 2, 110))

        surface_sous = self.police_sous_titre.render("~ Un tower defense démoniaque ~", True, self.couleur_sous_titre)
        self.ecran.blit(surface_sous, (largeur_ecran // 2 - surface_sous.get_width() // 2, 170))

        pygame.draw.line(
            self.ecran, self.couleur_separateur,
            (largeur_ecran // 2 - 140, 198),
            (largeur_ecran // 2 + 140, 198), 1
        )

        position_souris = pygame.mouse.get_pos()
        for bouton in self.boutons_menu_principal:
            if bouton["rect"].collidepoint(position_souris):
                couleur = self.couleur_bouton_survol
            else:
                couleur = self.couleur_bouton_normal

            rect_ombre = bouton["rect"].move(3, 3)
            pygame.draw.rect(self.ecran, (8, 14, 10), rect_ombre, border_radius=6)
            pygame.draw.rect(self.ecran, couleur, bouton["rect"], border_radius=6)
            pygame.draw.rect(self.ecran, self.couleur_separateur, bouton["rect"], width=1, border_radius=6)

            surface_texte = self.police_bouton.render(bouton["texte"], True, self.couleur_texte_bouton)
            pos_x = bouton["rect"].x + (bouton["rect"].width - surface_texte.get_width()) // 2
            pos_y = bouton["rect"].y + (bouton["rect"].height - surface_texte.get_height()) // 2
            self.ecran.blit(surface_texte, (pos_x, pos_y))

        surface_version = self.police_sous_titre.render("v0.3", True, (45, 60, 48))
        self.ecran.blit(surface_version, (
            largeur_ecran - surface_version.get_width() - 12,
            hauteur_ecran - surface_version.get_height() - 8
        ))

    def dessiner_selection_monde(self):
        surface_titre = self.police_titre.render("Choisir un Monde", True, (200, 200, 200))
        self.ecran.blit(surface_titre, (largeur_ecran // 2 - surface_titre.get_width() // 2, 100))

        position_souris = pygame.mouse.get_pos()

        for monde in self.donnees_mondes:
            rect_monde = monde["rect"]

            if monde["debloque"]:
                if rect_monde.collidepoint(position_souris):
                    couleur_affichage = monde["couleur_survol"]
                else:
                    couleur_affichage = monde["couleur"]
            else:
                couleur_affichage = (50, 50, 50)

            rect_ombre = rect_monde.move(4, 4)
            pygame.draw.rect(self.ecran, (8, 8, 8), rect_ombre, border_radius=10)
            pygame.draw.rect(self.ecran, couleur_affichage, rect_monde, border_radius=10)

            if monde["debloque"]:
                pygame.draw.rect(self.ecran, (150, 150, 150), rect_monde, width=1, border_radius=10)
            else:
                pygame.draw.rect(self.ecran, (80, 80, 80), rect_monde, width=1, border_radius=10)

            if monde["debloque"]:
                couleur_nom = (240, 240, 240)
            else:
                couleur_nom = (100, 100, 100)

            surface_nom = self.police_monde.render(monde["nom"], True, couleur_nom)
            nom_x = rect_monde.x + (rect_monde.width - surface_nom.get_width()) // 2
            nom_y = rect_monde.y + rect_monde.height // 2 - surface_nom.get_height() // 2
            self.ecran.blit(surface_nom, (nom_x, nom_y))

            if not monde["debloque"]:
                surface_avert = self.police_avertissement.render("Tu n'es pas assez", True, (180, 60, 60))
                surface_avert2 = self.police_avertissement.render("fort pour y pénétrer", True, (180, 60, 60))
                self.ecran.blit(surface_avert, (
                    rect_monde.x + (rect_monde.width - surface_avert.get_width()) // 2,
                    rect_monde.y - 36
                ))
                self.ecran.blit(surface_avert2, (
                    rect_monde.x + (rect_monde.width - surface_avert2.get_width()) // 2,
                    rect_monde.y - 20
                ))

        position_souris = pygame.mouse.get_pos()
        if self.bouton_retour.collidepoint(position_souris):
            couleur_retour = (60, 80, 60)
        else:
            couleur_retour = (35, 50, 38)
        pygame.draw.rect(self.ecran, couleur_retour, self.bouton_retour, border_radius=6)
        surface_retour = self.police_retour.render("← Retour", True, (200, 200, 200))
        self.ecran.blit(surface_retour, (
            self.bouton_retour.x + (self.bouton_retour.width - surface_retour.get_width()) // 2,
            self.bouton_retour.y + (self.bouton_retour.height - surface_retour.get_height()) // 2
        ))

    def dessiner_map(self):
        surface_titre = self.police_titre.render("Carte du Monde", True, (200, 200, 200))
        self.ecran.blit(surface_titre, (largeur_ecran // 2 - surface_titre.get_width() // 2, 80))

        # Charger l'image une seule fois  
        if self.image_map is None:
            self.image_map = pygame.image.load("image/map_entier.png").convert()
            self.image_map = pygame.transform.scale(
                self.image_map,
                (largeur_ecran - 160, hauteur_ecran - 260)
            )

        rect_carte = pygame.Rect(80, 160, largeur_ecran - 160, hauteur_ecran - 260)

        # Affichage de la map
        self.ecran.blit(self.image_map, rect_carte.topleft)

        # Points cliquables sur la carte
        self.points_map = [
            {"nom": "Pirate", "pos": (200, 300), "debloque": True},
            {"nom": "Japon", "pos": (400, 260), "debloque": True},
            {"nom": "Médiéval", "pos": (600, 320), "debloque": True},
            {"nom": "Démoniaque", "pos": (800, 280), "debloque": False},
        ]

        for point in self.points_map:
            couleur = (0, 255, 100) if point["debloque"] else (120, 120, 120)

            pygame.draw.circle(self.ecran, couleur, point["pos"], 8)

            # petit texte au dessus
            texte = self.police_avertissement.render(point["nom"], True, (255, 255, 255))
            self.ecran.blit(texte, (point["pos"][0] - texte.get_width() // 2, point["pos"][1] - 20))

        # bouton retour
        position_souris = pygame.mouse.get_pos()
        couleur_retour = (60, 80, 60) if self.bouton_retour.collidepoint(position_souris) else (35, 50, 38)

        pygame.draw.rect(self.ecran, couleur_retour, self.bouton_retour, border_radius=6)
        surface_retour = self.police_retour.render("← Retour", True, (200, 200, 200))
        self.ecran.blit(surface_retour, (
            self.bouton_retour.x + (self.bouton_retour.width - surface_retour.get_width()) // 2,
            self.bouton_retour.y + (self.bouton_retour.height - surface_retour.get_height()) // 2
        ))