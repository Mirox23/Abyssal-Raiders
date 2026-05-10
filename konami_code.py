"""
A quoi sert le fichier : Ce fichier gère le système de codes secrets et d'easter eggs du jeu. Il contient la classe CodeSecret qui gère le code Hidden Route (Konami), l'easter egg MLK, et les animations de confettis associées. Il permet de débloquer tous les niveaux et continents avec le code secret, et de déclencher des effets visuels spéciaux.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

# Importe les bibliothèques nécessaires pour les codes secrets et les animations
import pygame
import random
import math


class CodeSecret:
    # Classe qui gère le code secret Hidden Route et les easter eggs
    """Gestionnaire du code secret et des animations spéciales."""

    def __init__(self):
        """
        A quoi sert la fonction : Initialise le système de codes secrets avec les séquences prédéfinies.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Initialise correctement les attributs de l'objet.
        """
        # Séquence Hidden Route: ↑↑↓↓←→↓↑ (Konami Code)
        self.sequence_secrete = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, 
                               pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]
        self.sequence_joueur = []  # Séquence entrée par le joueur
        self.code_active = False  # État du code secret
        self.animation_confettis = []  # Liste des confettis pour l'animation
        self.timer_animation = 0  # Timer pour l'animation
        self.duree_animation = 180  # 3 secondes à 60 FPS
        self.deblocage_complet = False  # État de déblocage complet
        
        # Easter egg MLK: m-l-k (Martin Luther King)
        self.sequence_mlk = [pygame.K_m, pygame.K_l, pygame.K_k]
        self.sequence_mlk_joueur = []  # Séquence MLK entrée par le joueur
        self.mlk_active = False  # État de l'easter egg MLK
        
    def ajouter_touche(self, touche):
        """
        A quoi sert la fonction : Ajoute une touche aux séquences et vérifie les codes secrets.
        Entrée : touche.
        Sortie : Vérifie si le code secret est entré.
        """
        self.sequence_joueur.append(touche)  # Ajoute la touche à la séquence du joueur
        
        # Garder seulement les 8 dernières touches pour Hidden Route
        if len(self.sequence_joueur) > 8:
            self.sequence_joueur = self.sequence_joueur[-8:]
        
        # Vérifier si la séquence Hidden Route correspond
        if self.sequence_joueur == self.sequence_secrete:
            self.activer_code_secret()  # Active le code secret
            self.sequence_joueur = []  # Réinitialise la séquence
        
        # Vérifier la séquence MLK
        self.sequence_mlk_joueur.append(touche)
        
        # Garder seulement les 3 dernières touches pour MLK
        if len(self.sequence_mlk_joueur) > 3:
            self.sequence_mlk_joueur = self.sequence_mlk_joueur[-3:]
        
        # Vérifier si la séquence MLK correspond
        if self.sequence_mlk_joueur == self.sequence_mlk:
            self.activer_mlk()  # Active l'easter egg
            self.sequence_mlk_joueur = []  # Réinitialise la séquence
    
    def activer_code_secret(self):
        """
        A quoi sert la fonction : Active le code secret Hidden Route avec tous les bonus.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Débloque tous les niveaux, continents et téléporte au dernier niveau démoniaque.
        """
        self.code_active = True  # Active le code secret
        self.timer_animation = self.duree_animation  # Démarre le timer d'animation
        self.creer_confettis()  # Crée les confettis
        
        # Effets de déblocage complet
        self.deblocage_complet = True
    
    def activer_mlk(self):
        """
        A quoi sert la fonction : Active l'easter egg MLK pour sauter à la fin.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Active le mode MLK pour sauter à la dernière vague du dernier niveau du continent actuel.
        """
        self.mlk_active = True  # Active l'easter egg
        self.timer_animation = self.duree_animation  # Démarre le timer d'animation
        self.creer_confettis()  # Crée les confettis
    
    def creer_confettis(self):
        """
        A quoi sert la fonction : Crée 100 confettis aléatoires pour l'animation.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Génère 100 confettis aléatoires.
        """
        self.animation_confettis = []  # Réinitialise la liste de confettis
        
        # Crée 100 confettis avec des propriétés aléatoires
        for _ in range(100):
            confetti = {
                'x': random.randint(0, 1280),  # Position X aléatoire
                'y': random.randint(-50, -10),  # Position Y aléatoire (en haut de l'écran)
                'vx': random.uniform(-2, 2),  # Vitesse X aléatoire
                'vy': random.uniform(2, 8),  # Vitesse Y aléatoire (tombe)
                'couleur': random.choice([
                    (255, 0, 0),    # Rouge
                    (0, 255, 0),    # Vert
                    (0, 0, 255),    # Bleu
                    (255, 255, 0),  # Jaune
                    (255, 0, 255),  # Magenta
                    (0, 255, 255),  # Cyan
                    (255, 128, 0),  # Orange
                    (128, 0, 255),  # Violet
                ]),
                'taille': random.randint(3, 8),  # Taille aléatoire
                'rotation': random.uniform(0, 360),  # Rotation initiale aléatoire
                'rotation_vitesse': random.uniform(-5, 5)  # Vitesse de rotation aléatoire
            }
            self.animation_confettis.append(confetti)
    
    def mettre_a_jour(self):
        """
        A quoi sert la fonction : Met à jour l'animation des confettis et le timer.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Met à jour les confettis et le timer.
        """
        if self.timer_animation > 0:
            self.timer_animation -= 1  # Décrémente le timer
            
            # Mettre à jour les confettis
            for confetti in self.animation_confettis:
                confetti['x'] += confetti['vx']  # Déplace en X
                confetti['y'] += confetti['vy']  # Déplace en Y
                confetti['vy'] += 0.3  # Gravité (tombe plus vite)
                confetti['rotation'] += confetti['rotation_vitesse']  # Rotation
            
            # Supprimer les confettis qui sortent de l'écran
            self.animation_confettis = [c for c in self.animation_confettis if c['y'] < 720]
    
    def dessiner(self, fenetre):
        """
        A quoi sert la fonction : Dessine les confettis et les messages d'activation.
        Entrée : fenetre.
        Sortie : Affiche l'animation des confettis.
        """
        if self.timer_animation > 0:
            for confetti in self.animation_confettis:
                # Créer une surface pour le confetti
                surface = pygame.Surface((confetti['taille'], confetti['taille']), pygame.SRCALPHA)
                surface.fill(confetti['couleur'])  # Couleur du confetti
                
                # Appliquer la rotation
                angle = math.radians(confetti['rotation'])
                centre = confetti['taille'] // 2
                
                # Dessiner le confetti avec rotation
                points = []
                for x, y in [(0, 0), (confetti['taille'], 0), 
                              (confetti['taille'], confetti['taille']), (0, confetti['taille'])]:
                    # Rotation autour du centre
                    rx = (x - centre) * math.cos(angle) - (y - centre) * math.sin(angle) + centre
                    ry = (x - centre) * math.sin(angle) + (y - centre) * math.cos(angle) + centre
                    points.append((rx, ry))
                
                pygame.draw.polygon(surface, confetti['couleur'], points)
                fenetre.blit(surface, (confetti['x'], confetti['y']))  # Position du confetti
            
            # Afficher un message spécial
            if self.timer_animation > 120:  # Première seconde
                police = pygame.font.SysFont("consolas", 48, bold=True)
                message = "CODE SECRET ACTIVÉ !"
                texte = police.render(message, True, (255, 215, 0))  # Couleur orange
                texte_rect = texte.get_rect(center=(640, 200))
                
                # Effet de clignotement
                if (self.timer_animation // 10) % 2 == 0:
                    fenetre.blit(texte, texte_rect)
            
            # Afficher le message de déblocage
            if self.timer_animation > 60:  # Deuxième seconde
                police = pygame.font.SysFont("consolas", 32, bold=True)
                message = "Tous les niveaux débloqués !"
                texte = police.render(message, True, (0, 255, 0))  # Couleur verte
                texte_rect = texte.get_rect(center=(640, 300))
                fenetre.blit(texte, texte_rect)
    
    def est_actif(self):
        """
        A quoi sert la fonction : Vérifie si une animation de code secret est en cours.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Retourne True si l'animation est en cours.
        """
        return self.timer_animation > 0  # Retourne True si le timer est positif
