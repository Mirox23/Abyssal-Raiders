import pygame
from setting import largeur_ecran, hauteur_ecran
from interface import Bouton


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
            if rect.collidepoint(position_clic) and progression.niveau >= niveau and niveau not in self.niveaux_recuperes: # rect.collidepoint(position_clic) = le clic est sur le bouton de récompense du niveau "niveau" 
                self.niveaux_recuperes.add(niveau)
                return ("recompense", 8 + niveau * 2)
        for cle, rect in self.boutons_talents: # pour chaque talent, on regarde si le clic est sur le bouton du talent et si le joueur a des points de talent et si le talent n'est pas déjà au niveau max
            talent = self.talents[cle]
            if rect.collidepoint(position_clic) and progression.points_talent > 0 and talent["niveau"] < talent["max"]: # le clic est sur le bouton du talent et le joueur a des points de talent et le talent n'est pas déjà au niveau max
                progression.points_talent -= 1
                talent["niveau"] += 1
                return ("talent", cle)
        if self.rect.collidepoint(position_clic): # le clic est sur la fenêtre mais pas sur un bouton, on considère que le joueur veut juste fermer la fenêtre
            return ("consomme", None)
        return None

    def dessiner(self, fenetre, progression):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA) # on crée une surface transparente pour faire un voile sombre sur le reste de l'écran
        voile.fill((0, 0, 0, 150))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (20, 25, 40), self.rect, border_radius=14)
        pygame.draw.rect(fenetre, (90, 120, 175), self.rect, width=2, border_radius=14) # on dessine la fenêtre principale, puis les deux sous-fenêtres pour les récompenses et les talents, puis les titres et les boutons
        fenetre.blit(self.police_titre.render("Recompenses & Arbre de talents", True, (220, 230, 255)), (self.rect.x + 14, self.rect.y + 16))
        fenetre.blit(self.police_texte.render(f"Nombre point d'amelioration : {progression.points_talent}", True, (255, 220, 130)), (self.rect.x + 14, self.rect.y + 46))
        self.bouton_fermer.dessiner(fenetre)
        pygame.draw.rect(fenetre, (26, 34, 52), self.rect_recompense, border_radius=10)
        pygame.draw.rect(fenetre, (65, 105, 165), self.rect_recompense, width=1, border_radius=10)
        fenetre.blit(self.police_texte.render("Recompense XP", True, (185, 220, 255)), (self.rect_recompense.x + 10, self.rect_recompense.y + 8))
        for i, rect in enumerate(self.boutons_recompenses): # pour chaque bouton de récompense, on regarde si le joueur a déjà récupéré la récompense ou s'il peut la récupérer, et on affiche le bouton dans une couleur différente selon le cas
            niveau = i + 1
            claim = progression.niveau >= niveau and niveau not in self.niveaux_recuperes
            deja = niveau in self.niveaux_recuperes
            couleur = (22, 102, 68) if claim else (72, 72, 82)
            if deja:
                couleur = (45, 86, 58)
            pygame.draw.rect(fenetre, couleur, rect, border_radius=6)
            texte = f"Niv {niveau} : +{8 + niveau * 2} or"
            if deja:
                texte += " (recupere)" # si le joueur a déjà récupéré la récompense, on l'indique à côté du texte de la récompense
            fenetre.blit(self.police_petite.render(texte, True, (230, 235, 230)), (rect.x + 8, rect.y + 8)) # on affiche le texte de la récompense sur le bouton, avec une indication si le joueur a déjà récupéré la récompense
        pygame.draw.rect(fenetre, (26, 34, 52), self.rect_talents, border_radius=10)
        pygame.draw.rect(fenetre, (65, 105, 165), self.rect_talents, width=1, border_radius=10)
        fenetre.blit(self.police_texte.render("Arbre de talents du joueur", True, (185, 220, 255)), (self.rect_talents.x + 10, self.rect_talents.y + 8))
        fenetre.blit(self.police_petite.render("1 point = 1 niveau", True, (205, 215, 235)), (self.rect_talents.x + 12, self.rect_talents.y + 24))
        for cle, rect in self.boutons_talents: # pour chaque bouton de talent, on affiche le nom du talent, son niveau actuel et son niveau max, et une indication que le joueur peut cliquer pour améliorer le talent s'il a des points de talent disponibles et si le talent n'est pas déjà au niveau max
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
        if self.bouton_fermer.rect.collidepoint(position_clic): # si le clic est sur le bouton fermer, on ferme la fenêtre et on ne consomme pas le clic (on retourne None pour indiquer que le clic n'est pas consommé, ce qui permet de faire d'autres actions comme fermer une autre fenêtre ou interagir avec le jeu)
            self.visible = False
            return None
        for cle, rect in self.boutons:
            if rect.collidepoint(position_clic):
                return cle
        if self.rect.collidepoint(position_clic):
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
        fenetre.blit(self.police_titre.render("Competences du Pirate", True, (220, 230, 255)), (self.rect.x + 16, self.rect.y + 16))
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
            couleur_fond = (30, 84, 62) if peut_utiliser else (40, 56, 82)

            pygame.draw.rect(fenetre, couleur_fond, rect, border_radius=8)
            pygame.draw.rect(fenetre, (90, 120, 175), rect, width=1, border_radius=8)
            fenetre.blit(self.police_texte.render(f"[{pygame.key.name(donnees['touche']).upper()}] {donnees['nom']}", True, (235, 235, 250)), (rect.x + 10, rect.y + 9))
            cd = f"Cooldown : {donnees['cooldown']:.1f}s" if donnees["cooldown"] > 0 else "Cooldown : pret"
            fenetre.blit(self.police_texte.render(cd, True, (180, 210, 245)), (rect.x + 10, rect.y + 32))
            couleur_cout = (255, 215, 120) if assez_argent else (190, 125, 125)
            fenetre.blit(self.police_texte.render(f"Cout : {cout_reel} or", True, couleur_cout), (rect.right - 160, rect.y + 12))

            if peut_utiliser:
                statut = "Statut : utilisable"
                couleur_statut = (135, 240, 170)
            elif en_cooldown:
                statut = "Statut : en cooldown"
                couleur_statut = (240, 180, 110)
            else:
                statut = "Statut : argent insuffisant"
                couleur_statut = (235, 130, 130)
            fenetre.blit(self.police_texte.render(statut, True, couleur_statut), (rect.right - 220, rect.y + 34))
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

    def gerer_clic(self, position_clic): # cette méthode gère les clics sur la fenêtre des objets, en vérifiant d'abord si la fenêtre est visible, puis si le clic est sur le bouton fermer (dans ce cas on ferme la fenêtre et on retourne None pour indiquer que le clic n'est pas consommé), ensuite on vérifie si le clic est sur l'un des boutons d'objets (dans ce cas on retourne la clé de l'objet correspondant pour indiquer que le joueur veut utiliser cet objet), et enfin si le clic est sur la fenêtre mais pas sur un bouton, on considère que le joueur veut juste fermer la fenêtre sans consommer le clic (en retournant "consomme" pour indiquer que le clic est consommé mais sans action spécifique à faire)
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
            quantite = inventaire_objets.get(cle, 0)
            utilisable = quantite > 0
            rect = pygame.Rect(self.rect.x + 20, y, self.rect.width - 40, 60)
            self.boutons.append((cle, rect))
            pygame.draw.rect(fenetre, (62, 47, 27) if utilisable else (52, 42, 38), rect, border_radius=8)
            pygame.draw.rect(fenetre, (170, 135, 80), rect, width=1, border_radius=8)
            couleur_qte = (255, 240, 200) if utilisable else (180, 160, 145)
            fenetre.blit(self.police_texte.render(f"{nom} x{quantite}", True, couleur_qte), (rect.x + 10, rect.y + 10))
            fenetre.blit(self.police_texte.render(desc, True, (230, 210, 170)), (rect.x + 10, rect.y + 32))
            statut = "Utilisable" if utilisable else "Stock vide"
            couleur_statut = (125, 230, 150) if utilisable else (230, 130, 120)
            fenetre.blit(self.police_texte.render(statut, True, couleur_statut), (rect.right - 120, rect.y + 10))
            y += 70


class PanneauParametresMusique:
    def __init__(self):
        self.visible = False
        self.rect = pygame.Rect(285, 170, 430, 210)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.bouton_fermer = Bouton(self.rect.right - 94, self.rect.y + 12, 78, 28, "Fermer", 14)
        self.bouton_moins = pygame.Rect(self.rect.x + 70, self.rect.y + 98, 48, 42)
        self.bouton_plus = pygame.Rect(self.rect.x + 312, self.rect.y + 98, 48, 42)

    def ouvrir(self):
        self.visible = True

    def gerer_clic(self, position_clic): # cette méthode gère les clics sur la fenêtre des paramètres de musique, en vérifiant d'abord si la fenêtre est visible, puis si le clic est sur le bouton fermer (dans ce cas on ferme la fenêtre et on retourne None pour indiquer que le clic n'est pas consommé), ensuite on vérifie si le clic est sur le bouton moins (dans ce cas on retourne "moins" pour indiquer que le joueur veut baisser le volume de la musique) ou sur le bouton plus (dans ce cas on retourne "plus" pour indiquer que le joueur veut augmenter le volume de la musique), et enfin si le clic est sur la fenêtre mais pas sur un bouton, on considère que le joueur veut juste fermer la fenêtre sans consommer le clic (en retournant "consomme" pour indiquer que le clic est consommé mais sans action spécifique à faire)
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.visible = False
            return None
        if self.bouton_moins.collidepoint(position_clic):
            return "moins"
        if self.bouton_plus.collidepoint(position_clic):
            return "plus"
        if self.rect.collidepoint(position_clic):
            return "consomme"
        return None

    def dessiner(self, fenetre, volume):
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 130))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (25, 30, 46), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (96, 126, 184), self.rect, width=2, border_radius=12)
        fenetre.blit(self.police_titre.render("Parametre musique", True, (220, 235, 255)), (self.rect.x + 16, self.rect.y + 16))
        self.bouton_fermer.dessiner(fenetre)
        pygame.draw.rect(fenetre, (95, 65, 50), self.bouton_moins, border_radius=7)
        pygame.draw.rect(fenetre, (95, 65, 50), self.bouton_plus, border_radius=7)
        fenetre.blit(self.police_titre.render("-", True, (255, 220, 180)), (self.bouton_moins.x + 15, self.bouton_moins.y + 2)) # on affiche un "-" sur le bouton moins et un "+" sur le bouton plus, en utilisant une couleur claire pour faire ressortir les symboles sur les boutons de couleur sombre
        fenetre.blit(self.police_titre.render("+", True, (255, 220, 180)), (self.bouton_plus.x + 13, self.bouton_plus.y + 2))
        fenetre.blit(self.police_texte.render(f"Volume musique : {int(volume * 100)}%", True, (205, 225, 255)), (self.rect.x + 145, self.rect.y + 78)) # on affiche le texte indiquant le volume actuel de la musique en pourcentage, en utilisant une couleur claire pour le faire ressortir sur le fond sombre de la fenêtre
        barre = pygame.Rect(self.rect.x + 140, self.rect.y + 114, 150, 14)
        pygame.draw.rect(fenetre, (42, 48, 65), barre, border_radius=6)
        rempli = int(barre.width * volume) # on calcule la largeur de la partie remplie de la barre en fonction du volume actuel (qui est un nombre entre 0 et 1), et on dessine un rectangle rempli par-dessus la barre pour représenter visuellement le volume actuel, avec une couleur plus vive que celle de la barre pour le faire ressortir
        pygame.draw.rect(fenetre, (100, 200, 130), (barre.x, barre.y, rempli, barre.height), border_radius=6)
