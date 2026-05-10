"""
Qu'est-ce que le fichier gère : Ce fichier gère les classes de mobs de base.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
import math
from setting import *


class Mob:
    """
    Classe de base pour tous les ennemis du jeu.
    """
    
    def __init__(self, position_spawn, vie=10, degats=1, vitesse=30, recompense=2, couleur=(200, 50, 50)):
        """
        Explication de ce que fais la fonction : Cette fonction initialise un mob de base.
        Les entrées : position_spawn, vie, degats, vitesse, recompense, couleur.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.x, self.y = position_spawn
        self.vie = vie
        self.vie_max = vie
        self.degats = degats
        self.vitesse = vitesse
        self.recompense = recompense
        self.couleur = couleur
        self.rayon = 12
        self.chemin_index = 0
        self.xp = 1
        
    def avancer(self, delta_temps, chemin):
        """
        Explication de ce que fais la fonction : Cette fonction fait avancer le mob sur le chemin.
        Les entrées : delta_temps, chemin.
        Le résultat : Retourne True si le mob atteint le mur, False sinon.
        """
        if self.chemin_index >= len(chemin) - 1:
            return True
        
        # Calculer la direction vers le prochain point du chemin
        cible_x, cible_y = chemin[self.chemin_index + 1]
        direction_x = cible_x - self.x
        direction_y = cible_y - self.y
        distance = math.sqrt(direction_x**2 + direction_y**2)
        
        if distance > 0:
            # Normaliser et appliquer le déplacement
            direction_x /= distance
            direction_y /= distance
            deplacement = self.vitesse * delta_temps
            
            self.x += direction_x * deplacement
            self.y += direction_y * deplacement
            
            # Vérifier si on a atteint le point cible
            if math.sqrt((self.x - cible_x)**2 + (self.y - cible_y)**2) < 5:
                self.chemin_index += 1
        
        return False
    
    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine le mob à l'écran.
        Les entrées : fenetre.
        Le résultat : Affiche le mob.
        """
        pygame.draw.circle(fenetre, self.couleur, (int(self.x), int(self.y)), self.rayon)
        pygame.draw.circle(fenetre, (0, 0, 0), (int(self.x), int(self.y)), self.rayon, 2)
        
        # Barre de vie
        if self.vie < self.vie_max:
            barre_largeur = 30
            barre_hauteur = 4
            barre_x = self.x - barre_largeur // 2
            barre_y = self.y - self.rayon - 10
            
            pygame.draw.rect(fenetre, (100, 0, 0), (barre_x - 1, barre_y - 1, barre_largeur + 2, barre_hauteur + 2))
            vie_ratio = self.vie / self.vie_max
            pygame.draw.rect(fenetre, (0, 200, 0), (barre_x, barre_y, int(barre_largeur * vie_ratio), barre_hauteur))


class MobRapide(Mob):
    """
    Mob rapide : se déplace plus vite mais a moins de vie.
    """
    
    def __init__(self, position_spawn):
        """
        Explication de ce que fais la fonction : Cette fonction initialise un mob rapide.
        Les entrées : position_spawn.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_spawn, vie=8, degats=1, vitesse=50, recompense=3, couleur=(255, 150, 50))
        self.xp = 2


class MobTank(Mob):
    """
    Mob tank : beaucoup de vie mais se déplace lentement.
    """
    
    def __init__(self, position_spawn):
        """
        Explication de ce que fais la fonction : Cette fonction initialise un mob tank.
        Les entrées : position_spawn.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_spawn, vie=20, degats=2, vitesse=20, recompense=4, couleur=(100, 100, 150))
        self.rayon = 15
        self.xp = 3
