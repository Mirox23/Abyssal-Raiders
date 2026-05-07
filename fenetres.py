import pygame
import random
from setting import largeur_ecran, hauteur_ecran, cout_amelioration, niveau_max
from interface import Bouton


class PanneauInfos:
    def __init__(self):
        self.visible = False
        self.tour_selectionnee = None
        self.police_info = pygame.font.SysFont("consolas", 18)
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)
        self.rect = pygame.Rect(largeur_ecran // 2 - 150, hauteur_ecran // 2 - 105, 300, 210)
        base_x = self.rect.x + 20
        base_y = self.rect.y + self.rect.height - 55
        self.bouton_ameliorer = Bouton(base_x, base_y, 82, 38, "Ameliorer", 14)
        self.bouton_revendre = Bouton(base_x + 92, base_y, 82, 38, "Revendre", 14)
        self.bouton_fermer = Bouton(base_x + 184, base_y, 82, 38, "Fermer", 14)

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
        if self.bouton_revendre.rect.collidepoint(position_clic):
            prix_revente = self.tour_selectionnee.valeur_revente() if hasattr(self.tour_selectionnee, "valeur_revente") else 5
            return "revendre", argent_joueur + prix_revente
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
        self.bouton_revendre.dessiner(fenetre)
        self.bouton_fermer.dessiner(fenetre)


class PanneauAchevement:
    noms_mondes = ["Pirate", "Samouraï", "Médiéval", "Démoniaque"]
    cles_mondes = ["pirate", "samourai", "medieval", "demoniaque"]

    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(largeur_ecran // 2 - 340, hauteur_ecran // 2 - 230, 680, 460)
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)
        self.police_onglet = pygame.font.SysFont("consolas", 15, bold=True)
        self.police_label = pygame.font.SysFont("consolas", 13)
        # 8 niveaux × 4 vagues
        self.progression = {cle: [[False] * 4 for _ in range(8)] for cle in self.cles_mondes}
        self.onglet_actif = 0
        self.progression_monde = None
        self.bouton_fermer = Bouton(self.rect.right - 90, self.rect.y + 8, 80, 30, "Fermer", 14)
        largeur_onglet = self.rect.width // 4
        self.rects_onglets = [pygame.Rect(self.rect.x + i * largeur_onglet, self.rect.y + 48, largeur_onglet, 30) for i in range(4)]

    def lier_progression_monde(self, progression_monde):
        self.progression_monde = progression_monde

    def ouvrir(self):
        self.visible = True

    def fermer(self):
        self.visible = False

    def marquer_vague(self, continent, numero_niveau, numero_vague):
        if continent not in self.progression:
            return
        if not (1 <= numero_niveau <= 8 and 1 <= numero_vague <= 4):
            return
        self.progression[continent][numero_niveau - 1][numero_vague - 1] = True
        if self.progression_monde and numero_vague <= 4:
            self.progression_monde.marquer_succes_vague(continent, numero_niveau, numero_vague)

    def marquer_niveau_conquis(self, continent, numero_niveau):
        if continent not in self.progression:
            return
        if not (1 <= numero_niveau <= 8):
            return
        for i in range(4):
            self.progression[continent][numero_niveau - 1][i] = True
        if self.progression_monde:
            self.progression_monde.marquer_conquis(continent, numero_niveau)

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
        fenetre.blit(self.police_titre.render("Succes", True, (220, 210, 255)), (self.rect.x + 16, self.rect.y + 12))
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
        if self.progression_monde:
            cle = self.cles_mondes[self.onglet_actif]
            for niv in range(8):
                succes = self.progression_monde.succes_niveau(cle, niv + 1)
                for v in range(4):
                    progression_monde[niv][v] = succes[v]
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

        # Légende en bas (comme avant)
        legende_y = self.rect.bottom - 28
        pygame.draw.rect(fenetre, (0, 130, 0), (marge_gauche, legende_y, 14, 14), border_radius=2)
        fenetre.blit(self.police_label.render("= Conquis", True, (180, 180, 180)), (marge_gauche + 18, legende_y))
        pygame.draw.rect(fenetre, (100, 100, 110), (marge_gauche + 120, legende_y, 14, 14), border_radius=2)
        fenetre.blit(self.police_label.render("= Pas encore conquis", True, (180, 180, 180)), (marge_gauche + 138, legende_y))


class EcranFinVague:
    def __init__(self):
        self.visible = False
        self.numero_vague = 0
        self.xp_gagnee = 0
        self.score_vague = 0
        self.police_titre = pygame.font.SysFont("consolas", 30, bold=True)
        self.police_message = pygame.font.SysFont("consolas", 19)
        self.police_xp = pygame.font.SysFont("consolas", 16)
        centre_x = largeur_ecran // 2
        centre_y = hauteur_ecran // 2
        self.rect = pygame.Rect(centre_x - 250, centre_y - 115, 500, 230)
        self.bouton_nouvelle_vague = Bouton(centre_x - 230, centre_y + 60, 210, 44, "Nouvelle vague", 18)
        self.bouton_modification = Bouton(centre_x + 20, centre_y + 60, 210, 44, "Modification", 18)

    def ouvrir(self, numero, xp_gagnee, score_vague):
        self.numero_vague = numero
        self.xp_gagnee = xp_gagnee
        self.score_vague = score_vague
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
        surface_score = self.police_xp.render(f"Score de vague : {self.score_vague}", True, (255, 220, 120))
        fenetre.blit(surface_score, (centre_x - surface_score.get_width() // 2, self.rect.y + 112))
        self.bouton_nouvelle_vague.dessiner(fenetre)
        self.bouton_modification.dessiner(fenetre)


class FenetreNiveauConquis:
    def __init__(self):
        self.visible = False
        self.police_titre = pygame.font.SysFont("consolas", 28, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 15)
        self.rect = pygame.Rect(largeur_ecran // 2 - 320, hauteur_ecran // 2 - 120, 640, 240)
        self.bouton_niveau_suivant = Bouton(self.rect.x + 40, self.rect.bottom - 60, 260, 44, "Niveau suivant", 18)
        self.bouton_retour = Bouton(self.rect.right - 300, self.rect.bottom - 60, 260, 44, "Retour a la map", 18)

    def ouvrir(self):
        self.visible = True

    def gerer_clic(self, position_clic):
        if not self.visible:
            return None
        if self.bouton_niveau_suivant.rect.collidepoint(position_clic):
            self.visible = False
            return "niveau_suivant"
        if self.bouton_retour.rect.collidepoint(position_clic):
            self.visible = False
            return "retour_map"
        if self.rect.collidepoint(position_clic):
            return "consomme"
        return None

    def dessiner(self, fenetre):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 150))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (28, 32, 46), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (100, 120, 200), self.rect, width=2, border_radius=12)
        titre = self.police_titre.render("Bravo ! Niveau conquis !", True, (210, 200, 80))
        fenetre.blit(titre, (self.rect.centerx - titre.get_width() // 2, self.rect.y + 26))
        ligne = "Vous avez maintenant les compétences pour vous attaquer au niveau suivant."
        txt = self.police_texte.render(ligne, True, (210, 210, 220))
        fenetre.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.y + 80))
        self.bouton_niveau_suivant.dessiner(fenetre)
        self.bouton_retour.dessiner(fenetre)



# Marché entre les vagues

CATALOGUE_CARTES = [
    {"id": "or_bonus", "nom": "+20 Or", "desc": "Coffre de butin pirate", "cout": 0,  "couleur": (200, 170, 40)},
    {"id": "soin_mur", "nom": "+3 Vie mur","desc": "Planches de renfort", "cout": 0,  "couleur": (80, 180, 100)},
    {"id": "tour_gratuite", "nom": "Tour offerte", "desc": "Pose une tour sans payer", "cout": 0, "couleur": (100, 140, 220)},
    {"id": "cadence_bonus", "nom": "Cadence +15%", "desc": "Huile de mecanique magique", "cout": 0, "couleur": (220, 120, 50)},
    {"id": "portee_bonus", "nom": "Portée +20","desc": "Longue-vue enchantée", "cout": 0, "couleur": (160, 80, 200)},
    {"id": "xp_bonus", "nom": "+25 XP", "desc": "Parchemin de sagesse", "cout": 0, "couleur": (80, 200, 210)},
    {"id": "argent_double", "nom": "Primes x2 (vague)", "desc": "Contrat de mercenaire", "cout": 0, "couleur": (255, 200, 0)},
    {"id": "gel_global", "nom": "Gel de zone", "desc": "Blizzard instantané", "cout": 0, "couleur": (150, 200, 255)},
]


class FenetreMarcheVague:
    """
    Marché entre les vagues : 3 cartes aléatoires apparaissent,
    le joueur en choisit UNE. Puis il clique 'Continuer'.
    """

    def __init__(self):
        self.visible = False
        self.cartes_proposees = []
        self.carte_choisie = None
        self.rect = pygame.Rect(largeur_ecran // 2 - 360, hauteur_ecran // 2 - 200, 720, 400)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_nom = pygame.font.SysFont("consolas", 16, bold=True)
        self.police_desc = pygame.font.SysFont("consolas", 13)
        self.bouton_continuer = Bouton(self.rect.centerx - 110, self.rect.bottom - 52, 220, 40, "Continuer", 17)
        self._rects_cartes = []

    def ouvrir(self):
        self.visible = True
        self.carte_choisie = None
        self.cartes_proposees = random.sample(CATALOGUE_CARTES, min(3, len(CATALOGUE_CARTES)))
        largeur_carte = 190
        espacement = 30
        total = largeur_carte * 3 + espacement * 2
        depart_x = self.rect.centerx - total // 2
        self._rects_cartes = [
            pygame.Rect(depart_x + i * (largeur_carte + espacement), self.rect.y + 65, largeur_carte, 240)
            for i in range(3)
        ]

    def fermer(self):
        self.visible = False

    def gerer_clic(self, pos):
        if not self.visible:
            return None
        # Sélection d'une carte
        for i, rect in enumerate(self._rects_cartes):
            if rect.collidepoint(pos):
                self.carte_choisie = i
                return None
        # Bouton continuer : Attention ! ne fonctionne que si une carte est choisie
        if self.bouton_continuer.rect.collidepoint(pos) and self.carte_choisie is not None:
            carte = self.cartes_proposees[self.carte_choisie]
            self.fermer()
            return carte["id"]
        return None

    def dessiner(self, fenetre):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 155))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (18, 22, 36), self.rect, border_radius=14)
        pygame.draw.rect(fenetre, (100, 130, 200), self.rect, width=2, border_radius=14)
        titre = self.police_titre.render("⚓ Marché du butin : choisissez une récompense", True, (220, 210, 80))
        fenetre.blit(titre, (self.rect.centerx - titre.get_width() // 2, self.rect.y + 14))

        for i, (carte, rect) in enumerate(zip(self.cartes_proposees, self._rects_cartes)):
            selectionne = i == self.carte_choisie
            couleur_fond = (35, 42, 62) if not selectionne else (50, 60, 95)
            couleur_bord = carte["couleur"] if selectionne else (70, 85, 130)
            epaisseur_bord = 3 if selectionne else 1
            pygame.draw.rect(fenetre, couleur_fond, rect, border_radius=12)
            pygame.draw.rect(fenetre, couleur_bord, rect, width=epaisseur_bord, border_radius=12)

            # Icone de couleur en haut
            pygame.draw.rect(fenetre, carte["couleur"], pygame.Rect(rect.x + 16, rect.y + 18, rect.width - 32, 50), border_radius=8)

            surf_nom = self.police_nom.render(carte["nom"], True, (255, 255, 255) if selectionne else (210, 210, 210))
            fenetre.blit(surf_nom, (rect.centerx - surf_nom.get_width() // 2, rect.y + 82))
            surf_desc = self.police_desc.render(carte["desc"], True, (170, 185, 210))
            fenetre.blit(surf_desc, (rect.centerx - surf_desc.get_width() // 2, rect.y + 108))

            if selectionne:
                surf_ok = self.police_desc.render("✓ Sélectionnée", True, (130, 230, 140))
                fenetre.blit(surf_ok, (rect.centerx - surf_ok.get_width() // 2, rect.y + 135))

        if self.carte_choisie is not None:
            self.bouton_continuer.dessiner(fenetre)
        else:
            # Bouton grisé
            pygame.draw.rect(fenetre, (50, 55, 70), self.bouton_continuer.rect, border_radius=5)
            surf = self.police_desc.render("Choisissez une carte", True, (130, 130, 150))
            fenetre.blit(surf, (self.bouton_continuer.rect.centerx - surf.get_width() // 2,
                                self.bouton_continuer.rect.centery - surf.get_height() // 2))

# Tableau des meilleurs scores

class FenetreScores:
    """Affiche le top 5 global + meilleurs temps par vague."""

    def __init__(self):
        self.visible = False
        self.continent = "pirate"
        self.rect = pygame.Rect(largeur_ecran // 2 - 280, hauteur_ecran // 2 - 200, 560, 400)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_ligne = pygame.font.SysFont("consolas", 15)
        self.police_petit = pygame.font.SysFont("consolas", 12)
        self.bouton_fermer = Bouton(self.rect.right - 90, self.rect.y + 10, 78, 30, "Fermer", 13)
        self.scores = []
        self.meilleurs_par_vague = {}

    def ouvrir(self, continent):
        from scores import obtenir_scores, obtenir_meilleurs_par_vague
        self.continent = continent
        self.scores = obtenir_scores(continent)
        self.meilleurs_par_vague = obtenir_meilleurs_par_vague(continent)
        self.visible = True

    def fermer(self):
        self.visible = False

    def gerer_clic(self, pos):
        if not self.visible:
            return False
        if self.bouton_fermer.rect.collidepoint(pos):
            self.fermer()
            return True
        return self.rect.collidepoint(pos)

    def dessiner(self, fenetre):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 140))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (20, 24, 38), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (90, 120, 180), self.rect, width=2, border_radius=12)

        nom_continent = self.continent.capitalize()
        titre = self.police_titre.render(f"🏆 Meilleurs scores — {nom_continent}", True, (220, 200, 80))
        fenetre.blit(titre, (self.rect.centerx - titre.get_width() // 2, self.rect.y + 14))
        self.bouton_fermer.dessiner(fenetre)

        # En-têtes
        entetes_y = self.rect.y + 58
        fenetre.blit(self.police_petit.render("#", True, (160, 160, 200)), (self.rect.x + 30, entetes_y))
        fenetre.blit(self.police_petit.render("Score", True, (160, 160, 200)), (self.rect.x + 80, entetes_y))
        fenetre.blit(self.police_petit.render("Niveau", True, (160, 160, 200)), (self.rect.x + 220, entetes_y))
        fenetre.blit(self.police_petit.render("Niv. joueur", True, (160, 160, 200)), (self.rect.x + 340, entetes_y))
        pygame.draw.line(fenetre, (70, 80, 120), (self.rect.x + 20, entetes_y + 18), (self.rect.right - 20, entetes_y + 18))

        if not self.scores:
            msg = self.police_ligne.render("Aucun score enregistré pour ce continent.", True, (160, 160, 180))
            fenetre.blit(msg, (self.rect.centerx - msg.get_width() // 2, self.rect.centery - 10))
        else:
            medailles = ["🥇", "🥈", "🥉", "4.", "5."]
            for i, entree in enumerate(self.scores[:5]):
                y_ligne = entetes_y + 30 + i * 44
                couleur = (255, 220, 80) if i == 0 else (200, 200, 215)
                fond_rect = pygame.Rect(self.rect.x + 18, y_ligne - 4, self.rect.width - 36, 38)
                pygame.draw.rect(fenetre, (30, 36, 55) if i % 2 == 0 else (26, 30, 46), fond_rect, border_radius=6)
                medaille = medailles[i] if i < 3 else medailles[i]
                fenetre.blit(self.police_ligne.render(medaille, True, couleur), (self.rect.x + 25, y_ligne + 6))
                fenetre.blit(self.police_ligne.render(str(entree["score"]), True, couleur), (self.rect.x + 75, y_ligne + 6))
                fenetre.blit(self.police_ligne.render(f"Niv. {entree['niveau']}", True, (200, 210, 230)), (self.rect.x + 215, y_ligne + 6))
                fenetre.blit(self.police_ligne.render(f"Joueur Niv. {entree['niveau_joueur']}", True, (180, 195, 215)), (self.rect.x + 335, y_ligne + 6))

        titre_vague = self.police_petit.render("Meilleurs temps par vague :", True, (200, 200, 220))
        fenetre.blit(titre_vague, (self.rect.x + 24, self.rect.bottom - 110))
        for numero_vague in range(1, 5):
            infos = self.meilleurs_par_vague.get(str(numero_vague))
            if infos:
                texte = f"Vague {numero_vague} : {infos['temps']} s - {infos.get('nom_joueur', 'Joueur')}"
                couleur = (180, 230, 180)
            else:
                texte = f"Vague {numero_vague} : aucun score"
                couleur = (145, 155, 180)
            fenetre.blit(
                self.police_petit.render(texte, True, couleur),
                (self.rect.x + 26 + ((numero_vague - 1) % 2) * 260, self.rect.bottom - 88 + ((numero_vague - 1) // 2) * 22),
            )
