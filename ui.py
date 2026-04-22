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
            couleur = couleur_bouton_survol if self.rect.collidepoint(position_souris) else couleur_bouton
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

        pygame.draw.rect(fenetre, (40, 40, 50), (barre_x, barre_y, largeur_barre, hauteur_barre), border_radius=6)
        largeur_remplie = int(largeur_barre * progression.ratio_xp())
        if largeur_remplie > 0:
            pygame.draw.rect(fenetre, (80, 180, 240), (barre_x, barre_y, largeur_remplie, hauteur_barre), border_radius=6)
        pygame.draw.rect(fenetre, (100, 120, 160), (barre_x, barre_y, largeur_barre, hauteur_barre), width=1, border_radius=6)

        texte_niveau = f"Niv. {progression.niveau}"
        surface_niveau = self.police_niveau.render(texte_niveau, True, (220, 220, 255))
        fenetre.blit(surface_niveau, (barre_x - surface_niveau.get_width() - 8, barre_y - 2))

        texte_xp = f"{progression.xp_actuelle} / {progression.xp_necessaire} XP"
        surface_xp = self.police_xp.render(texte_xp, True, (160, 180, 200))
        fenetre.blit(surface_xp, (barre_x + largeur_barre // 2 - surface_xp.get_width() // 2, barre_y + hauteur_barre + 2))

        if progression.message_niveau_up:
            surface_msg = self.police_message.render(f"⬆ {progression.message_niveau_up}", True, (255, 230, 50))
            pos_msg_x = largeur_ecran // 2 - surface_msg.get_width() // 2
            fenetre.blit(surface_msg, (pos_msg_x, 70))


class PanneauTelephone:
    """
    Téléphone rétractable en bas à droite.
    Ordre du haut vers le bas : Info, Objets, Competence, Achèvement, New vague, Parametre.
    """

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
            self.liste_boutons.append(
                Bouton(self.x, self.y - decalage, self.largeur, self.hauteur_bouton, nom)
            ) # Boutons du menu déroulant, positionnés les uns au-dessus des autres, avec une marge entre eux

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
            rect_fond = pygame.Rect(
                self.x - 4,
                self.y - hauteur_panneau,
                self.largeur + 8,
                hauteur_panneau,
            )
            pygame.draw.rect(fenetre, (28, 35, 48), rect_fond, border_radius=10)
            pygame.draw.rect(fenetre, (90, 120, 170), rect_fond, width=2, border_radius=10)

            for bouton in self.liste_boutons:
                bouton.dessiner(fenetre, couleur_fond=(40, 60, 88), couleur_texte=(225, 235, 255))

        self.bouton_principal.dessiner(fenetre, couleur_fond=(42, 84, 110), couleur_texte=(220, 245, 255))


class FenetreRecompensesTalents:
    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(120, 60, 760, 440)
        self.rect_recompense = pygame.Rect(self.rect.x + 18, self.rect.y + 72, 340, 340)
        self.rect_talents = pygame.Rect(self.rect.x + 380, self.rect.y + 72, 360, 340)
        self.police_titre = pygame.font.SysFont("consolas", 24, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.police_petite = pygame.font.SysFont("consolas", 12)
        self.bouton_fermer = Bouton(self.rect.right - 100, self.rect.y + 14, 84, 30, "Fermer", 14)
        self.niveaux_recuperes = set()
        self.talents = {
            "degats_competence": {"nom": "Poudre noire +", "niveau": 0, "max": 4},
            "reduction_cout": {"nom": "Marchandage pirate", "niveau": 0, "max": 3},
            "prime_or": {"nom": "Prime de chasse", "niveau": 0, "max": 4},
            "resistance_mur": {"nom": "Mur renforce", "niveau": 0, "max": 3},
        }
        self.boutons_recompenses = []
        self.boutons_talents = []
        self._maj_boutons()

    def _maj_boutons(self):
        self.boutons_recompenses = [pygame.Rect(self.rect_recompense.x + 18, self.rect_recompense.y + 34 + i * 36, 300, 28) for i in range(8)]
        self.boutons_talents = []
        for i, cle in enumerate(self.talents.keys()):
            self.boutons_talents.append((cle, pygame.Rect(self.rect_talents.x + 16, self.rect_talents.y + 42 + i * 72, 326, 60)))

    def ouvrir(self):
        self.visible = True

    def gerer_clic(self, position_clic, progression):
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.visible = False
            return ("fermer", None)

        for i, rect in enumerate(self.boutons_recompenses):
            niveau = i + 1
            if rect.collidepoint(position_clic) and progression.niveau >= niveau and niveau not in self.niveaux_recuperes:
                self.niveaux_recuperes.add(niveau)
                return ("recompense", 8 + niveau * 2)

        for cle, rect in self.boutons_talents:
            talent = self.talents[cle]
            if rect.collidepoint(position_clic) and progression.points_talent > 0 and talent["niveau"] < talent["max"]:
                progression.points_talent -= 1
                talent["niveau"] += 1
                return ("talent", cle)

        if self.rect.collidepoint(position_clic):
            return ("consomme", None)
        return None

    def dessiner(self, fenetre, progression):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 150))
        fenetre.blit(voile, (0, 0))

        pygame.draw.rect(fenetre, (20, 25, 40), self.rect, border_radius=14)
        pygame.draw.rect(fenetre, (90, 120, 175), self.rect, width=2, border_radius=14)
        fenetre.blit(self.police_titre.render("Recompenses & Arbre de talents", True, (220, 230, 255)), (self.rect.x + 14, self.rect.y + 16))
        fenetre.blit(self.police_texte.render(f"Nombre point d'amelioration : {progression.points_talent}", True, (255, 220, 130)), (self.rect.x + 14, self.rect.y + 46))
        self.bouton_fermer.dessiner(fenetre)

        pygame.draw.rect(fenetre, (26, 34, 52), self.rect_recompense, border_radius=10)
        pygame.draw.rect(fenetre, (65, 105, 165), self.rect_recompense, width=1, border_radius=10)
        fenetre.blit(self.police_texte.render("Recompense XP", True, (185, 220, 255)), (self.rect_recompense.x + 10, self.rect_recompense.y + 8))

        for i, rect in enumerate(self.boutons_recompenses):
            niveau = i + 1
            claim = progression.niveau >= niveau and niveau not in self.niveaux_recuperes
            deja = niveau in self.niveaux_recuperes
            couleur = (22, 102, 68) if claim else (72, 72, 82)
            if deja:
                couleur = (45, 86, 58)
            pygame.draw.rect(fenetre, couleur, rect, border_radius=6)
            texte = f"Niv {niveau} : +{8 + niveau * 2} or"
            if deja:
                texte += " (recupere)"
            fenetre.blit(self.police_petite.render(texte, True, (230, 235, 230)), (rect.x + 8, rect.y + 8))

        pygame.draw.rect(fenetre, (26, 34, 52), self.rect_talents, border_radius=10)
        pygame.draw.rect(fenetre, (65, 105, 165), self.rect_talents, width=1, border_radius=10)
        fenetre.blit(self.police_texte.render("Arbre de talents du joueur", True, (185, 220, 255)), (self.rect_talents.x + 10, self.rect_talents.y + 8))
        fenetre.blit(self.police_petite.render("1 point = 1 niveau", True, (205, 215, 235)), (self.rect_talents.x + 12, self.rect_talents.y + 24))

        for cle, rect in self.boutons_talents:
            talent = self.talents[cle]
            pygame.draw.rect(fenetre, (44, 56, 86), rect, border_radius=7)
            pygame.draw.rect(fenetre, (95, 130, 182), rect, width=1, border_radius=7)
            fenetre.blit(self.police_petite.render(f"{talent['nom']} ({talent['niveau']}/{talent['max']})", True, (235, 240, 255)), (rect.x + 10, rect.y + 12))
            fenetre.blit(self.police_petite.render("Clique pour ameliorer", True, (170, 205, 245)), (rect.x + 10, rect.y + 34))


class PanneauCompetences:
    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(200, 90, 600, 380)
        self.police_titre = pygame.font.SysFont("consolas", 24, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.bouton_fermer = Bouton(self.rect.right - 96, self.rect.y + 12, 80, 30, "Fermer", 14)
        self.boutons = []

    def ouvrir(self):
        self.visible = True

    def gerer_clic(self, position_clic):
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.visible = False
            return None
        for cle, rect in self.boutons:
            if rect.collidepoint(position_clic):
                return cle
        if self.rect.collidepoint(position_clic):
            return "consomme"
        return None

    def dessiner(self, fenetre, gestionnaire_competences, argent_joueur):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 135))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (20, 26, 40), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (95, 125, 180), self.rect, width=2, border_radius=12)
        fenetre.blit(self.police_titre.render("Competences du Pirate", True, (220, 230, 255)), (self.rect.x + 16, self.rect.y + 16))
        self.bouton_fermer.dessiner(fenetre)

        self.boutons = []
        y = self.rect.y + 70
        for cle, donnees in gestionnaire_competences.competences.items():
            rect = pygame.Rect(self.rect.x + 18, y, self.rect.width - 36, 64)
            self.boutons.append((cle, rect))
            pygame.draw.rect(fenetre, (40, 56, 82), rect, border_radius=8)
            pygame.draw.rect(fenetre, (90, 120, 175), rect, width=1, border_radius=8)
            fenetre.blit(self.police_texte.render(f"[{pygame.key.name(donnees['touche']).upper()}] {donnees['nom']}", True, (235, 235, 250)), (rect.x + 10, rect.y + 9))
            cd = f"Cooldown : {donnees['cooldown']:.1f}s" if donnees["cooldown"] > 0 else "Cooldown : pret"
            fenetre.blit(self.police_texte.render(cd, True, (180, 210, 245)), (rect.x + 10, rect.y + 32))
            couleur_cout = (255, 215, 120) if argent_joueur >= donnees["cout"] else (190, 125, 125)
            fenetre.blit(self.police_texte.render(f"Cout : {donnees['cout']} or", True, couleur_cout), (rect.right - 150, rect.y + 32))
            y += 74


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

    def gerer_clic(self, position_clic):
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.visible = False
            return None
        for cle, rect in self.boutons:
            if rect.collidepoint(position_clic):
                return cle
        if self.rect.collidepoint(position_clic):
            return "consomme"
        return None

    def dessiner(self, fenetre, inventaire_objets):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 135))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (24, 28, 36), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (150, 118, 70), self.rect, width=2, border_radius=12)
        fenetre.blit(self.police_titre.render("Objets utiles", True, (255, 230, 170)), (self.rect.x + 16, self.rect.y + 16))
        self.bouton_fermer.dessiner(fenetre)

        definitions = [
            ("potion_mur", "Potion de planches", "Restaure +2 vie mur"),
            ("bourse_or", "Bourse de secours", "Gagne +6 or"),
            ("totem_froid", "Totem de givre", "Ralentit tous les mobs 1.2s"),
        ]
        self.boutons = []
        y = self.rect.y + 72
        for cle, nom, desc in definitions:
            rect = pygame.Rect(self.rect.x + 20, y, self.rect.width - 40, 60)
            self.boutons.append((cle, rect))
            pygame.draw.rect(fenetre, (62, 47, 27), rect, border_radius=8)
            pygame.draw.rect(fenetre, (170, 135, 80), rect, width=1, border_radius=8)
            fenetre.blit(self.police_texte.render(f"{nom} x{inventaire_objets.get(cle, 0)}", True, (255, 240, 200)), (rect.x + 10, rect.y + 10))
            fenetre.blit(self.police_texte.render(desc, True, (230, 210, 170)), (rect.x + 10, rect.y + 32))
            y += 70


class PanneauInfos:
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

        if tour.type_tour == "Ralentissement":
            texte_special = f"Ralenti  : {int((1 - tour.facteur_ralentissement) * 100)}% / {tour.duree_ralentissement:.1f}s" # Affiche le pourcentage de ralentissement et la durée du ralentissement, s": applique à la tour de ralentissement
            fenetre.blit(self.police_info.render(texte_special, True, (100, 200, 255)), (pos_x, pos_y))
            pos_y += 24
        elif tour.type_tour == "Support":
            texte_special = f"Rayon buff : {int(tour.rayon_buff)} / Bonus : {int(tour.bonus_cadence_buff * 100)}%" # Affiche le rayon d'effet du buff et le bonus de cadence que la tour de support applique aux tours voisines
            fenetre.blit(self.police_info.render(texte_special, True, (255, 220, 80)), (pos_x, pos_y))
            pos_y += 24

        if tour.niveau >= niveau_max:
            surface_cout = self.police_info.render("Niveau maximum !", True, (255, 180, 50))
        else:
            surface_cout = self.police_info.render(f"Coût amélioration : {cout_amelioration} ¤", True, (130, 210, 130))
        fenetre.blit(surface_cout, (pos_x, pos_y))

        self.bouton_ameliorer.dessiner(fenetre)
        self.bouton_fermer.dessiner(fenetre)


class PanneauAchevement:
    """
    Fenêtre d'achèvement : affiche la progression du joueur dans chaque monde.
    4 mondes × 8 niveaux × 4 vagues.
    Les vagues terminées = vert foncé, les autres = gris.
    Chaque monde a son propre onglet.
    """

    # Noms des 4 mondes affichés dans les onglets
    noms_mondes = ["Pirate", "Japonais", "Médiéval", "Samouraï"]
    cles_mondes = ["pirate", "japonais", "medieval", "samourai"]

    def __init__(self):
        self.visible = False

        # Fenêtre centrée, assez grande pour afficher 8 niveaux × 4 vagues
        self.rect = pygame.Rect(
            largeur_ecran // 2 - 340,
            hauteur_ecran // 2 - 230,
            680,
            460
        )

        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)
        self.police_onglet = pygame.font.SysFont("consolas", 15, bold=True)
        self.police_label = pygame.font.SysFont("consolas", 13)

        # Progression : dictionnaire {cle_monde: [[bool×4] × 8]}
        # False = vague non terminée, True = vague terminée
        self.progression = {
            cle: [[False] * 4 for _ in range(8)]
            for cle in self.cles_mondes
        }

        # Quel onglet est actif (index dans cles_mondes)
        self.onglet_actif = 0

        # Bouton fermer en haut à droite
        self.bouton_fermer = Bouton(
            self.rect.right - 90,
            self.rect.y + 8,
            80, 30,
            "Fermer", 14
        )

        # Rectangles des onglets 
        self.rects_onglets = []
        largeur_onglet = self.rect.width // 4
        for i in range(4):
            rx = self.rect.x + i * largeur_onglet
            ry = self.rect.y + 48
            self.rects_onglets.append(pygame.Rect(rx, ry, largeur_onglet, 30))

    def ouvrir(self):
        self.visible = True

    def fermer(self):
        self.visible = False

    def terminer_vague(self, cle_monde, numero_niveau, numero_vague):
        """
        Marque une vague comme terminée.
        numero_niveau : 0 à 7
        numero_vague  : 0 à 3
        """
        if cle_monde in self.progression:
            self.progression[cle_monde][numero_niveau][numero_vague] = True

    def gerer_clic(self, position_clic):
        """Retourne True si le clic a été consommé (pour bloquer les clics derrière)"""
        if not self.visible:
            return False

        # Bouton fermer
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.fermer()
            return True

        # Clic sur un onglet
        for i, rect_onglet in enumerate(self.rects_onglets):
            if rect_onglet.collidepoint(position_clic):
                self.onglet_actif = i
                return True

        # Clic dans la fenêtre = consommé
        if self.rect.collidepoint(position_clic):
            return True

        return False

    def dessiner(self, fenetre):
        if not self.visible:
            return

        # Fond semi-transparent pour assombrir le reste de l'écran
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 120))
        fenetre.blit(voile, (0, 0))

        # Fond du panneau 
        pygame.draw.rect(fenetre, (22, 24, 38), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (80, 90, 150), self.rect, width=2, border_radius=12)

        # Titre
        surface_titre = self.police_titre.render("Achèvements", True, (220, 210, 255))
        fenetre.blit(surface_titre, (self.rect.x + 16, self.rect.y + 12))

        self.bouton_fermer.dessiner(fenetre)

        # Onglets des 4 mondes  
        for i, (nom, rect_onglet) in enumerate(zip(self.noms_mondes, self.rects_onglets)):
            if i == self.onglet_actif:
                # Onglet actif : fond clair
                pygame.draw.rect(fenetre, (60, 70, 120), rect_onglet)
                couleur_texte_onglet = (255, 255, 255)
            else:
                # Onglet inactif : fond sombre
                pygame.draw.rect(fenetre, (35, 38, 60), rect_onglet)
                couleur_texte_onglet = (150, 150, 180)

            pygame.draw.rect(fenetre, (80, 90, 140), rect_onglet, width=1)

            surface_onglet = self.police_onglet.render(nom, True, couleur_texte_onglet)
            fenetre.blit(surface_onglet, (
                rect_onglet.x + (rect_onglet.width - surface_onglet.get_width()) // 2,
                rect_onglet.y + (rect_onglet.height - surface_onglet.get_height()) // 2
            ))

        # Grille des niveaux et vagues
        # Zone de contenu sous les onglets
        zone_y_depart = self.rect.y + 88
        marge_gauche = self.rect.x + 30

        cle_monde = self.cles_mondes[self.onglet_actif]
        progression_monde = self.progression[cle_monde]

        # Taille de chaque petit rectangle de vague
        taille_rect_vague = 22
        espacement_vague = 6   # espacement entre les rectangles de vagues sur la même ligne
        espacement_niveau = 10  # espacement entre les lignes de niveaux

        # En-tête des colonnes (Vague 1, 2, 3, 4)
        for v in range(4):
            x_entete = marge_gauche + 80 + v * (taille_rect_vague + espacement_vague)
            surface_v = self.police_label.render(f"V{v+1}", True, (160, 160, 200))
            fenetre.blit(surface_v, (x_entete, zone_y_depart))

        # Lignes : une par niveau
        for niv in range(8):
            y_ligne = zone_y_depart + 20 + niv * (taille_rect_vague + espacement_niveau)

            # Label du niveau à gauche
            surface_niv = self.police_label.render(f"Niveau {niv + 1}", True, (200, 200, 200))
            fenetre.blit(surface_niv, (marge_gauche, y_ligne + 3))

            # 4 petits rectangles pour les 4 vagues
            for vague in range(4):
                x_rect = marge_gauche + 80 + vague * (taille_rect_vague + espacement_vague)

                # Vert foncé si terminé, gris sinon
                if progression_monde[niv][vague]:
                    couleur_rect = (0, 130, 0)   # vert foncé = terminé
                else:
                    couleur_rect = (100, 100, 110)  # gris = pas encore fait

                pygame.draw.rect(
                    fenetre, couleur_rect,
                    (x_rect, y_ligne, taille_rect_vague, taille_rect_vague),
                    border_radius=3
                )
                # Petit contour pour distinguer les cases
                pygame.draw.rect(
                    fenetre, (60, 60, 80),
                    (x_rect, y_ligne, taille_rect_vague, taille_rect_vague),
                    width=1, border_radius=3
                )

        # Légende en bas
        legende_y = self.rect.bottom - 28
        pygame.draw.rect(fenetre, (0, 130, 0), (marge_gauche, legende_y, 14, 14), border_radius=2)
        surface_leg1 = self.police_label.render("= Terminé", True, (180, 180, 180))
        fenetre.blit(surface_leg1, (marge_gauche + 18, legende_y))

        pygame.draw.rect(fenetre, (100, 100, 110), (marge_gauche + 120, legende_y, 14, 14), border_radius=2)
        surface_leg2 = self.police_label.render("= Non terminé", True, (180, 180, 180))
        fenetre.blit(surface_leg2, (marge_gauche + 138, legende_y))


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