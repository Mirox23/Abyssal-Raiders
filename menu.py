import math
import pygame
from setting import largeur_ecran, hauteur_ecran
from musique import MusiqueManager
from progression_monde import ProgressionMonde


class Menu:
    def __init__(self, ecran):
        self.ecran = ecran
        self.etat = "principal"
        self.minuterie_animation = 0.0
        self.volume_son = 0.5
        self.monde_selectionne = "pirate"
        self.niveau_selectionne = 1
        self.musique = MusiqueManager(self.volume_son)
        self.musique.jouer("musique/menu.wav")

        self.police_titre = pygame.font.SysFont("consolas", 52, bold=True)
        self.police_sous_titre = pygame.font.SysFont("consolas", 15)
        self.police_bouton = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_monde = pygame.font.SysFont("consolas", 17, bold=True)
        self.police_avertissement = pygame.font.SysFont("consolas", 13)
        self.police_retour = pygame.font.SysFont("consolas", 16)

        cx = largeur_ecran // 2
        self.boutons_menu_principal = [
            {"texte": "Jouer", "rect": pygame.Rect(cx - 120, 210, 240, 50), "action": "ouvrir_mondes"},
            {"texte": "Map", "rect": pygame.Rect(cx - 120, 272, 240, 50), "action": "ouvrir_map"},
            {"texte": "Options", "rect": pygame.Rect(cx - 120, 334, 240, 50), "action": "options"},
            {"texte": "Sauvegarde", "rect": pygame.Rect(cx - 120, 396, 240, 50), "action": "sauvegarde"},
            {"texte": "Quitter", "rect": pygame.Rect(cx - 120, 458, 240, 50), "action": "quitter"},
        ]
        self.donnees_mondes = [
            {"nom": "Monde Pirate", "cle": "pirate", "couleur": (45, 85, 145), "survol": (65, 110, 180), "debloque": True, "rect": pygame.Rect(80, 200, 170, 160)},
            {"nom": "Monde Japonais", "cle": "japonais", "couleur": (145, 45, 45), "survol": (180, 65, 65), "debloque": True, "rect": pygame.Rect(290, 200, 170, 160)},
            {"nom": "Monde Médiéval", "cle": "medieval", "couleur": (45, 110, 55), "survol": (60, 140, 70), "debloque": True, "rect": pygame.Rect(500, 200, 170, 160)},
            {"nom": "Monde Démoniaque", "cle": "demoniaque", "couleur": (55, 55, 55), "survol": (70, 70, 70), "debloque": False, "rect": pygame.Rect(710, 200, 170, 160)},
        ]
        self.points_map_globale = [
            {"nom": "Samourai", "pos": (180, 430), "debloque": True, "cle": "samourai"},
            {"nom": "Medieval", "pos": (220, 320), "debloque": True, "cle": "medieval"},
            {"nom": "Pirate", "pos": (560, 300), "debloque": True, "cle": "pirate"},
            {"nom": "Demoniaque", "pos": (820, 290), "debloque": False, "cle": "demoniaque"},
        ]
        self.monde_map_detail = None
        self.afficher_carte_continent = False
        self.continent_carte = None
        self.bouton_lancer_niveau = pygame.Rect(largeur_ecran // 2 - 110, hauteur_ecran // 2 + 160, 220, 44)
        self.niveaux_par_continent = {cle: [] for cle in ["pirate", "medieval", "samourai", "demoniaque"]}
        self.progression_monde = ProgressionMonde()
        self.map_entier = None
        self._creer_positions_niveaux()
        self.bouton_retour = pygame.Rect(largeur_ecran - 160, hauteur_ecran - 60, 140, 40)
        self.bouton_volume_moins = pygame.Rect(360, 230, 56, 44)
        self.bouton_volume_plus = pygame.Rect(584, 230, 56, 44)

    def gerer_evenement(self, evenement):
        if evenement.type != pygame.MOUSEBUTTONDOWN:
            return None
        clic = evenement.pos
        if self.etat == "principal":
            for bouton in self.boutons_menu_principal:
                if bouton["rect"].collidepoint(clic):
                    action = bouton["action"]
                    if action == "quitter":
                        return "quitter"
                    if action == "ouvrir_mondes":
                        self.etat = "mondes"
                    elif action == "ouvrir_map":
                        self.etat = "map"
                        self.monde_map_detail = None
                    elif action == "options":
                        self.etat = "options"
                    elif action == "sauvegarde":
                        self.etat = "sauvegarde"
        elif self.etat == "mondes":
            if self.bouton_retour.collidepoint(clic):
                self.etat = "principal"
                return None
            for monde in self.donnees_mondes:
                if monde["rect"].collidepoint(clic) and monde["debloque"]:
                    self.continent_carte = monde["cle"]
                    self.afficher_carte_continent = True
                    self.niveau_selectionne = 1
                    return None
        elif self.etat == "map":
            if self.bouton_retour.collidepoint(clic):
                if self.monde_map_detail:
                    self.monde_map_detail = None
                else:
                    self.etat = "principal"
                return None
            for point in self.points_map_globale:
                if ((clic[0] - point["pos"][0]) ** 2 + (clic[1] - point["pos"][1]) ** 2) ** 0.5 <= 12:
                    if point["debloque"] and point["cle"] != "demoniaque":
                        self.continent_carte = point["cle"]
                        self.afficher_carte_continent = True
                        self.niveau_selectionne = 1
                    return None
        elif self.etat == "options":
            if self.bouton_retour.collidepoint(clic):
                self.etat = "principal"
            elif self.bouton_volume_moins.collidepoint(clic):
                self.volume_son = max(0.0, self.volume_son - 0.1)
                self.musique.regler_volume(self.volume_son)
            elif self.bouton_volume_plus.collidepoint(clic):
                self.volume_son = min(1.0, self.volume_son + 0.1)
                self.musique.regler_volume(self.volume_son)
        elif self.etat == "sauvegarde":
            if self.bouton_retour.collidepoint(clic):
                self.etat = "principal"
                return None

        # Mini-fenêtre carte continent (depuis mondes ou map)
        if self.afficher_carte_continent:
            # Bouton retour ferme la mini-fenêtre
            if self.bouton_retour.collidepoint(clic):
                self.afficher_carte_continent = False
                self.continent_carte = None
                return None
            # Choix niveau
            niveaux = self.niveaux_par_continent.get(self.continent_carte, [])
            for numero, pos in niveaux:
                if ((clic[0] - pos[0]) ** 2 + (clic[1] - pos[1]) ** 2) ** 0.5 <= 14:
                    if self.progression_monde.est_niveau_debloque(self.continent_carte, numero):
                        self.niveau_selectionne = numero
                    return None
            # Lancer niveau (obligatoire)
            if self.bouton_lancer_niveau.collidepoint(clic):
                if self.progression_monde.est_niveau_debloque(self.continent_carte, self.niveau_selectionne):
                    self.monde_selectionne = self.continent_carte or "pirate"
                    self.afficher_carte_continent = False
                    return "lancer_jeu"
        return None

    def mise_a_jour(self, delta_temps):
        self.minuterie_animation += delta_temps

    def dessiner(self):
        self.ecran.fill((14, 22, 18))
        for x in range(0, largeur_ecran, 60):
            pygame.draw.line(self.ecran, (20, 32, 24), (x, 0), (x, hauteur_ecran))
        for y in range(0, hauteur_ecran, 60):
            pygame.draw.line(self.ecran, (20, 32, 24), (0, y), (largeur_ecran, y))
        if self.etat == "principal":
            self._dessiner_principal()
        elif self.etat == "mondes":
            self._dessiner_mondes()
        elif self.etat == "map":
            self._dessiner_map()
        elif self.etat == "options":
            self._dessiner_options()
        elif self.etat == "sauvegarde":
            self._dessiner_sauvegarde()

        if self.afficher_carte_continent:
            self._dessiner_carte_continent()

    def _dessiner_principal(self):
        pulse = int(10 * math.sin(self.minuterie_animation * 2.0))
        titre = self.police_titre.render("ABYSSAL RAIDERS", True, (210 + pulse, 140 + pulse, 35))
        self.ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, 110))
        sous = self.police_sous_titre.render("~ Un tower defense démoniaque ~", True, (90, 110, 95))
        self.ecran.blit(sous, (largeur_ecran // 2 - sous.get_width() // 2, 170))
        souris = pygame.mouse.get_pos()
        for bouton in self.boutons_menu_principal:
            couleur = (60, 110, 72) if bouton["rect"].collidepoint(souris) else (38, 70, 48)
            pygame.draw.rect(self.ecran, (8, 14, 10), bouton["rect"].move(3, 3), border_radius=6)
            pygame.draw.rect(self.ecran, couleur, bouton["rect"], border_radius=6)
            txt = self.police_bouton.render(bouton["texte"], True, (220, 235, 220))
            self.ecran.blit(txt, (bouton["rect"].centerx - txt.get_width() // 2, bouton["rect"].centery - txt.get_height() // 2))

    def _dessiner_mondes(self):
        titre = self.police_titre.render("Choisir un Monde", True, (200, 200, 200))
        self.ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, 100))
        souris = pygame.mouse.get_pos()
        for monde in self.donnees_mondes:
            rect = monde["rect"]
            if monde["debloque"]:
                couleur = monde["survol"] if rect.collidepoint(souris) else monde["couleur"]
            else:
                couleur = (50, 50, 50)
            pygame.draw.rect(self.ecran, couleur, rect, border_radius=10)
            nom = self.police_monde.render(monde["nom"], True, (240, 240, 240) if monde["debloque"] else (100, 100, 100))
            self.ecran.blit(nom, (rect.centerx - nom.get_width() // 2, rect.centery - nom.get_height() // 2))
        self._dessiner_retour()

    def _dessiner_map(self):
        titre = self.police_titre.render("Carte du Monde", True, (200, 200, 200))
        self.ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, 30))
        rect_carte = pygame.Rect(80, 110, largeur_ecran - 160, hauteur_ecran - 200)
        if self.map_entier is None:
            try:
                img = pygame.image.load("image/map_entier.png").convert()
                self.map_entier = pygame.transform.scale(img, (rect_carte.width, rect_carte.height))
            except Exception:
                self.map_entier = False
        if self.map_entier:
            self.ecran.blit(self.map_entier, rect_carte.topleft)
        else:
            pygame.draw.rect(self.ecran, (30, 60, 100), rect_carte, border_radius=8)
        for point in self.points_map_globale:
            px, py = point["pos"]
            couleur = (0, 220, 100) if point["debloque"] else (100, 100, 100)
            pygame.draw.circle(self.ecran, (255, 255, 255), (px, py), 11)
            pygame.draw.circle(self.ecran, couleur, (px, py), 9)
            txt = self.police_avertissement.render(point["nom"], True, (255, 255, 255))
            self.ecran.blit(txt, (px - txt.get_width() // 2, py - 22))
        self._dessiner_retour()

    def _dessiner_sauvegarde(self):
        titre = self.police_titre.render("Sauvegarde", True, (200, 200, 200))
        self.ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, 90))
        txt = self.police_avertissement.render("Bientôt : sauvegarde de la progression.", True, (200, 220, 205))
        self.ecran.blit(txt, (largeur_ecran // 2 - txt.get_width() // 2, 200))
        self._dessiner_retour()

    def _dessiner_carte_continent(self):
        # voile + fenêtre
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 140))
        self.ecran.blit(voile, (0, 0))
        rect = pygame.Rect(140, 80, 720, 400)
        pygame.draw.rect(self.ecran, (20, 28, 40), rect, border_radius=12)
        pygame.draw.rect(self.ecran, (90, 120, 170), rect, width=2, border_radius=12)
        nom = (self.continent_carte or "pirate").capitalize()
        titre = self.police_monde.render(f"Carte du continent : {nom}", True, (220, 230, 255))
        self.ecran.blit(titre, (rect.x + 16, rect.y + 14))

        # mini-carte
        zone_carte = pygame.Rect(rect.x + 16, rect.y + 52, rect.width - 32, rect.height - 120)
        pygame.draw.rect(self.ecran, (35, 55, 85), zone_carte, border_radius=10)
        pygame.draw.rect(self.ecran, (70, 95, 130), zone_carte, width=1, border_radius=10)

        niveaux = self.niveaux_par_continent.get(self.continent_carte, [])
        for numero, pos in niveaux:
            debloque = self.progression_monde.est_niveau_debloque(self.continent_carte, numero)
            conquis = self.progression_monde.est_conquis(self.continent_carte, numero)
            if conquis:
                couleur = (0, 220, 100)
            elif not debloque:
                couleur = (120, 120, 120)
            else:
                couleur = (255, 255, 255)
            if numero == self.niveau_selectionne and debloque:
                couleur = (255, 230, 120)
            pygame.draw.circle(self.ecran, couleur, pos, 14)
            pygame.draw.circle(self.ecran, (20, 20, 25), pos, 12)
            txt = self.police_avertissement.render(str(numero), True, (255, 255, 255))
            self.ecran.blit(txt, (pos[0] - txt.get_width() // 2, pos[1] - txt.get_height() // 2))

            # petites vagues (3 carrés)
            base_x = pos[0] - 26
            base_y = pos[1] + 22
            for v in range(3):
                pygame.draw.rect(self.ecran, (100, 100, 110), (base_x + v * 14, base_y, 10, 10), border_radius=2)

        # bouton lancer (obligatoire)
        pygame.draw.rect(self.ecran, (38, 70, 48), self.bouton_lancer_niveau, border_radius=8)
        pygame.draw.rect(self.ecran, (80, 130, 90), self.bouton_lancer_niveau, width=2, border_radius=8)
        txt = self.police_bouton.render(f"Lancer niveau {self.niveau_selectionne}", True, (220, 235, 220))
        self.ecran.blit(txt, (self.bouton_lancer_niveau.centerx - txt.get_width() // 2, self.bouton_lancer_niveau.centery - txt.get_height() // 2))

        self._dessiner_retour()

    def _creer_positions_niveaux(self):
        # positions simples en grille sur la mini-carte
        rect = pygame.Rect(140, 80, 720, 400)
        zone = pygame.Rect(rect.x + 16, rect.y + 52, rect.width - 32, rect.height - 120)
        xs = [zone.x + 120, zone.x + 260, zone.x + 400, zone.x + 540]
        ys = [zone.y + 70, zone.y + 150]
        positions = []
        i = 1
        for y in ys:
            for x in xs:
                positions.append((i, (x, y)))
                i += 1
        self.niveaux_par_continent["pirate"] = positions[:8]
        self.niveaux_par_continent["medieval"] = positions[:8]
        self.niveaux_par_continent["samourai"] = positions[:8]
        self.niveaux_par_continent["demoniaque"] = positions[:8]

    def appliquer_progression(self, progression_monde):
        self.progression_monde = progression_monde

    def _dessiner_options(self):
        titre = self.police_titre.render("Options du capitaine", True, (205, 205, 225))
        self.ecran.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, 70))
        rect_audio = pygame.Rect(280, 170, 440, 130)
        pygame.draw.rect(self.ecran, (25, 34, 46), rect_audio, border_radius=10)
        pygame.draw.rect(self.ecran, (90, 120, 170), rect_audio, width=2, border_radius=10)
        self.ecran.blit(self.police_monde.render("Volume du canon-son", True, (220, 230, 255)), (rect_audio.x + 20, rect_audio.y + 14))
        pygame.draw.rect(self.ecran, (95, 65, 50), self.bouton_volume_moins, border_radius=7)
        pygame.draw.rect(self.ecran, (95, 65, 50), self.bouton_volume_plus, border_radius=7)
        self.ecran.blit(self.police_bouton.render("-", True, (255, 220, 180)), (self.bouton_volume_moins.x + 20, self.bouton_volume_moins.y + 4))
        self.ecran.blit(self.police_bouton.render("+", True, (255, 220, 180)), (self.bouton_volume_plus.x + 18, self.bouton_volume_plus.y + 4))
        barre = pygame.Rect(430, 244, 144, 14)
        pygame.draw.rect(self.ecran, (45, 45, 58), barre, border_radius=6)
        pygame.draw.rect(self.ecran, (100, 200, 130), (barre.x, barre.y, int(barre.width * self.volume_son), barre.height), border_radius=6)
        info = [
            "Objectif : protège le mur, pose des tours, lance les vagues et survie.",
            "Compétences : touche A = tir puissant, touche Z = pluie de bombes, touche E = boost tours, touche R = gèle une zone.",
            "Easter eggs : touche P = petite pluie d'or ; flèche du : haut, haut, bas, bas, gauche, droite = ouvre un mode fête.",
        ]
        rect_aide = pygame.Rect(120, 325, 760, 170)
        pygame.draw.rect(self.ecran, (20, 28, 28), rect_aide, border_radius=10)
        pygame.draw.rect(self.ecran, (75, 120, 90), rect_aide, width=2, border_radius=10)
        for i, ligne in enumerate(info):
            self.ecran.blit(self.police_avertissement.render(ligne, True, (200, 220, 205)), (rect_aide.x + 16, rect_aide.y + 18 + i * 28))
        blague = "Silence total : les démons n'entendent plus tes plans." if self.volume_son <= 0.01 else "Volume max : même le Roi Démon se bouche les oreilles."
        self.ecran.blit(self.police_avertissement.render(blague, True, (255, 190, 120)), (rect_aide.x + 16, rect_aide.bottom - 28))
        self._dessiner_retour()

    def _dessiner_retour(self):
        souris = pygame.mouse.get_pos()
        couleur = (60, 80, 60) if self.bouton_retour.collidepoint(souris) else (35, 50, 38)
        pygame.draw.rect(self.ecran, couleur, self.bouton_retour, border_radius=6)
        txt = self.police_retour.render("← Retour", True, (200, 200, 200))
        self.ecran.blit(txt, (self.bouton_retour.centerx - txt.get_width() // 2, self.bouton_retour.centery - txt.get_height() // 2))
