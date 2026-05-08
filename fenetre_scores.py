"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie fenetre scores du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from decoration_cadre_abysse import dessiner_cadre_panneau, dessiner_plat_rect
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

# Tableau des meilleurs scores

class FenetreScores:
    """Affiche le nouveau système de scores : top runs + records de vague."""

    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.continent = "pirate"
        self.rect = pygame.Rect(largeur_ecran // 2 - 320, hauteur_ecran // 2 - 220, 640, 440)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_ligne = pygame.font.SysFont("consolas", 15)
        self.police_petit = pygame.font.SysFont("consolas", 12)
        self.bouton_fermer = Bouton(self.rect.right - 90, self.rect.y + 10, 78, 30, "Fermer", 13)
        self.scores = []
        self.meilleurs_par_vague = {}
        self.noms_continents = {
            "pirate": "Pirate",
            "samourai": "Samourai",
            "medieval": "Medieval",
            "demoniaque": "Demoniaque",
        }

    def ouvrir(self, continent):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : continent.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        from scores import obtenir_scores, obtenir_meilleurs_par_vague
        self.continent = continent
        self.scores = obtenir_scores(continent)
        self.meilleurs_par_vague = obtenir_meilleurs_par_vague(continent)
        self.visible = True

    def fermer(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute fermer.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = False

    def gerer_clic(self, pos):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : pos.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return False
        if self.bouton_fermer.rect.collidepoint(pos):
            self.fermer()
            return True
        return self.rect.collidepoint(pos)

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 140))
        fenetre.blit(voile, (0, 0))
        dessiner_cadre_panneau(fenetre, self.rect)

        rect_top = pygame.Rect(self.rect.x + 20, self.rect.y + 58, self.rect.width - 40, 240)
        rect_vagues = pygame.Rect(self.rect.x + 20, rect_top.bottom + 12, self.rect.width - 40, 108)

        nom_continent = self.noms_continents.get(self.continent, self.continent.title())
        dessiner_plat_rect(fenetre, rect_top, (26, 30, 48), (170, 120, 70), 2)
        titre = self.police_titre.render(f"Meilleurs scores - {nom_continent}", True, (220, 200, 80))
        fenetre.blit(titre, (self.rect.centerx - titre.get_width() // 2, self.rect.y + 14))
        self.bouton_fermer.dessiner(fenetre)

        rect_top = pygame.Rect(self.rect.x + 20, self.rect.y + 58, self.rect.width - 40, 240)
        rect_vagues = pygame.Rect(self.rect.x + 20, rect_top.bottom + 12, self.rect.width - 40, 108)

        pygame.draw.rect(fenetre, (26, 30, 48), rect_top, border_radius=8)
        pygame.draw.rect(fenetre, (64, 82, 128), rect_top, width=1, border_radius=8)
        pygame.draw.rect(fenetre, (24, 28, 44), rect_vagues, border_radius=8)
        pygame.draw.rect(fenetre, (64, 82, 128), rect_vagues, width=1, border_radius=8)

        entetes_y = rect_top.y + 10
        fenetre.blit(self.police_petit.render("Rang", True, (160, 160, 200)), (rect_top.x + 16, entetes_y))
        fenetre.blit(self.police_petit.render("Score", True, (160, 160, 200)), (rect_top.x + 90, entetes_y))
        fenetre.blit(self.police_petit.render("Niveau", True, (160, 160, 200)), (rect_top.x + 210, entetes_y))
        fenetre.blit(self.police_petit.render("Niveau joueur", True, (160, 160, 200)), (rect_top.x + 350, entetes_y))
        pygame.draw.line(fenetre, (70, 80, 120), (rect_top.x + 12, entetes_y + 18), (rect_top.right - 12, entetes_y + 18))

        if not self.scores:
            msg = self.police_ligne.render("Aucun score enregistre pour ce continent.", True, (160, 160, 180))
            fenetre.blit(msg, (rect_top.centerx - msg.get_width() // 2, rect_top.centery - 10))
        else:
            medailles = ["1", "2", "3", "4", "5"]
            for index_score, entree in enumerate(self.scores[:5]):
                y_ligne = entetes_y + 30 + index_score * 38
                fond_ligne = pygame.Rect(rect_top.x + 10, y_ligne - 4, rect_top.width - 20, 32)
                if index_score % 2 == 0:
                    couleur_fond = (32, 38, 58)
                else:
                    couleur_fond = (28, 34, 52)
                pygame.draw.rect(fenetre, couleur_fond, fond_ligne, border_radius=5)

                if index_score == 0:
                    couleur_ligne = (255, 220, 80)
                else:
                    couleur_ligne = (205, 210, 225)

                fenetre.blit(self.police_ligne.render(medailles[index_score], True, couleur_ligne), (rect_top.x + 20, y_ligne + 4))
                fenetre.blit(self.police_ligne.render(str(entree["score"]), True, couleur_ligne), (rect_top.x + 90, y_ligne + 4))
                fenetre.blit(self.police_ligne.render(f"Niv. {entree['niveau']}", True, (200, 210, 230)), (rect_top.x + 210, y_ligne + 4))
                fenetre.blit(self.police_ligne.render(f"Niv. {entree['niveau_joueur']}", True, (180, 195, 215)), (rect_top.x + 350, y_ligne + 4))

        titre_vagues = self.police_petit.render("Records de temps par vague", True, (200, 200, 220))
        fenetre.blit(titre_vagues, (rect_vagues.x + 12, rect_vagues.y + 8))

        for numero_vague in range(1, 5):
            infos_vague = self.meilleurs_par_vague.get(str(numero_vague))
            if infos_vague:
                texte = f"Vague {numero_vague} : {infos_vague['temps']} s - {infos_vague.get('nom_joueur', 'Joueur')}"
                couleur = (180, 230, 180)
            else:
                texte = f"Vague {numero_vague} : aucun score"
                couleur = (145, 155, 180)

            if numero_vague <= 2:
                position_x = rect_vagues.x + 14
                position_y = rect_vagues.y + 34 + (numero_vague - 1) * 24
            else:
                position_x = rect_vagues.x + rect_vagues.width // 2 + 6
                position_y = rect_vagues.y + 34 + (numero_vague - 3) * 24

            fenetre.blit(self.police_petit.render(texte, True, couleur), (position_x, position_y))
