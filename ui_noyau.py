"""
A quoi sert le fichier : Ce fichier contient les classes fondamentales pour l'interface utilisateur du jeu. Il définit la classe Bouton qui crée des boutons interactifs avec effets de survol, et la classe AffichageXP qui gère l'affichage de la barre d'expérience et du niveau du joueur. Ces composants sont les briques de base utilisées partout dans le jeu pour construire des interfaces interactives et responsives.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from setting import largeur_ecran, hauteur_ecran, couleur_bouton, couleur_bouton_survol


class Bouton:
    # Classe qui crée des boutons interactifs avec effets de survol
    
    def __init__(self, x, y, largeur, hauteur, texte, taille_police=20):
        """
        A quoi sert la fonction : Crée un nouveau bouton interactif avec sa position, sa taille, son texte et sa police personnalisée.
        Entrée : x (position horizontale), y (position verticale), largeur (largeur du bouton), hauteur (hauteur du bouton), texte (texte affiché), taille_police (taille de la police).
        Sortie : Initialise un objet bouton prêt à être utilisé dans l'interface.
        """
        self.rect = pygame.Rect(x, y, largeur, hauteur)  # Rectangle pour la détection de clics
        self.texte = texte  # Texte affiché sur le bouton
        self.police = pygame.font.SysFont("consolas", taille_police)  # Police du texte

    def dessiner(self, fenetre, couleur_fond=None, couleur_texte=(255, 255, 255)):
        """
        A quoi sert la fonction : Dessine le bouton sur la fenêtre avec un effet de survol automatique et le texte centré.
        Entrée : fenetre (la surface où dessiner le bouton), couleur_fond (couleur personnalisée optionnelle), couleur_texte (couleur du texte optionnelle).
        Sortie : Dessine le bouton avec l'effet de survol si la souris est dessus.
        """
        position_souris = pygame.mouse.get_pos()  # Position actuelle de la souris
        if couleur_fond is None:
            # Change la couleur si la souris survole le bouton
            couleur = couleur_bouton_survol if self.rect.collidepoint(position_souris) else couleur_bouton
        else:
            couleur = couleur_fond
        pygame.draw.rect(fenetre, couleur, self.rect, border_radius=5)  # Dessine le rectangle arrondi
        surface_texte = self.police.render(self.texte, True, couleur_texte)
        # Centre le texte dans le bouton
        fenetre.blit(surface_texte, (self.rect.centerx - surface_texte.get_width() // 2, self.rect.centery - surface_texte.get_height() // 2))


class AffichageXP:
    # Classe qui gère l'affichage de la barre d'expérience et du niveau du joueur
    
    def __init__(self):
        """
        A quoi sert la fonction : Initialise les polices nécessaires pour afficher le niveau, l'expérience et les messages XP.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Initialise les polices pour l'affichage de l'interface XP.
        """
        self.police_niveau = pygame.font.SysFont("consolas", 18, bold=True)  # Police pour le niveau
        self.police_xp = pygame.font.SysFont("consolas", 13)  # Police pour l'XP
        self.police_message = pygame.font.SysFont("consolas", 22, bold=True)  # Police pour les messages

    def dessiner(self, fenetre, progression):
        """
        A quoi sert la fonction : Dessine la barre d'expérience, le niveau du joueur et les messages de gain d'XP dans le coin supérieur droit de l'écran.
        Entrée : fenetre (la surface où dessiner l'interface), progression (l'objet contenant les données XP du joueur).
        Sortie : Affiche la barre d'expérience avec le niveau et les messages temporaires.
        """
        largeur_barre = 180  # Largeur de la barre d'XP
        hauteur_barre = 14  # Hauteur de la barre d'XP
        barre_x = largeur_ecran - largeur_barre - 20  # Position X (coin droit)
        barre_y = 20  # Position Y (coin haut)
        # Dessine le fond de la barre d'XP
        pygame.draw.rect(fenetre, (40, 40, 50), (barre_x, barre_y, largeur_barre, hauteur_barre), border_radius=6)
        largeur_remplie = int(largeur_barre * progression.ratio_xp())  # Calcule la largeur remplie
        if largeur_remplie > 0:
            # Dessine la partie remplie de la barre d'XP
            pygame.draw.rect(fenetre, (80, 180, 240), (barre_x, barre_y, largeur_remplie, hauteur_barre), border_radius=6)
        pygame.draw.rect(fenetre, (100, 120, 160), (barre_x, barre_y, largeur_barre, hauteur_barre), width=1, border_radius=6)
        surface_niveau = self.police_niveau.render(f"Niv. {progression.niveau}", True, (220, 220, 255))
        fenetre.blit(surface_niveau, (barre_x - surface_niveau.get_width() - 8, barre_y - 2))
        surface_xp = self.police_xp.render(f"{progression.xp_actuelle} / {progression.xp_necessaire} XP", True, (160, 180, 200))
        fenetre.blit(surface_xp, (barre_x + largeur_barre // 2 - surface_xp.get_width() // 2, barre_y + hauteur_barre + 2))
        if progression.message_niveau_up:
            surface_msg = self.police_message.render(f"⬆ {progression.message_niveau_up}", True, (255, 230, 50))
            fenetre.blit(surface_msg, (largeur_ecran // 2 - surface_msg.get_width() // 2, 70))


class PanneauTelephone:
    # Classe qui simule un téléphone avec des applications pour accéder aux différentes fonctions du jeu
    noms_boutons = ["Tourelle", "Info", "Objets", "Competence", "Succes", "New vague", "Parametre"]

    def __init__(self):
        """
        A quoi sert la fonction : Crée un panneau téléphone interactif avec un bouton principal et des sous-menus qui s'ouvrent vers le haut.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Initialise un panneau téléphone prêt à être utilisé dans l'interface du jeu.
        """
        self.largeur = 190  # Largeur du téléphone
        self.hauteur_bouton = 40  # Hauteur de chaque bouton d'application
        self.marge = 7  # Marge entre les boutons
        self.hauteur_ferme = 46  # Hauteur du téléphone quand il est fermé
        self.x = largeur_ecran - 210  # Position X (coin inférieur droit)
        self.y = hauteur_ecran - 58  # Position Y (coin inférieur droit)
        self.ouvert = False  # État du téléphone (ouvert/fermé)
        self.bouton_principal = Bouton(self.x, self.y, self.largeur, self.hauteur_ferme, "Telephone")
        self.liste_boutons = []
        nombre_boutons = len(self.noms_boutons)
        # Crée les boutons des applications en partant du bas
        for indice, nom in enumerate(self.noms_boutons):
            position_depuis_bas = nombre_boutons - indice
            decalage = position_depuis_bas * (self.hauteur_bouton + self.marge)
            self.liste_boutons.append(Bouton(self.x, self.y - decalage, self.largeur, self.hauteur_bouton, nom))

    def gerer_clic(self, position_clic):
        """
        A quoi sert la fonction : Gère les clics sur le téléphone pour l'ouvrir/fermer ou sélectionner une application.
        Entrée : position_clic (les coordonnées x,y du clic de souris).
        Sortie : Retourne le nom de l'application cliquée ou None si on clique sur le bouton principal.
        """
        if self.bouton_principal.rect.collidepoint(position_clic):
            self.ouvert = not self.ouvert  # Inverse l'état ouvert/fermé
            return None
        if self.ouvert:
            for bouton in self.liste_boutons:
                if bouton.rect.collidepoint(position_clic):
                    return bouton.texte  # Retourne le nom de l'application
        return None

    def dessiner(self, fenetre):
        """
        A quoi sert la fonction : Dessine le téléphone avec sa coque, son bouton principal et les applications si le téléphone est ouvert.
        Entrée : fenetre (la surface où dessiner le téléphone).
        Sortie : Affiche le téléphone dans le coin inférieur droit avec animations d'ouverture/fermeture.
        """
        hauteur_coque = self.hauteur_ferme + 14  # Hauteur de base de la coque
        if self.ouvert:
            # Agrandit la coque si le téléphone est ouvert
            hauteur_coque = len(self.noms_boutons) * (self.hauteur_bouton + self.marge) + self.hauteur_ferme + 20
        # Dessine la coque du téléphone
        coque = pygame.Rect(self.x - 10, self.y + self.hauteur_ferme - hauteur_coque + 8, self.largeur + 20, hauteur_coque)
        pygame.draw.rect(fenetre, (12, 14, 20), coque, border_radius=18)
        pygame.draw.rect(fenetre, (70, 88, 125), coque, width=2, border_radius=18)
        if self.ouvert:
            # Dessine le panneau des applications si ouvert
            hauteur_panneau = len(self.noms_boutons) * (self.hauteur_bouton + self.marge) + self.marge
            rect_fond = pygame.Rect(self.x - 4, self.y - hauteur_panneau, self.largeur + 8, hauteur_panneau)
            pygame.draw.rect(fenetre, (28, 35, 48), rect_fond, border_radius=10)
            pygame.draw.rect(fenetre, (90, 120, 170), rect_fond, width=2, border_radius=10)
            for bouton in self.liste_boutons:
                bouton.dessiner(fenetre, couleur_fond=(40, 60, 88), couleur_texte=(225, 235, 255))
        # Dessine le bouton principal du téléphone
        self.bouton_principal.dessiner(fenetre, couleur_fond=(42, 84, 110), couleur_texte=(220, 245, 255))
