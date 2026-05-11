"""
A quoi sert le fichier : Ce fichier gère la fenêtre des scores qui affiche les meilleurs temps par vague, par continent et par vague. Il contient la classe FenetreScores qui présente les classements des joueurs dans un tableau 2x2 avec les temps, les noms et les dates. La fenêtre permet de comparer les performances et de voir les records personnels.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

# Importe les bibliothèques nécessaires pour la fenêtre des scores
import pygame
from decoration_cadre_abysse import dessiner_cadre_panneau
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

# Tableau des meilleurs scores par vague (classement multi-joueurs)

class FenetreScores:
    # Classe qui affiche le classement des meilleurs temps par vague, en grille 2x2
    
    """
    A quoi sert la fonction : Crée la fenêtre des scores qui présente les classements dans un tableau 2x2.
    Entrée : Cette fonction ne demande pas de paramètre direct.
    Sortie : Initialise une fenêtre de scores prête à être affichée.
    """
    """Affiche le classement des meilleurs temps par vague, en grille 2x2."""

    def __init__(self):
        """
        A quoi sert la fonction : Initialise la fenêtre des scores avec le continent, le niveau et les polices nécessaires.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Crée un objet fenêtre de scores prêt à être affiché.
        """
        self.visible = False  # État de visibilité de la fenêtre
        self.continent = "pirate"  # Continent actif
        self.niveau = 1  # Niveau actuel
        # Polices pour les différents textes
        self.police_titre = pygame.font.SysFont("consolas", 18, bold=True)  # Police pour les titres
        self.police_noms = pygame.font.SysFont("consolas", 14)  # Police pour les noms
        self.police_temps = pygame.font.SysFont("consolas", 12)  # Police pour les temps
        self.police_dates = pygame.font.SysFont("consolas", 10)  # Police pour les dates
        self.visible = False  # État de visibilité de la fenêtre
        self.continent = "pirate"  # Continent actif
        self.niveau = 1  # Niveau actif
        # Polices pour les différents textes
        self.police_titre = pygame.font.SysFont("consolas", 18, bold=True)  # Police pour les titres
        self.police_noms = pygame.font.SysFont("consolas", 14)  # Police pour les noms
        self.police_temps = pygame.font.SysFont("consolas", 12)  # Police pour les temps
        self.police_dates = pygame.font.SysFont("consolas", 10)  # Police pour les dates
        # Initialise les attributs de la fenêtre des scores
        self.visible = False  # État de visibilité de la fenêtre
        self.continent = "pirate"  # Continent actif
        self.niveau = 1  # Niveau actuel
        # Panneau plus grand pour accueillir le tableau 2x2
        self.rect = pygame.Rect(largeur_ecran // 2 - 380, hauteur_ecran // 2 - 260, 760, 520)  # Dimensions et position
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)  # Police pour le titre
        self.police_entete = pygame.font.SysFont("consolas", 13, bold=True)  # Police pour les en-têtes
        self.police_ligne = pygame.font.SysFont("consolas", 13)  # Police pour les lignes
        self.police_petit = pygame.font.SysFont("consolas", 11)  # Police pour le texte petit
        self.bouton_fermer = Bouton(self.rect.right - 100, self.rect.y + 12, 84, 28, "Fermer", 13)  # Bouton pour fermer
        self.classement_par_vague = {}  # Données du classement par vague
        # Noms des continents pour l'affichage
        self.noms_continents = {
            "pirate": "Pirate",
            "samourai": "Samourai",
            "medieval": "Medieval",
            "demoniaque": "Demoniaque",
        }

    def ouvrir(self, continent, niveau=1):
        """
        A quoi sert la fonction : Ouvre la fenêtre des scores en chargeant les données du continent et du niveau spécifiés.
        Entrée : continent (le continent à afficher), niveau (le niveau, par défaut 1).
        Sortie : Charge et affiche les scores du continent et niveau spécifiés.
        """
        # Importe la fonction pour obtenir le classement et configure la fenêtre
        from scores import obtenir_classement_par_vague
        self.continent = continent  # Définit le continent
        self.niveau = niveau  # Définit le niveau
        self.classement_par_vague = obtenir_classement_par_vague(continent)  # Charge les données
        self.visible = True  # Rend la fenêtre visible

    def fermer(self):
        """
        A quoi sert la fonction : Ferme la fenêtre des scores en la rendant invisible.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Cache la fenêtre des scores.
        """
        self.visible = False

    def gerer_clic(self, pos):
        """
        A quoi sert la fonction : Gère les clics sur la fenêtre des scores pour fermer la fenêtre.
        Entrée : pos (la position du clic de souris).
        Sortie : Retourne True si le clic ferme la fenêtre, False sinon.
        """
        # Gère les clics seulement si la fenêtre est visible
        if not self.visible:
            return False
        
        # Vérifie si on clique sur le bouton fermer
        if self.bouton_fermer.rect.collidepoint(pos):
            self.fermer()
            return True
        
        return self.rect.collidepoint(pos)  # Vérifie si le clic est dans la fenêtre

    def _dessiner_cellule_vague(self, fenetre, numero_vague, rect_cellule):
        """
        A quoi sert la fonction : Dessine une cellule du tableau pour une vague donnée avec le fond, le titre et les scores.
        Entrée : fenetre (la surface où dessiner), numero_vague (le numéro de la vague), rect_cellule (le rectangle de la cellule).
        Sortie : Affiche la cellule complète avec le fond, le titre et les lignes de classement.
        """
        # Fond de la cellule
        pygame.draw.rect(fenetre, (22, 30, 44), rect_cellule, border_radius=8)  # Dessine le fond de la cellule
        pygame.draw.rect(fenetre, (70, 95, 140), rect_cellule, width=1, border_radius=8)  # Dessine le contour de la cellule

        # Titre de la vague
        couleurs_vague = {
            1: (100, 200, 255),  # bleu clair
            2: (120, 230, 140),  # vert
            3: (255, 200, 80),   # doré
            4: (255, 100, 100),  # rouge (boss)
        }
        couleur_titre = couleurs_vague.get(numero_vague, (200, 200, 220))
        label = "BOSS" if numero_vague == 4 else f"Vague {numero_vague}"
        surf_titre = self.police_entete.render(f"— {label} —", True, couleur_titre)
        fenetre.blit(surf_titre, (
            rect_cellule.centerx - surf_titre.get_width() // 2,  # Centre le titre horizontalement
            rect_cellule.y + 8  # Positionne le titre en haut de la cellule
        ))

        # En-têtes colonnes
        y_entete = rect_cellule.y + 28
        col_rang = rect_cellule.x + 8
        col_temps = rect_cellule.x + 36
        col_nom = rect_cellule.x + 120

        fenetre.blit(self.police_petit.render("#", True, (160, 160, 180)), (col_rang, y_entete))
        fenetre.blit(self.police_petit.render("Temps", True, (160, 160, 180)), (col_temps, y_entete))
        fenetre.blit(self.police_petit.render("Nom", True, (160, 160, 180)), (col_nom, y_entete))

        # Ligne de séparation sous les en-têtes
        sep_y = y_entete + 14
        pygame.draw.line(fenetre, (55, 70, 100),
                         (rect_cellule.x + 6, sep_y),
                         (rect_cellule.right - 6, sep_y))  # Dessine la ligne de séparation sous les en-têtes

        # Données du classement
        entrees = self.classement_par_vague.get(str(numero_vague), [])

        if not entrees:
            # Aucun score enregistré : afficher un message immersif
            surf_vide = self.police_petit.render("Aucun aventurier n'a encore", True, (120, 130, 150))
            surf_vide2 = self.police_petit.render("franchi cette vague.", True, (120, 130, 150))
            fenetre.blit(surf_vide, (rect_cellule.x + 8, sep_y + 8))
            fenetre.blit(surf_vide2, (rect_cellule.x + 8, sep_y + 22))
            return

        # Afficher chaque joueur du classement (max 4)
        couleurs_rang = {
            0: (255, 215, 0),    # or
            1: (210, 210, 210),  # argent
            2: (180, 130, 80),   # bronze
            3: (170, 180, 200),  # reste
        }
        for i, entree in enumerate(entrees[:4]):
            y_ligne = sep_y + 8 + i * 20
            couleur_rang = couleurs_rang.get(i, (170, 180, 200))
            
            # Numéro de rang
            fenetre.blit(
                self.police_ligne.render(str(i + 1), True, couleur_rang),
                (col_rang, y_ligne)
            )
            
            # Temps formaté
            temps_str = f"{entree['temps']:.2f}s"  # Formate le temps avec 2 décimales
            # Cette ligne formate le temps en secondes avec deux décimales pour une meilleure lisibilité
            fenetre.blit(
                self.police_ligne.render(temps_str, True, (200, 220, 200)),
                (col_temps, y_ligne)
            )
            # Nom du joueur (tronqué si trop long)
            nom = str(entree.get("nom_joueur", "Joueur"))
            if len(nom) > 12:
                nom = nom[:11] + "."
            fenetre.blit(
                self.police_ligne.render(nom, True, (220, 230, 245)),
                (col_nom, y_ligne)
            )

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine le tableau des scores par vague.
        Les entrées : fenetre.
        Le résultat : Affiche la grille 2x2 des classements de vagues.
        """
        if not self.visible:
            return

        # Voile sombre
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 150))
        fenetre.blit(voile, (0, 0))

        # Fond du panneau principal
        dessiner_cadre_panneau(fenetre, self.rect)

        # En-tête : continent (gauche) + niveau (droite)
        nom_continent = self.noms_continents.get(self.continent, self.continent.capitalize())
        surf_continent = self.police_titre.render(nom_continent, True, (220, 200, 80))
        fenetre.blit(surf_continent, (self.rect.x + 16, self.rect.y + 12))

        surf_niveau = self.police_titre.render(f"Niveau : {self.niveau}", True, (180, 210, 255))
        fenetre.blit(surf_niveau, (self.rect.right - surf_niveau.get_width() - 110, self.rect.y + 12))

        # Grille 2×2 des vagues
        # Marge et espacement entre les cellules
        marge = 14
        espacement = 10
        zone_x = self.rect.x + marge
        zone_y = self.rect.y + 50          # démarrer sous l'en-tête
        largeur_zone = self.rect.width - marge * 2
        hauteur_zone = self.rect.height - 50 - marge

        largeur_cellule = (largeur_zone - espacement) // 2
        hauteur_cellule = (hauteur_zone - espacement) // 2

        # Positions des 4 cellules : (vague, col, row)
        disposition = [
            (1, 0, 0),  # vague 1 : haut gauche
            (2, 1, 0),  # vague 2 : haut droite
            (3, 0, 1),  # vague 3 : bas gauche
            (4, 1, 1),  # vague 4 : bas droite
        ]

        for numero_vague, col, row in disposition:
            x_cellule = zone_x + col * (largeur_cellule + espacement)
            y_cellule = zone_y + row * (hauteur_cellule + espacement)
            rect_cellule = pygame.Rect(x_cellule, y_cellule, largeur_cellule, hauteur_cellule)
            self._dessiner_cellule_vague(fenetre, numero_vague, rect_cellule)

        # Bouton Fermer 
        self.bouton_fermer.dessiner(fenetre)