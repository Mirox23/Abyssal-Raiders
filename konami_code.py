"""
Qu'est-ce que le fichier gère : Ce fichier gère le code Hidden Route et les animations spéciales.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
import random
import math


class CodeSecret:
    """Gestionnaire du code secret et des animations spéciales."""

    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        # Séquence Hidden Route: ↑↑↓↓←→↓↑
        self.sequence_secrete = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, 
                               pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]
        self.sequence_joueur = []
        self.code_active = False
        self.animation_confettis = []
        self.timer_animation = 0
        self.duree_animation = 180  # 3 secondes à 60 FPS
        self.deblocage_complet = False
        
    def ajouter_touche(self, touche):
        """
        Explication de ce que fais la fonction : Cette fonction ajoute une touche à la séquence.
        Les entrées : touche.
        Le résultat : Vérifie si le code secret est entré.
        """
        self.sequence_joueur.append(touche)
        
        # Garder seulement les 8 dernières touches
        if len(self.sequence_joueur) > 8:
            self.sequence_joueur = self.sequence_joueur[-8:]
        
        # Vérifier si la séquence correspond
        if self.sequence_joueur == self.sequence_secrete:
            self.activer_code_secret()
            self.sequence_joueur = []  # Réinitialiser la séquence
    
    def activer_code_secret(self):
        """
        Explication de ce que fais la fonction : Cette fonction active le code secret.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Débloque tous les niveaux, continents et téléporte au dernier niveau démoniaque.
        """
        self.code_active = True
        self.timer_animation = self.duree_animation
        self.creer_confettis()
        
        # Effets de déblocage complet
        self.deblocage_complet = True
    
    def creer_confettis(self):
        """
        Explication de ce que fais la fonction : Cette fonction crée les confettis.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Génère 100 confettis aléatoires.
        """
        self.animation_confettis = []
        
        for _ in range(100):
            confetti = {
                'x': random.randint(0, 1280),
                'y': random.randint(-50, -10),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(2, 8),
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
                'taille': random.randint(3, 8),
                'rotation': random.uniform(0, 360),
                'rotation_vitesse': random.uniform(-5, 5)
            }
            self.animation_confettis.append(confetti)
    
    def mettre_a_jour(self):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour l'animation.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Met à jour les confettis et le timer.
        """
        if self.timer_animation > 0:
            self.timer_animation -= 1
            
            # Mettre à jour les confettis
            for confetti in self.animation_confettis:
                confetti['x'] += confetti['vx']
                confetti['y'] += confetti['vy']
                confetti['vy'] += 0.3  # Gravité
                confetti['rotation'] += confetti['rotation_vitesse']
            
            # Supprimer les confettis qui sortent de l'écran
            self.animation_confettis = [c for c in self.animation_confettis if c['y'] < 720]
    
    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine les confettis.
        Les entrées : fenetre.
        Le résultat : Affiche l'animation des confettis.
        """
        if self.timer_animation > 0:
            for confetti in self.animation_confettis:
                # Créer une surface pour le confetti
                surface = pygame.Surface((confetti['taille'], confetti['taille']), pygame.SRCALPHA)
                surface.fill(confetti['couleur'])
                
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
                fenetre.blit(surface, (confetti['x'], confetti['y']))
            
            # Afficher un message spécial
            if self.timer_animation > 120:  # Première seconde
                police = pygame.font.SysFont("consolas", 48, bold=True)
                message = "CODE SECRET ACTIVÉ !"
                texte = police.render(message, True, (255, 215, 0))
                texte_rect = texte.get_rect(center=(640, 200))
                
                # Effet de clignotement
                if (self.timer_animation // 10) % 2 == 0:
                    fenetre.blit(texte, texte_rect)
            
            # Afficher le message de déblocage
            if self.timer_animation > 60:  # Deuxième seconde
                police = pygame.font.SysFont("consolas", 32, bold=True)
                message = "Tous les niveaux débloqués !"
                texte = police.render(message, True, (0, 255, 0))
                texte_rect = texte.get_rect(center=(640, 300))
                fenetre.blit(texte, texte_rect)
    
    def est_actif(self):
        """
        Explication de ce que fais la fonction : Cette fonction vérifie si le code est actif.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne True si l'animation est en cours.
        """
        return self.timer_animation > 0
