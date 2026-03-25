# mob.py
# représente un ennemi qui se déplace sur le chemin

import pygame


class Mob:
    def __init__(self, position_depart, vitesse, couleur):
        self.x = float(position_depart[0])
        self.y = float(position_depart[1])

        self.vitesse = vitesse
        self.couleur = couleur

        self.taille = 12
        self.prochain_point = 1  # l'index du prochain waypoint à atteindre

        self.vie_max = 4
        self.vie = self.vie_max

    def avancer(self, temps_ecoule, chemin):
        # si on a dépassé le dernier point, le mob est arrivé au mur
        if self.prochain_point >= len(chemin):
            return True

        cible_x, cible_y = chemin[self.prochain_point]

        dist_x = cible_x - self.x
        dist_y = cible_y - self.y
        distance = (dist_x**2 + dist_y**2) ** 0.5

        deplacement = self.vitesse * temps_ecoule

        # si on est proche du point, on passe au suivant
        if distance <= deplacement:
            self.x, self.y = cible_x, cible_y
            self.prochain_point += 1
            return self.prochain_point >= len(chemin)

        if distance > 0:
            self.x += (dist_x / distance) * deplacement
            self.y += (dist_y / distance) * deplacement

        return False

    def dessiner(self, ecran):
        # on dessine le mob
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

        # puis sa barre de vie
        self._dessiner_barre_vie(ecran)

    def _dessiner_barre_vie(self, ecran):
        largeur_barre = 20
        hauteur_barre = 4

        ratio_vie = self.vie / self.vie_max

        # la couleur passe du vert au rouge selon les pv restants
        composante_rouge = int(255 * (1 - ratio_vie))
        composante_verte = int(255 * ratio_vie)
        couleur_barre = (composante_rouge, composante_verte, 0)

        pos_x = self.x - largeur_barre // 2
        pos_y = self.y - self.taille - 10

        # fond gris
        pygame.draw.rect(ecran, (50, 50, 50), (pos_x, pos_y, largeur_barre, hauteur_barre))
        # vie restante
        pygame.draw.rect(ecran, couleur_barre, (pos_x, pos_y, largeur_barre * ratio_vie, hauteur_barre))