import os
import pygame
from setting import largeur_ecran, hauteur_ecran
from interface import Bouton


#  Fenêtre de récompenses de niveau + arbre à talents 

class FenetreRecompenses:
    """
    Affiche les récompenses d'or débloquées à chaque niveau.
    Les récompenses sont infinies : tous les 8 niveaux on repart sur un cycle
    avec des montants un peu plus élevés.
    """

    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(200, 80, 600, 420)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.police_petite = pygame.font.SysFont("consolas", 12)
        self.bouton_fermer = Bouton(self.rect.right - 100, self.rect.y + 12, 84, 30, "Fermer", 14)
        self.niveaux_recuperes = set()   # clés = (cycle, rang) pour être infini
        self._boutons_recompenses = []

    def _calcul_recompense(self, numero_niveau_joueur):
        """
        Calcule le montant d'or pour le niveau joueur donné.
        Tous les 8 niveaux = 1 cycle. Chaque cycle est un peu plus généreux.
        """
        cycle = (numero_niveau_joueur - 1) // 8       # 0, 1, 2 …
        rang = (numero_niveau_joueur - 1) % 8 + 1     # 1 à 8
        base = 8 + rang * 2                            # 10 à 24 comme avant
        bonus_cycle = cycle * 4                        # +4 par cycle
        return base + bonus_cycle

    def _generer_lignes(self, niveau_joueur):
        """
        Génère la liste des 8 prochains paliers à partir du niveau actuel.
        On affiche les 8 niveaux qui entourent le niveau courant.
        """
        debut = max(1, niveau_joueur - 2)
        return [(debut + i, self._calcul_recompense(debut + i)) for i in range(8)]

    def ouvrir(self):
        self.visible = True

    def gerer_clic(self, pos_clic, progression):
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(pos_clic):
            self.visible = False
            return ("fermer", None)
        for niv, montant, rect in self._boutons_recompenses:
            cle = niv   # chaque niveau = clé unique infinie
            peut_recuperer = progression.niveau >= niv and cle not in self.niveaux_recuperes
            if rect.collidepoint(pos_clic) and peut_recuperer:
                self.niveaux_recuperes.add(cle)
                return ("recompense", montant)
        if self.rect.collidepoint(pos_clic):
            return ("consomme", None)
        return None

    def dessiner(self, fenetre, progression):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA) #SRCALPHA pour transparence
        voile.fill((0, 0, 0, 150))
        fenetre.blit(voile, (0, 0)) 

        pygame.draw.rect(fenetre, (20, 25, 40), self.rect, border_radius=14)
        pygame.draw.rect(fenetre, (90, 120, 175), self.rect, width=2, border_radius=14)

        titre = self.police_titre.render("Récompenses de niveau", True, (220, 230, 255))
        fenetre.blit(titre, (self.rect.x + 14, self.rect.y + 14))

        sous = self.police_petite.render(
            f"Niveau joueur actuel : {progression.niveau}  |  Points talent disponibles : {progression.points_talent}",
            True, (255, 220, 130)
        )
        fenetre.blit(sous, (self.rect.x + 14, self.rect.y + 44))
        self.bouton_fermer.dessiner(fenetre)

        lignes = self._generer_lignes(progression.niveau)
        self._boutons_recompenses = []
        y = self.rect.y + 72

        for niv, montant in lignes:
            rect_btn = pygame.Rect(self.rect.x + 20, y, self.rect.width - 40, 32)
            self._boutons_recompenses.append((niv, montant, rect_btn))

            deja = niv in self.niveaux_recuperes
            peut = progression.niveau >= niv and not deja

            if deja:
                couleur = (45, 86, 58)
            elif peut:
                couleur = (22, 102, 68)
            else:
                couleur = (60, 60, 70)

            pygame.draw.rect(fenetre, couleur, rect_btn, border_radius=6)
            pygame.draw.rect(fenetre, (80, 100, 140), rect_btn, width=1, border_radius=6)

            texte = f"Niveau {niv:3}  →  +{montant} or"
            if deja:
                texte += "  ✓ récupéré"
            elif not peut:
                texte += "  (verrouillé)"

            coul_txt = (200, 210, 200) if deja else (230, 235, 230) if peut else (130, 130, 140)
            fenetre.blit(self.police_texte.render(texte, True, coul_txt), (rect_btn.x + 12, rect_btn.y + 8))
            y += 40


#  Fenêtre arbre à talents (séparée des récompenses)


class FenetreArbreTalents:
    """
    Arbre à talents avec icônes PNG (dossier image/talent/).
    L'arbre se reset à chaque nouveau niveau de jeu, mais le joueur
    repart avec un petit bonus permanent basé sur son niveau précédent.
    """

    TALENTS = {
        "degats_competence": {
            "nom": "Poudre noire +",
            "icone": "image/talent/poudre_noire.png",
            "max": 4,
            "desc_courte": "+2 dégâts par compétence",
            "desc_longue": "Chaque niveau ajoute +2 dégâts\nà toutes vos compétences actives.",
        },
        "reduction_cout": {
            "nom": "Marchandage pirate",
            "icone": "image/talent/marchandage.png",
            "max": 3,
            "desc_courte": "-1 coût par compétence",
            "desc_longue": "Réduit de 1 or le coût\nde chaque compétence utilisée.",
        },
        "chasseur": {
            "nom": "Chasseur de prime",
            "icone": "image/talent/chasseur.png",
            "max": 3,
            "desc_courte": "+1 or bonus mobs rapides",
            "desc_longue": "Les mobs rapides et kamikazes\nvous rapportent +1 or à la mort.",
        },
        "ingenieur": {
            "nom": "Ingénieur de guilde",
            "icone": "image/talent/ingenieur.png",
            "max": 3,
            "desc_courte": "+8 portée à toutes les tours",
            "desc_longue": "Chaque niveau augmente\nla portée de toutes vos tours de 8.",
        },
        "resistance_mur": {
            "nom": "Mur renforcé",
            "icone": "image/talent/mur_renforce.png",
            "max": 3,
            "desc_courte": "-1 dégât reçu par le mur",
            "desc_longue": "Le mur absorbe 1 dégât\nde plus par niveau de talent.",
        },
        "alchimiste": {
            "nom": "Alchimiste fou",
            "icone": "image/talent/alchimiste.png",
            "max": 2,
            "desc_courte": "Effets des objets ×1.5",
            "desc_longue": "Tous vos objets (potions,\nbourses…) ont un effet amplifié.",
        },
    }

    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(120, 60, 760, 470)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_nom = pygame.font.SysFont("consolas", 13, bold=True)
        self.police_desc = pygame.font.SysFont("consolas", 11)
        self.police_niv = pygame.font.SysFont("consolas", 12)
        self.bouton_fermer = Bouton(self.rect.right - 100, self.rect.y + 12, 84, 30, "Fermer", 14)

        # État des talents : niveau actuel pour chaque talent
        self.talents = {cle: {"niveau": 0, "max": d["max"]} for cle, d in self.TALENTS.items()}

        # Icônes chargées une seule fois
        self._icones = {}
        self._charger_icones()

        self._boutons_talents = []
        self._maj_boutons()

    def _charger_icones(self):
        taille = (48, 48)
        for cle, donnees in self.TALENTS.items():
            chemin = donnees["icone"]
            if os.path.exists(chemin):
                try:
                    img = pygame.image.load(chemin).convert_alpha()
                    self._icones[cle] = pygame.transform.smoothscale(img, taille)
                except Exception:
                    self._icones[cle] = None
            else:
                self._icones[cle] = None

    def _maj_boutons(self):
        self._boutons_talents = []
        cols = 3
        larg_carte = 220
        haut_carte = 130
        marge_x = 18
        marge_y = 14
        depart_x = self.rect.x + 20
        depart_y = self.rect.y + 80

        for i, cle in enumerate(self.TALENTS):
            col = i % cols
            lig = i // cols
            bx = depart_x + col * (larg_carte + marge_x)
            by = depart_y + lig * (haut_carte + marge_y)
            self._boutons_talents.append((cle, pygame.Rect(bx, by, larg_carte, haut_carte)))

    def ouvrir(self):
        self.visible = True

    def reset_pour_nouveau_niveau(self, niveau_joueur_avant):
        """
        Remet tous les talents à 0 mais applique un petit bonus permanent
        qu'on retournera à game.py pour qu'il l'ajoute à talents_appliques.
        """
        for cle in self.talents:
            self.talents[cle]["niveau"] = 0
        # bonus permanent : +1 degats tous les 4 niveaux, +1 portée tous les 5 niveaux
        bonus_degats = niveau_joueur_avant // 4
        bonus_portee = niveau_joueur_avant // 5
        return bonus_degats, bonus_portee

    def gerer_clic(self, pos_clic, progression):
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(pos_clic):
            self.visible = False
            return ("fermer", None)
        for cle, rect in self._boutons_talents:
            t = self.talents[cle]
            if rect.collidepoint(pos_clic):
                if progression.points_talent > 0 and t["niveau"] < t["max"]:
                    progression.points_talent -= 1
                    t["niveau"] += 1
                    return ("talent", cle)
        if self.rect.collidepoint(pos_clic):
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

        titre = self.police_titre.render("Arbre à talents", True, (220, 230, 255))
        fenetre.blit(titre, (self.rect.x + 14, self.rect.y + 14))

        pts_txt = self.police_desc.render(
            f"Points disponibles : {progression.points_talent}  —  Bonus permanent : +{progression.bonus_degats_permanent} dégâts / +{progression.bonus_portee_permanent} portée",
            True, (255, 220, 130)
        )
        fenetre.blit(pts_txt, (self.rect.x + 14, self.rect.y + 44))
        self.bouton_fermer.dessiner(fenetre)

        for cle, rect in self._boutons_talents:
            t = self.talents[cle]
            info = self.TALENTS[cle]
            peut = progression.points_talent > 0 and t["niveau"] < t["max"]
            maximal = t["niveau"] >= t["max"]

            # Fond de la carte
            coul_fond = (26, 34, 52)
            coul_bord = (200, 170, 60) if maximal else (140, 190, 100) if peut else (70, 90, 130)
            pygame.draw.rect(fenetre, coul_fond, rect, border_radius=10)
            pygame.draw.rect(fenetre, coul_bord, rect, width=2 if (peut or maximal) else 1, border_radius=10)

            # Icône
            icone = self._icones.get(cle)
            if icone:
                fenetre.blit(icone, (rect.x + 8, rect.y + 8))
                tx = rect.x + 64
            else:
                # Carré de couleur de remplacement si pas d'icône
                pygame.draw.rect(fenetre, (50, 70, 110), pygame.Rect(rect.x + 8, rect.y + 8, 48, 48), border_radius=6)
                tx = rect.x + 64

            # Nom du talent
            surf_nom = self.police_nom.render(info["nom"], True, (235, 240, 255))
            fenetre.blit(surf_nom, (tx, rect.y + 10))

            # Description courte
            surf_desc = self.police_desc.render(info["desc_courte"], True, (160, 200, 240))
            fenetre.blit(surf_desc, (tx, rect.y + 28))

            # Description longue (2 lignes)
            lignes = info["desc_longue"].split("\n")
            for j, ligne in enumerate(lignes):
                s = self.police_desc.render(ligne, True, (130, 150, 180))
                fenetre.blit(s, (rect.x + 10, rect.y + 68 + j * 14))

            # Barre de niveaux (petits carrés)
            for k in range(t["max"]):
                cx = rect.x + 10 + k * 18
                cy = rect.y + rect.height - 22
                coul = (255, 220, 60) if k < t["niveau"] else (50, 60, 80)
                pygame.draw.rect(fenetre, coul, (cx, cy, 14, 10), border_radius=2)
                pygame.draw.rect(fenetre, (80, 100, 140), (cx, cy, 14, 10), width=1, border_radius=2)

            # Texte niv actuel
            niv_txt = f"Niv {t['niveau']}/{t['max']}"
            coul_niv = (255, 200, 50) if t["niveau"] > 0 else (120, 130, 150)
            if maximal:
                niv_txt = "MAX"
                coul_niv = (255, 180, 40)
            s_niv = self.police_niv.render(niv_txt, True, coul_niv)
            fenetre.blit(s_niv, (rect.right - s_niv.get_width() - 8, rect.bottom - 20))


#  Classe de compatibilité : garde l'ancien nom utilisé dans game.py et ui.py


class FenetreRecompensesTalents:
    """
    Classe de compatibilité qui encapsule FenetreRecompenses + FenetreArbreTalents.
    game.py l'utilise via l'ancien nom, on délègue les appels aux deux nouvelles fenêtres.
    """

    def __init__(self):
        self.fenetre_recompenses = FenetreRecompenses()
        self.fenetre_talents = FenetreArbreTalents()
        # Alias pour que game.py puisse lire talents directement
        self.talents = self.fenetre_talents.talents
        self.visible = False
        self._onglet = "recompenses"   # "recompenses" ou "talents"
        self.rect = pygame.Rect(110, 50, 780, 500)
        self.police_onglet = pygame.font.SysFont("consolas", 15, bold=True)
        self.rect_onglet_recomp = pygame.Rect(self.rect.x, self.rect.y - 36, 190, 36)
        self.rect_onglet_talent = pygame.Rect(self.rect.x + 196, self.rect.y - 36, 190, 36)

    def ouvrir(self):
        self.visible = True
        self.fenetre_recompenses.visible = True
        self.fenetre_talents.visible = False
        self._onglet = "recompenses"

    def gerer_clic(self, pos_clic, progression):
        if not self.visible:
            return None

        # Clic sur les onglets
        if self.rect_onglet_recomp.collidepoint(pos_clic):
            self._onglet = "recompenses"
            self.fenetre_recompenses.visible = True
            self.fenetre_talents.visible = False
            return ("consomme", None)
        if self.rect_onglet_talent.collidepoint(pos_clic):
            self._onglet = "talents"
            self.fenetre_recompenses.visible = False
            self.fenetre_talents.visible = True
            return ("onglet_talent", None)

        # Déléguer au bon panneau
        if self._onglet == "recompenses":
            action = self.fenetre_recompenses.gerer_clic(pos_clic, progression)
        else:
            action = self.fenetre_talents.gerer_clic(pos_clic, progression)

        if action and action[0] == "fermer":
            self.visible = False
            self.fenetre_recompenses.visible = False
            self.fenetre_talents.visible = False

        return action

    def dessiner(self, fenetre, progression):
        if not self.visible:
            return

        # Dessiner les onglets
        for label, rect_ong, onglet_cle in [
            ("Récompenses", self.rect_onglet_recomp, "recompenses"),
            ("Arbre à talents", self.rect_onglet_talent, "talents"),
        ]:
            actif = self._onglet == onglet_cle
            pygame.draw.rect(fenetre, (30, 40, 62) if actif else (20, 26, 40), rect_ong, border_radius=6)
            pygame.draw.rect(fenetre, (90, 120, 175) if actif else (50, 65, 95), rect_ong, width=1, border_radius=6)
            surf = self.police_onglet.render(label, True, (220, 230, 255) if actif else (130, 145, 175))
            fenetre.blit(surf, (rect_ong.centerx - surf.get_width() // 2, rect_ong.centery - surf.get_height() // 2))

        if self._onglet == "recompenses":
            self.fenetre_recompenses.dessiner(fenetre, progression)
        else:
            self.fenetre_talents.dessiner(fenetre, progression)

    def reset_pour_nouveau_niveau(self, niveau_joueur_avant):
        """Appelé par game.py à chaque nouveau niveau de jeu."""
        return self.fenetre_talents.reset_pour_nouveau_niveau(niveau_joueur_avant)


# Les autres fenêtres (compétences, objets) sont indépendantes et plus simples.

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

    def dessiner(self, fenetre, gestionnaire_competences, argent_joueur, reduction_cout):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 135))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (20, 26, 40), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (95, 125, 180), self.rect, width=2, border_radius=12)
        fenetre.blit(self.police_titre.render("Compétences du Pirate", True, (220, 230, 255)), (self.rect.x + 16, self.rect.y + 16))
        self.bouton_fermer.dessiner(fenetre)
        self.boutons = []
        y = self.rect.y + 70
        for cle, donnees in gestionnaire_competences.competences.items():
            rect = pygame.Rect(self.rect.x + 18, y, self.rect.width - 36, 64)
            self.boutons.append((cle, rect))
            cout_reel = max(1, donnees["cout"] - reduction_cout)
            en_cooldown = donnees["cooldown"] > 0
            assez_argent = argent_joueur >= cout_reel
            peut_utiliser = (not en_cooldown) and assez_argent
            coul_fond = (30, 84, 62) if peut_utiliser else (40, 56, 82)
            pygame.draw.rect(fenetre, coul_fond, rect, border_radius=8)
            pygame.draw.rect(fenetre, (90, 120, 175), rect, width=1, border_radius=8)
            fenetre.blit(self.police_texte.render(f"[{pygame.key.name(donnees['touche']).upper()}] {donnees['nom']}", True, (235, 235, 250)), (rect.x + 10, rect.y + 9))
            cd = f"Cooldown : {donnees['cooldown']:.1f}s" if donnees["cooldown"] > 0 else "Cooldown : prêt"
            fenetre.blit(self.police_texte.render(cd, True, (180, 210, 245)), (rect.x + 10, rect.y + 32))
            coul_cout = (255, 215, 120) if assez_argent else (190, 125, 125)
            fenetre.blit(self.police_texte.render(f"Coût : {cout_reel} or", True, coul_cout), (rect.right - 160, rect.y + 12))
            if peut_utiliser:
                statut, coul_s = "Utilisable", (135, 240, 170)
            elif en_cooldown:
                statut, coul_s = "En cooldown", (240, 180, 110)
            else:
                statut, coul_s = "Pas assez d'or", (235, 130, 130) # rouge vif, coul_s : couleur du statut à droite
            fenetre.blit(self.police_texte.render(statut, True, coul_s), (rect.right - 220, rect.y + 34))
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
        pygame.draw.rect(fenetre, (24, 28, 36), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (150, 118, 70), self.rect, width=2, border_radius=12)
        fenetre.blit(self.police_titre.render("Objets utiles", True, (255, 230, 170)), (self.rect.x + 16, self.rect.y + 16))
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
            pygame.draw.rect(fenetre, (62, 47, 27) if utilisable else (52, 42, 38), rect, border_radius=8)
            pygame.draw.rect(fenetre, (170, 135, 80), rect, width=1, border_radius=8)
            coul_qte = (255, 240, 200) if utilisable else (180, 160, 145)
            fenetre.blit(self.police_texte.render(f"{nom} x{qte}", True, coul_qte), (rect.x + 10, rect.y + 10))
            fenetre.blit(self.police_texte.render(desc, True, (230, 210, 170)), (rect.x + 10, rect.y + 32))
            statut = "Utilisable" if utilisable else "Stock vide"
            coul_s = (125, 230, 150) if utilisable else (230, 130, 120)
            fenetre.blit(self.police_texte.render(statut, True, coul_s), (rect.right - 120, rect.y + 10))
            y += 70


class PanneauParametresMusique:
    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(260, 130, 480, 290)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.bouton_fermer = Bouton(self.rect.right - 94, self.rect.y + 12, 78, 28, "Fermer", 14)
        self.bouton_moins  = pygame.Rect(self.rect.x + 70,  self.rect.y + 98,  48, 42)
        self.bouton_plus = pygame.Rect(self.rect.x + 312, self.rect.y + 98,  48, 42)
        self.bouton_moins_effets = pygame.Rect(self.rect.x + 70,  self.rect.y + 165, 48, 42)
        self.bouton_plus_effets = pygame.Rect(self.rect.x + 312, self.rect.y + 165, 48, 42)
        self.bouton_x15 = pygame.Rect(self.rect.x + 110, self.rect.y + 225, 110, 36)
        self.bouton_x2  = pygame.Rect(self.rect.x + 250, self.rect.y + 225, 110, 36)

    def ouvrir(self):
        self.visible = True

    def gerer_clic(self, pos_clic):
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(pos_clic):
            self.visible = False
            return None
        if self.bouton_moins.collidepoint(pos_clic): return "moins"
        if self.bouton_plus.collidepoint(pos_clic): return "plus"
        if self.bouton_moins_effets.collidepoint(pos_clic): return "moins_effets"
        if self.bouton_plus_effets.collidepoint(pos_clic): return "plus_effets"
        if self.bouton_x15.collidepoint(pos_clic): return "vitesse_x15"
        if self.bouton_x2.collidepoint(pos_clic): return "vitesse_x2"
        if self.rect.collidepoint(pos_clic): return "consomme"
        return None

    def dessiner(self, fenetre, volume, volume_effets, vitesse_jeu=1.0):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 130))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (25, 30, 46), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (96, 126, 184), self.rect, width=2, border_radius=12)
        fenetre.blit(self.police_titre.render("Paramètres musique", True, (220, 235, 255)), (self.rect.x + 16, self.rect.y + 16))
        self.bouton_fermer.dessiner(fenetre)
        for btn in (self.bouton_moins, self.bouton_plus):
            pygame.draw.rect(fenetre, (95, 65, 50), btn, border_radius=7)
        fenetre.blit(self.police_titre.render("-", True, (255, 220, 180)), (self.bouton_moins.x + 15, self.bouton_moins.y + 2))
        fenetre.blit(self.police_titre.render("+", True, (255, 220, 180)), (self.bouton_plus.x + 13,  self.bouton_plus.y + 2))
        fenetre.blit(self.police_texte.render(f"Volume musique : {int(volume * 100)}%", True, (205, 225, 255)), (self.rect.x + 145, self.rect.y + 78))
        barre = pygame.Rect(self.rect.x + 140, self.rect.y + 114, 150, 14)
        pygame.draw.rect(fenetre, (42, 48, 65), barre, border_radius=6)
        pygame.draw.rect(fenetre, (100, 200, 130), (barre.x, barre.y, int(barre.width * volume), barre.height), border_radius=6)
        for btn in (self.bouton_moins_effets, self.bouton_plus_effets):
            pygame.draw.rect(fenetre, (95, 65, 50), btn, border_radius=7)
        fenetre.blit(self.police_titre.render("-", True, (255, 220, 180)), (self.bouton_moins_effets.x + 15, self.bouton_moins_effets.y + 2))
        fenetre.blit(self.police_titre.render("+", True, (255, 220, 180)), (self.bouton_plus_effets.x + 13,  self.bouton_plus_effets.y + 2))
        fenetre.blit(self.police_texte.render(f"Volume effets : {int(volume_effets * 100)}%", True, (255, 225, 190)), (self.rect.x + 145, self.rect.y + 145))
        barre_effets = pygame.Rect(self.rect.x + 140, self.rect.y + 181, 150, 14)
        pygame.draw.rect(fenetre, (42, 48, 65), barre_effets, border_radius=6)
        pygame.draw.rect(fenetre, (220, 170, 90), (barre_effets.x, barre_effets.y, int(barre_effets.width * volume_effets), barre_effets.height), border_radius=6)
        fenetre.blit(self.police_texte.render(f"Vitesse du jeu : x{vitesse_jeu}", True, (220, 230, 255)), (self.rect.x + 120, self.rect.y + 202))
        pygame.draw.rect(fenetre, (50,  85, 120), self.bouton_x15, border_radius=7)
        pygame.draw.rect(fenetre, (80, 130, 180), self.bouton_x15, width=1, border_radius=7)
        pygame.draw.rect(fenetre, (50, 100,  95), self.bouton_x2,  border_radius=7)
        pygame.draw.rect(fenetre, (85, 160, 145), self.bouton_x2,  width=1, border_radius=7)
        police_v = pygame.font.SysFont("consolas", 15, bold=True)
        t15 = police_v.render("x1.5", True, (235, 245, 255))
        t2  = police_v.render("x2",   True, (235, 255, 235))
        fenetre.blit(t15, (self.bouton_x15.centerx - t15.get_width() // 2, self.bouton_x15.centery - t15.get_height() // 2))
        fenetre.blit(t2,  (self.bouton_x2.centerx  - t2.get_width()  // 2, self.bouton_x2.centery  - t2.get_height()  // 2))