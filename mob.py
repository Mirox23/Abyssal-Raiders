import pygame


class Mob:
    def __init__(self, pos_depart, vitesse, couleur):
        self.x = float(pos_depart[0])
        self.y = float(pos_depart[1])

        self.vitesse = vitesse
        self.couleur = couleur

        self.taille = 12
        self.etape = 1

        self.vie_max = 4
        self.vie = self.vie_max

    def avancer(self, dt, chemin):
        if self.etape >= len(chemin):
            return True

        cible_x, cible_y = chemin[self.etape]
        dx = cible_x - self.x
        dy = cible_y - self.y

        distance = (dx**2 + dy**2) ** 0.5
        deplacement = self.vitesse * dt

        if distance <= deplacement:
            self.x, self.y = cible_x, cible_y
            self.etape += 1
            return self.etape >= len(chemin)

        if distance > 0:
            self.x += (dx / distance) * deplacement
            self.y += (dy / distance) * deplacement

        return False

    def dessiner(self, fenetre):
        pygame.draw.circle(fenetre, self.couleur, (int(self.x), int(self.y)), self.taille)

        largeur_barre = 20
        hauteur_barre = 4
        ratio_vie = self.vie / self.vie_max

        rouge = int(255 * (1 - ratio_vie))
        vert  = int(255 * ratio_vie)
        couleur_barre = (rouge, vert, 0)

        bx = self.x - largeur_barre // 2
        by = self.y - self.taille - 10

        pygame.draw.rect(fenetre, (50, 50, 50), (bx, by, largeur_barre, hauteur_barre))
        pygame.draw.rect(fenetre, couleur_barre, (bx, by, largeur_barre * ratio_vie, hauteur_barre))