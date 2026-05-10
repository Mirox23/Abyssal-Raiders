"""
Qu'est-ce que le fichier gère : Ce fichier gère les classes de mobs spéciaux.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
import math
from mobs_base import Mob


class MobKamikaze(Mob):
    """
    Mob kamikaze : explose au contact du mur.
    """
    
    def __init__(self, position_spawn):
        """
        Explication de ce que fais la fonction : Cette fonction initialise un mob kamikaze.
        Les entrées : position_spawn.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_spawn, vie=5, degats=5, vitesse=40, recompense=3, couleur=(255, 100, 100))
        self.degats_explosion = 8
        self.xp = 2
    
    def avancer(self, delta_temps, chemin):
        """
        Explication de ce que fais la fonction : Cette fonction fait avancer le mob kamikaze.
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


class MobSoigneur(Mob):
    """
    Mob soigneur : soigne les autres mobs autour de lui.
    """
    
    def __init__(self, position_spawn):
        """
        Explication de ce que fais la fonction : Cette fonction initialise un mob soigneur.
        Les entrées : position_spawn.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_spawn, vie=12, degats=1, vitesse=25, recompense=3, couleur=(100, 200, 255))
        self.rayon_soins = 80
        self.vitesse_soins = 2.0
        self.dernier_soins = 0.0
        self.xp = 2
    
    def soigner_alentours(self, delta_temps, liste_ennemis):
        """
        Explication de ce que fais la fonction : Cette fonction soigne les mobs autour.
        Les entrées : delta_temps, liste_ennemis.
        Le résultat : Soigne les ennemis dans le rayon.
        """
        self.dernier_soins += delta_temps
        if self.dernier_soins >= 1.0 / self.vitesse_soins:
            self.dernier_soins = 0.0
            for ennemi in liste_ennemis:
                if ennemi != self and ennemi.vie < ennemi.vie_max:
                    distance = math.sqrt((self.x - ennemi.x)**2 + (self.y - ennemi.y)**2)
                    if distance <= self.rayon_soins:
                        ennemi.vie = min(ennemi.vie_max, ennemi.vie + 1)


class MobBoss(Mob):
    """
    Mob boss : ennemi final avec beaucoup de vie et de dégâts.
    """
    
    def __init__(self, position_spawn):
        """
        Explication de ce que fais la fonction : Cette fonction initialise un mob boss.
        Les entrées : position_spawn.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_spawn, vie=50, degats=3, vitesse=20, recompense=15, couleur=(150, 50, 150))
        self.rayon = 20
        self.degats_mur = 5
        self.xp = 5
    
    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine le boss.
        Les entrées : fenetre.
        Le résultat : Affiche le boss avec un design spécial.
        """
        # Dessiner le cercle principal plus grand
        pygame.draw.circle(fenetre, self.couleur, (int(self.x), int(self.y)), self.rayon)
        pygame.draw.circle(fenetre, (0, 0, 0), (int(self.x), int(self.y)), self.rayon, 3)
        
        # Couronne de boss
        pygame.draw.circle(fenetre, (255, 215, 0), (int(self.x), int(self.y) - self.rayon - 5), 8, 2)
        pygame.draw.circle(fenetre, (255, 215, 0), (int(self.x), int(self.y) - self.rayon - 5), 3)
        
        # Barre de vie plus grande
        if self.vie < self.vie_max:
            barre_largeur = 50
            barre_hauteur = 6
            barre_x = self.x - barre_largeur // 2
            barre_y = self.y - self.rayon - 20
            
            pygame.draw.rect(fenetre, (100, 0, 0), (barre_x - 2, barre_y - 2, barre_largeur + 4, barre_hauteur + 4))
            vie_ratio = self.vie / self.vie_max
            pygame.draw.rect(fenetre, (200, 0, 0), (barre_x, barre_y, int(barre_largeur * vie_ratio), barre_hauteur))
