import pygame
from setting import largeur_ecran, hauteur_ecran, FPS
from menu import Menu
from game import Jeu
from musique import MusiqueManager
from progression_monde import ProgressionMonde


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption("Abyssal Raiders")
    horloge = pygame.time.Clock()

    musique_menu = MusiqueManager(0.5)
    menu = Menu(ecran, musique_menu)
    menu.relancer_musique_menu()
    progression_monde = ProgressionMonde()
    etat_application = "menu"

    while etat_application != "quitter":
        delta_temps = horloge.tick(FPS) / 1000

        if etat_application == "menu":
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT: 
                    etat_application = "quitter"
                else:
                    resultat = menu.gerer_evenement(evenement)
                    if resultat == "lancer_jeu":
                        etat_application = "jeu"
                    elif resultat == "quitter":
                        etat_application = "quitter"

            menu.mise_a_jour(delta_temps)
            menu.dessiner()
            pygame.display.flip()

        elif etat_application == "jeu":
            jeu = Jeu(menu.monde_selectionne, menu.volume_son, menu.niveau_selectionne, progression_monde)
            resultat = jeu.lancer()
            menu.relancer_musique_menu()
            menu.appliquer_progression(progression_monde)
            if resultat.get("ouvrir_map"):
                menu.etat = "map"
            etat_application = "menu"

    pygame.quit()


if __name__ == "__main__":
    main()
