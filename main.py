import pygame
from setting import largeur_ecran, hauteur_ecran, FPS
from menu import Menu
from game import Jeu
from musique import MusiqueManager
from progression_monde import ProgressionMonde
from sauvegarde import sauvegarder


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    info = pygame.display.Info()
    ecran = pygame.display.set_mode((info.current_w, info.current_h),pygame.FULLSCREEN)
    pygame.display.set_caption("Abyssal Raiders")
    horloge = pygame.time.Clock()

    menu = Menu(ecran)
    progression_monde = ProgressionMonde()
    etat_application = "menu"

    while etat_application != "quitter":
        delta_temps = horloge.tick(FPS) / 1000

        if etat_application == "menu":
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT: 
                    sauvegarder("autosave", progression_monde)
                    etat_application = "quitter"
                else:
                    resultat = menu.gerer_evenement(evenement)
                    if resultat == "lancer_jeu":
                        etat_application = "jeu"
                    elif resultat == "quitter":
                        etat_application = "quitter"

            menu.mise_a_jour(delta_temps)
            ecran.fill((0, 0, 0))
            menu.dessiner()
            pygame.display.flip()

        elif etat_application == "jeu":
            jeu = Jeu(menu.monde_selectionne, menu.volume_son, menu.niveau_selectionne, progression_monde)
            resultat = jeu.lancer()
            if resultat.get("quitter"):
                sauvegarder("autosave", progression_monde)
                etat_application = "quitter"
                continue
            menu.relancer_musique_menu()
            menu.appliquer_progression(progression_monde)
            if resultat.get("ouvrir_map"):
                menu.etat = "map"
            etat_application = "menu"

    sauvegarder("autosave", progression_monde)
    pygame.quit()


if __name__ == "__main__":
    main()
