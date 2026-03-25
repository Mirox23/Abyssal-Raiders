import pygame
from setting import *
from chemin import CHEMIN, draw_decor, draw_path
from mob import Mob
from tower import Tour, TourSniper, TourCanonnier
from ui import Bouton, PanneauTelephone


class Jeu:
    def __init__(self):
        pygame.init()

        self.fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
        pygame.display.set_caption("Abyssal Raiders")

        self.horloge = pygame.time.Clock()
        self.police = pygame.font.SysFont("consolas", 22)

        self.reinitialiser()

    def reinitialiser(self):
        self.ennemis = []
        self.tours = []

        self.minuterie_spawn = 0
        self.nb_ennemis_spawnes = 0

        self.vie_mur = vie_mur_depart
        self.argent = argent_depart

        self.bouton_tour = Bouton(820, 470, 150, 40, "Tourelle")
        self.telephone = PanneauTelephone()

        self.mode_placement = False
        self.type_tour_choisi = None
        self.tour_selectionnee = None

    def est_sur_chemin(self, pos):
        for i in range(len(CHEMIN) - 1):
            zone = pygame.Rect(
                min(CHEMIN[i][0], CHEMIN[i+1][0]) - 30,
                min(CHEMIN[i][1], CHEMIN[i+1][1]) - 30,
                abs(CHEMIN[i][0] - CHEMIN[i+1][0]) + 60,
                abs(CHEMIN[i][1] - CHEMIN[i+1][1]) + 60,
            )
            if zone.collidepoint(pos):
                return True
        return False

    def lancer(self):
        en_cours = True

        while en_cours:
            dt = self.horloge.tick(FPS) / 1000

            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    en_cours = False

                if evenement.type == pygame.MOUSEBUTTONDOWN:

                    action = self.telephone.gerer_clic(evenement.pos)
                    if action == "New Manche":
                        self.ennemis.clear()
                        self.nb_ennemis_spawnes = 0
                        self.minuterie_spawn = 0
                        self.argent += argent_par_vague

                    if self.bouton_tour.rect.collidepoint(evenement.pos):
                        self.mode_placement = True
                        self.type_tour_choisi = None
                        self.tour_selectionnee = None

                    else:
                        self.tour_selectionnee = None
                        for t in self.tours:
                            dist_x = evenement.pos[0] - t.x
                            dist_y = evenement.pos[1] - t.y
                            if (dist_x**2 + dist_y**2) ** 0.5 <= t.taille:
                                self.tour_selectionnee = t

                    if self.mode_placement and self.type_tour_choisi is None:
                        zone_sniper = pygame.Rect(400, 200, 150, 50)
                        zone_canonnier = pygame.Rect(400, 270, 150, 50)

                        if zone_sniper.collidepoint(evenement.pos):
                            self.type_tour_choisi = TourSniper
                        elif zone_canonnier.collidepoint(evenement.pos):
                            self.type_tour_choisi = TourCanonnier

                    elif self.mode_placement and self.type_tour_choisi:
                        if (
                            len(self.tours) < nb_tours_max
                            and not self.est_sur_chemin(evenement.pos)
                            and evenement.pos[0] < pos_mur - 10
                            and self.argent >= prix_tour
                        ):
                            self.tours.append(self.type_tour_choisi(evenement.pos))
                            self.argent -= prix_tour

                        self.mode_placement = False
                        self.type_tour_choisi = None

            self.mettre_a_jour(dt)
            self.dessiner()
            pygame.display.flip()

        pygame.quit()

    def mettre_a_jour(self, dt):
        if self.nb_ennemis_spawnes < total_ennemis:
            self.minuterie_spawn += dt
            if self.minuterie_spawn >= intervalle_spawn:
                self.minuterie_spawn = 0
                self.ennemis.append(Mob(CHEMIN[0], vitesse_ennemi, couleur_ennemis))
                self.nb_ennemis_spawnes += 1

        survivants = []
        for ennemi in self.ennemis:
            if ennemi.vie <= 0:
                self.argent += argent_par_kill
                continue
            a_atteint = ennemi.avancer(dt, CHEMIN)
            if a_atteint:
                self.vie_mur -= 1
                continue
            survivants.append(ennemi)
        self.ennemis = survivants

        for tour in self.tours:
            tour.mettre_a_jour(dt, self.ennemis)

    def dessiner(self):
        self.fenetre.fill(couleur_fond)

        draw_decor(self.fenetre, pygame)
        draw_path(self.fenetre, pygame)

        for tour in self.tours:
            tour.dessiner(self.fenetre)
        for ennemi in self.ennemis:
            ennemi.dessiner(self.fenetre)

        self.bouton_tour.dessiner(self.fenetre)
        self.telephone.dessiner(self.fenetre)

        self.fenetre.blit(self.police.render(f"Vie : {self.vie_mur}", True, couleur_texte), (20, 20))
        self.fenetre.blit(self.police.render(f"Argent : {self.argent}", True, couleur_texte), (20, 50))

        if self.tour_selectionnee:
            t = self.tour_selectionnee
            cote = 30
            ecart = 5
            bx = t.x - cote
            by = t.y + t.taille + 5

            pygame.draw.rect(self.fenetre, (255, 200, 0), (bx, by, cote, cote))
            self.fenetre.blit(self.police.render("A", True, (0, 0, 0)), (bx + 8, by + 5))

            pygame.draw.rect(self.fenetre, (180, 180, 180), (bx + cote + ecart, by, cote, cote))
            self.fenetre.blit(self.police.render(str(t.niveau), True, (0, 0, 0)), (bx + cote + ecart + 8, by + 5))

        if self.mode_placement and self.type_tour_choisi is None:
            zone_sniper = pygame.Rect(400, 200, 150, 50)
            zone_canonnier = pygame.Rect(400, 270, 150, 50)

            pygame.draw.rect(self.fenetre, (0, 0, 0), zone_sniper)
            pygame.draw.rect(self.fenetre, (139, 69, 19), zone_canonnier)

            self.fenetre.blit(self.police.render("Sniper", True, (255, 255, 255)), (420, 210))
            self.fenetre.blit(self.police.render("Canonnier", True, (255, 255, 255)), (420, 280))


if __name__ == "__main__":
    jeu = Jeu()
    jeu.lancer()