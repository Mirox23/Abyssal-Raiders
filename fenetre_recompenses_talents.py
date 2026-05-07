import pygame
from decoration_cadre_abysse import dessiner_cadre_onglet
from fenetre_recompenses import FenetreRecompenses
from fenetre_arbre_talents import FenetreArbreTalents

class FenetreRecompensesTalents:
    """
    Classe de compatibilité qui encapsule FenetreRecompenses + FenetreArbreTalents.
    game.py l'utilise via l'ancien nom, on délègue les appels aux deux nouvelles fenêtres.
    """

    def __init__(self):
        self.fenetre_recompenses = FenetreRecompenses()
        self.fenetre_talents = FenetreArbreTalents()
        # Alias pour que game.py puisse lire talents directement
        self.talents = self.fenetre_talents.talents
        self.visible = False
        self._onglet = "recompenses"   # "recompenses" ou "talents"
        self.rect = pygame.Rect(110, 50, 780, 500)
        self.police_onglet = pygame.font.SysFont("consolas", 15, bold=True)
        self.rect_onglet_recomp = pygame.Rect(self.rect.x, self.rect.y - 36, 190, 36)
        self.rect_onglet_talent = pygame.Rect(self.rect.x + 196, self.rect.y - 36, 190, 36)

    def ouvrir(self):
        self.visible = True
        self.fenetre_recompenses.visible = True
        self.fenetre_talents.visible = False
        self._onglet = "recompenses"

    def gerer_clic(self, pos_clic, progression):
        if not self.visible:
            return None

        # Clic sur les onglets
        if self.rect_onglet_recomp.collidepoint(pos_clic):
            self._onglet = "recompenses"
            self.fenetre_recompenses.visible = True
            self.fenetre_talents.visible = False
            return ("consomme", None)
        if self.rect_onglet_talent.collidepoint(pos_clic):
            self._onglet = "talents"
            self.fenetre_recompenses.visible = False
            self.fenetre_talents.visible = True
            return ("onglet_talent", None)

        # Déléguer au bon panneau
        if self._onglet == "recompenses":
            action = self.fenetre_recompenses.gerer_clic(pos_clic, progression)
        else:
            action = self.fenetre_talents.gerer_clic(pos_clic, progression)

        if action and action[0] == "fermer":
            self.visible = False
            self.fenetre_recompenses.visible = False
            self.fenetre_talents.visible = False

        return action

    def dessiner(self, fenetre, progression):
        if not self.visible:
            return

        # Dessiner les onglets
        for label, rect_ong, onglet_cle in [
            ("Récompenses", self.rect_onglet_recomp, "recompenses"),
            ("Arbre à talents", self.rect_onglet_talent, "talents"),
        ]:
            actif = self._onglet == onglet_cle
            dessiner_cadre_onglet(fenetre, rect_ong, actif)
            surf = self.police_onglet.render(label, True, (245, 230, 196) if actif else (172, 144, 113))
            fenetre.blit(surf, (rect_ong.centerx - surf.get_width() // 2, rect_ong.centery - surf.get_height() // 2))

        if self._onglet == "recompenses":
            self.fenetre_recompenses.dessiner(fenetre, progression)
        else:
            self.fenetre_talents.dessiner(fenetre, progression)

    def reset_pour_nouveau_niveau(self, niveau_joueur_avant):
        """Appelé par game.py à chaque nouveau niveau de jeu."""
        return self.fenetre_talents.reset_pour_nouveau_niveau(niveau_joueur_avant)

