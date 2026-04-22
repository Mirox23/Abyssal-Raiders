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
        self.volume_son = 0.5
        self.bouton_volume_moins = pygame.Rect(360, 230, 56, 44)
        self.bouton_volume_plus = pygame.Rect(584, 230, 56, 44)

        # On stocke UNE image par monde (None = pas encore chargée)
        # Clé = nom du monde en minuscule sans accent
        self.images_maps = {
            "pirate": None,
            "japonais": None,
            "medieval": None,
        }

        # Le monde actuellement affiché dans la map
        # On le met à jour quand le joueur clique sur un monde depuis la sélection
        self.monde_map_actif = "pirate"

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
                "cle": "pirate",
                "couleur": (45, 85, 145),
                "couleur_survol": (65, 110, 180),
                "debloque": True,
                "rect": pygame.Rect(80, 200, 170, 160),
            },
            {
                "nom": "Monde Japonais",
                "cle": "japonais",
                "couleur": (145, 45, 45),
                "couleur_survol": (180, 65, 65),
                "debloque": True,
                "rect": pygame.Rect(290, 200, 170, 160),
            },
            {
                "nom": "Monde Médiéval",
                "cle": "medieval",
                "couleur": (45, 110, 55),
                "couleur_survol": (60, 140, 70),
                "debloque": True,
                "rect": pygame.Rect(500, 200, 170, 160),
            },
            {
                "nom": "Monde Démoniaque",
                "cle": "demoniaque",
                "couleur": (55, 55, 55),
                "couleur_survol": (55, 55, 55),
                "debloque": False,
                "rect": pygame.Rect(710, 200, 170, 160),
            },
        ]

        self.bouton_retour = pygame.Rect(largeur_ecran - 160, hauteur_ecran - 60, 140, 40)

        # Points cliquables sur la MAP GLOBALE (écran "map" du menu principal)
        # Chaque point représente un continent sur la carte générale
        self.points_map_globale = [
            {"nom": "Pirate",      "pos": (200, 300), "debloque": True,  "cle": "pirate"},
            {"nom": "Japonais",    "pos": (400, 260), "debloque": True,  "cle": "japonais"},
            {"nom": "Médiéval",    "pos": (600, 320), "debloque": True,  "cle": "medieval"},
            {"nom": "Samouraï",    "pos": (150, 420), "debloque": True,  "cle": "samourai"},
            {"nom": "Démoniaque",  "pos": (800, 280), "debloque": False, "cle": "demoniaque"},
        ]

        # Points par monde (écran "map" d'un monde spécifique) - ces points représentent les niveaux de ce monde
        # Ces points s'affichent quand on consulte la map d'un monde spécifique
        self.points_par_monde = {
            "pirate": [
                {"nom": "Port des Corsaires", "pos": (200, 250), "debloque": True},
                {"nom": "Île du Crâne",        "pos": (400, 300), "debloque": True},
                {"nom": "Baie Maudite",        "pos": (600, 200), "debloque": False},
            ],
            "japonais": [
                {"nom": "Temple du Soleil",    "pos": (180, 200), "debloque": True},
                {"nom": "Forêt des Esprits",   "pos": (380, 320), "debloque": True},
                {"nom": "Palais du Shogun",    "pos": (580, 250), "debloque": False},
            ],
            "medieval": [
                {"nom": "Village de Pierre",   "pos": (220, 280), "debloque": True},
                {"nom": "Forteresse Royale",   "pos": (440, 200), "debloque": True},
                {"nom": "Tour des Mages",      "pos": (620, 320), "debloque": False},
            ],
        }

        # Quand on clique "voir map" d'un monde depuis la sélection, on mémorise lequel
        self.monde_map_detail = None

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
                        # La map globale s'ouvre (pas de monde spécifique)
                        self.etat = "map"
                        self.monde_map_detail = None
                    elif bouton["action"] == "options":
                        self.etat = "options"
                    return None

        elif self.etat == "mondes":
            if self.bouton_retour.collidepoint(position_clic):
                self.etat = "principal"
                return None

            for monde in self.donnees_mondes:
                if monde["rect"].collidepoint(position_clic):
                    if not monde["debloque"]:
                        # Monde verrouillé = rien
                        return None
                    # On lance le jeu avec ce monde
                    return "lancer_jeu"

        elif self.etat == "map":
            if self.bouton_retour.collidepoint(position_clic):
                # Si on était dans un détail de monde, on revient à la map globale
                if self.monde_map_detail is not None:
                    self.monde_map_detail = None
                else:
                    self.etat = "principal"
                return None

            # Clic sur un point de la map globale
            if self.monde_map_detail is None:
                for point in self.points_map_globale:
                    px, py = point["pos"]
                    distance = ((position_clic[0] - px)**2 + (position_clic[1] - py)**2) ** 0.5
                    if distance <= 12:
                        if point["debloque"] and point["cle"] != "demoniaque":
                            # On affiche la map détaillée de ce monde
                            self.monde_map_detail = point["cle"]
                        else:
                            print("Monde verrouillé ou démoniaque fermé")
                        return None
            else:
                # Clic sur un point de la map d'un monde spécifique
                points = self.points_par_monde.get(self.monde_map_detail, [])
                for point in points:
                    px, py = point["pos"]
                    distance = ((position_clic[0] - px)**2 + (position_clic[1] - py)**2) ** 0.5
                    if distance <= 12:
                        if point["debloque"]:
                            return "lancer_jeu"
                        else:
                            print("Niveau verrouillé")
                        return None

        elif self.etat == "options":
            if self.bouton_retour.collidepoint(position_clic):
                self.etat = "principal"
                return None
            if self.bouton_volume_moins.collidepoint(position_clic):
                self.volume_son = max(0.0, self.volume_son - 0.1)
                self._appliquer_volume()
                return None
            if self.bouton_volume_plus.collidepoint(position_clic):
                self.volume_son = min(1.0, self.volume_son + 0.1)
                self._appliquer_volume()
                return None

        return None

    def mise_a_jour(self, delta_temps):
        self.minuterie_animation += delta_temps

    def dessiner(self):
        self.ecran.fill(self.couleur_fond_menu)

        # Grille de fond
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
        elif self.etat == "options":
            self.dessiner_options()

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
            couleur = self.couleur_bouton_survol if bouton["rect"].collidepoint(position_souris) else self.couleur_bouton_normal

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
                couleur_affichage = monde["couleur_survol"] if rect_monde.collidepoint(position_souris) else monde["couleur"]
            else:
                couleur_affichage = (50, 50, 50)

            rect_ombre = rect_monde.move(4, 4)
            pygame.draw.rect(self.ecran, (8, 8, 8), rect_ombre, border_radius=10)
            pygame.draw.rect(self.ecran, couleur_affichage, rect_monde, border_radius=10)

            couleur_bord = (150, 150, 150) if monde["debloque"] else (80, 80, 80)
            pygame.draw.rect(self.ecran, couleur_bord, rect_monde, width=1, border_radius=10)

            couleur_nom = (240, 240, 240) if monde["debloque"] else (100, 100, 100)
            surface_nom = self.police_monde.render(monde["nom"], True, couleur_nom) # Nom du monde centré dans le rectangle, couleur plus claire si débloqué
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

        couleur_retour = (60, 80, 60) if self.bouton_retour.collidepoint(position_souris) else (35, 50, 38)
        pygame.draw.rect(self.ecran, couleur_retour, self.bouton_retour, border_radius=6)
        surface_retour = self.police_retour.render("← Retour", True, (200, 200, 200))
        self.ecran.blit(surface_retour, (
            self.bouton_retour.x + (self.bouton_retour.width - surface_retour.get_width()) // 2,
            self.bouton_retour.y + (self.bouton_retour.height - surface_retour.get_height()) // 2
        )) # Bouton retour en bas à droite pour revenir au menu principal visible dans tous les sous-menus

    def dessiner_map(self):
        """
        Affiche soit la map globale (tous les continents),
        soit la map détaillée d'un monde spécifique selon monde_map_detail.
        """

        if self.monde_map_detail is None:
            # Map globale = tous les continents + points pour chaque continent 
            self.dessiner_map_globale()
        else:
            # map monde = image de ce monde + points de niveaux de ce monde
            self.dessiner_map_monde(self.monde_map_detail)

    def dessiner_map_globale(self):
        """Map avec tous les continents et leurs points."""

        surface_titre = self.police_titre.render("Carte du Monde", True, (200, 200, 200))
        self.ecran.blit(surface_titre, (largeur_ecran // 2 - surface_titre.get_width() // 2, 30))

        # Chargement image map globale (une seule fois)
        if self.images_maps.get("globale") is None:
            try:
                img = pygame.image.load("image/map_entier.png").convert()
                self.images_maps["globale"] = pygame.transform.scale(
                    img, (largeur_ecran - 160, hauteur_ecran - 200)
                )
            except Exception:
                # Si l'image n'existe pas, on dessine un fond de remplacement
                self.images_maps["globale"] = False  # False = image absente

        rect_carte = pygame.Rect(80, 110, largeur_ecran - 160, hauteur_ecran - 200)

        if self.images_maps.get("globale"):
            self.ecran.blit(self.images_maps["globale"], rect_carte.topleft)
        else:
            # Fond bleu océan si image absente
            pygame.draw.rect(self.ecran, (30, 60, 100), rect_carte, border_radius=8)

        # Dessin des points de chaque continent
        for point in self.points_map_globale:
            px, py = point["pos"]

            # Couleur selon déverrouillage
            if not point["debloque"]:
                couleur_point = (100, 100, 100)
            elif point["cle"] == "demoniaque":
                couleur_point = (150, 30, 30)
            else:
                couleur_point = (0, 220, 100)

            # Cercle extérieur blanc pour visibilité
            pygame.draw.circle(self.ecran, (255, 255, 255), (px, py), 11)
            pygame.draw.circle(self.ecran, couleur_point, (px, py), 9)

            # Nom du point
            texte = self.police_avertissement.render(point["nom"], True, (255, 255, 255))
            self.ecran.blit(texte, (px - texte.get_width() // 2, py - 22))

            # Si verrouillé, petit cadenas (représenté par "🔒" )
            if not point["debloque"]:
                verrou = self.police_avertissement.render("X", True, (200, 50, 50))
                self.ecran.blit(verrou, (px - verrou.get_width() // 2, py - verrou.get_height() // 2))

        # Indication cliquable
        info = self.police_avertissement.render("Cliquez sur un continent pour voir sa map", True, (180, 180, 120))
        self.ecran.blit(info, (largeur_ecran // 2 - info.get_width() // 2, hauteur_ecran - 80))

        self._dessiner_bouton_retour()

    def dessiner_map_monde(self, cle_monde):
        """
        Affiche la map propre à un monde (pirate, japonais, médiéval).
        Chaque monde a son image et ses points de niveaux.
        """

        # Nom affiché selon la clé
        noms_affichage = {
            "pirate":   "Monde Pirate",
            "japonais": "Monde Japonais",
            "medieval": "Monde Médiéval",
            "samourai": "Monde Samouraï",
        }
        nom = noms_affichage.get(cle_monde, cle_monde.capitalize())

        surface_titre = self.police_titre.render(f"Map : {nom}", True, (200, 200, 200)) # Titre avec le nom du monde, centré en haut, couleur claire
        self.ecran.blit(surface_titre, (largeur_ecran // 2 - surface_titre.get_width() // 2, 30))

        # Fichiers images par monde (associés à la même clé que pour les données)
        # Pour l'instant on a pas encore d'image
        fichiers_images = {
            "pirate":   "image/map_pirate.png",
            "japonais": "image/map_japonais.png",
            "medieval": "image/map_medieval.png",
            "samourai": "image/map_samourai.png",
        }

        # Chargement image du monde (une seule fois grâce au cache)
        if self.images_maps.get(cle_monde) is None:
            chemin_img = fichiers_images.get(cle_monde, "")
            try:
                img = pygame.image.load(chemin_img).convert()
                self.images_maps[cle_monde] = pygame.transform.scale(
                    img, (largeur_ecran - 160, hauteur_ecran - 200)
                )
            except Exception:
                self.images_maps[cle_monde] = False  # Image absente

        rect_carte = pygame.Rect(80, 110, largeur_ecran - 160, hauteur_ecran - 200) # Même rect que pour la map globale pour garder la même zone d'affichage

        if self.images_maps.get(cle_monde):
            self.ecran.blit(self.images_maps[cle_monde], rect_carte.topleft)
        else:
            # Couleur de fond différente selon le monde si l'image est absente
            couleurs_fond = {
                "pirate":   (20, 50, 100),
                "japonais": (100, 20, 20),
                "medieval": (20, 80, 30),
                "samourai": (80, 60, 20),
            }
            couleur_fond = couleurs_fond.get(cle_monde, (40, 40, 40))
            pygame.draw.rect(self.ecran, couleur_fond, rect_carte, border_radius=8)

        # Affichage des points de niveaux du monde
        points = self.points_par_monde.get(cle_monde, [])
        # Chaque point a une position, un nom et un statut de déverrouillage
        for point in points:
            px, py = point["pos"]
            couleur_point = (0, 220, 100) if point["debloque"] else (120, 120, 120)

            pygame.draw.circle(self.ecran, (255, 255, 255), (px, py), 11) # cercle extérieur blanc pour faire ressortir le point
            pygame.draw.circle(self.ecran, couleur_point, (px, py), 9) # cercle intérieur coloré selon le statut

            texte = self.police_avertissement.render(point["nom"], True, (255, 255, 255)) # nom du point au-dessus
            self.ecran.blit(texte, (px - texte.get_width() // 2, py - 22))

            if not point["debloque"]:
                verrou = self.police_avertissement.render("X", True, (200, 50, 50))
                self.ecran.blit(verrou, (px - verrou.get_width() // 2, py - verrou.get_height() // 2))

        # Bouton retour vers la map globale
        info = self.police_avertissement.render("← Retour à la carte mondiale", True, (180, 180, 120))
        self.ecran.blit(info, (largeur_ecran // 2 - info.get_width() // 2, hauteur_ecran - 80))

        self._dessiner_bouton_retour()

    def _dessiner_bouton_retour(self):
        """Méthode utilitaire pour dessiner le bouton retour (pour éviter de le dupliquer dans les deux méthodes de dessin de map)"""
        position_souris = pygame.mouse.get_pos()
        couleur_retour = (60, 80, 60) if self.bouton_retour.collidepoint(position_souris) else (35, 50, 38) # couleur plus claire au survol
        pygame.draw.rect(self.ecran, couleur_retour, self.bouton_retour, border_radius=6)
        surface_retour = self.police_retour.render("← Retour", True, (200, 200, 200)) # texte du bouton
        self.ecran.blit(surface_retour, (
            self.bouton_retour.x + (self.bouton_retour.width - surface_retour.get_width()) // 2,
            self.bouton_retour.y + (self.bouton_retour.height - surface_retour.get_height()) // 2
        )) # centrage du texte dans le bouton

    def _appliquer_volume(self):
        try:
            pygame.mixer.music.set_volume(self.volume_son)
        except Exception:
            pass

    def dessiner_options(self):
        titre = self.police_titre.render("Options du capitaine", True, (205, 205, 225))
        self.ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, 70))

        rect_audio = pygame.Rect(280, 170, 440, 130)
        pygame.draw.rect(self.ecran, (25, 34, 46), rect_audio, border_radius=10)
        pygame.draw.rect(self.ecran, (90, 120, 170), rect_audio, width=2, border_radius=10)
        txt_audio = self.police_monde.render("Volume du canon-son", True, (220, 230, 255))
        self.ecran.blit(txt_audio, (rect_audio.x + 20, rect_audio.y + 14))

        pygame.draw.rect(self.ecran, (95, 65, 50), self.bouton_volume_moins, border_radius=7)
        pygame.draw.rect(self.ecran, (95, 65, 50), self.bouton_volume_plus, border_radius=7)
        self.ecran.blit(self.police_bouton.render("-", True, (255, 220, 180)), (self.bouton_volume_moins.x + 20, self.bouton_volume_moins.y + 4))
        self.ecran.blit(self.police_bouton.render("+", True, (255, 220, 180)), (self.bouton_volume_plus.x + 18, self.bouton_volume_plus.y + 4))

        barre = pygame.Rect(430, 244, 144, 14)
        pygame.draw.rect(self.ecran, (45, 45, 58), barre, border_radius=6)
        remplissage = int(barre.width * self.volume_son)
        pygame.draw.rect(self.ecran, (100, 200, 130), (barre.x, barre.y, remplissage, barre.height), border_radius=6)
        pourcentage = self.police_monde.render(f"{int(self.volume_son * 100)}%", True, (220, 255, 220))
        self.ecran.blit(pourcentage, (barre.x + 50, barre.y - 26))

        rect_aide = pygame.Rect(120, 325, 760, 190)
        pygame.draw.rect(self.ecran, (20, 28, 28), rect_aide, border_radius=10)
        pygame.draw.rect(self.ecran, (75, 120, 90), rect_aide, width=2, border_radius=10)
        lignes = [
            "Objectif : protege le mur, pose des tours, lance les vagues et survive.",
            "Competences : A tir puissant, Z pluie de bombes, E buff tours, R givre de zone.",
            "Easter eggs : touche P = petite pluie d'or ; code haut haut bas bas gauche droite = mode fete.",
            "Astuce fun : si le son est a 0%, ton pirate dit 'mode infiltration active'.",
        ]
        for i, ligne in enumerate(lignes):
            surf = self.police_avertissement.render(ligne, True, (200, 220, 205))
            self.ecran.blit(surf, (rect_aide.x + 16, rect_aide.y + 18 + i * 28))

        if self.volume_son <= 0.01:
            blague = self.police_avertissement.render("Silence total : les demons n'entendent plus tes plans.", True, (255, 190, 120))
            self.ecran.blit(blague, (rect_aide.x + 16, rect_aide.bottom - 28))
        elif self.volume_son >= 0.99:
            blague = self.police_avertissement.render("Volume max : meme le Roi Demon se bouche les oreilles.", True, (255, 190, 120))
            self.ecran.blit(blague, (rect_aide.x + 16, rect_aide.bottom - 28))

        self._dessiner_bouton_retour()