"""
A quoi sert le fichier : Ce fichier gère toutes les tours de défense du jeu. Il contient la classe Tour qui gère les différents types de tours (sniper, canon, ralentissement, support), leurs niveaux d'amélioration, leurs dégâts, leur portée, leur cadence de tir, et le coût de chaque amélioration. Il gère aussi les projectiles et les effets visuels des tours.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

# Importe les bibliothèques nécessaires pour les tours
import pygame
import os
from setting import portee_tour, cadence_tour, couleur_tour, cout_amelioration, bonus_portee, bonus_cadence, niveau_max
from projectile import Projectile, ProjectileRalentissement


class Tour:
    def __init__(self, position):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        # Position et caractéristiques de base de la tour
        self.x, self.y = position  # Position sur la carte
        self.taille = 15  # Taille pour la détection des ennemis
        self.portee = portee_tour  # Portée de tir de base
        self.cadence = cadence_tour  # Cadence de tir (tirs par seconde)
        self.couleur = couleur_tour  # Couleur de la tour
        self.cout_amelioration = cout_amelioration  # Coût pour améliorer la tour
        self.temps_depuis_dernier_tir = 0  # Timer pour la cadence de tir
        self.liste_projectiles = []  # Liste des projectiles tirés
        self.type_tour = "Base"  # Type de tour par défaut
        self.niveau = 1  # Niveau d'amélioration
        self.degats_tir = 1  # Dégâts de base
        self._charger_image_tour()  # Charge l'image appropriée = None
        self._taille_image = (56, 56)
        self._charger_image_tour()

    def _palier_image(self):
        """
        A quoi sert la fonction : Retourne l'index de l'image selon le niveau de la tour.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Retourne l'index de l'image selon le niveau de la tour
        if self.niveau >= 5:
            return 3  # Niveau 5+ = image index 3
        if self.niveau >= 3:
            return 2  # Niveau 3-4 = image index 2
        return 1  # Niveau 1-2 = image index 1

    def _chemins_images_possibles(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute chemins images possibles.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Construit les chemins possibles pour les images des tours selon le type
        base = f"Tours/{self.type_tour}"
        return [f"{base}/lvl{i}.png" for i in range(1, 4)]  # lvl1.png, lvl2.png, lvl3.png, lvl4.png

    def _charger_image_tour(self):
        """
        A quoi sert la fonction : Charge l'image appropriée selon le niveau et le type de tour.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Charge l'image de la tour selon son niveau et son type
        chemins = self._chemins_images_possibles()
        palier = self._palier_image()
        if palier <= len(chemins):
            fichier = chemins[palier - 1]  # Sélectionne le fichier approprié
            if os.path.exists(fichier):
                image = pygame.image.load(fichier).convert_alpha()
                self._image_tour = pygame.transform.scale(image, self._taille_image)
                return
        self._image_tour = None  # Pas d'image si le fichier n'existe pas

    def ameliorer(self, argent_joueur):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ameliorer.
        Les entrées : argent_joueur.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Vérifie si la tour peut être améliorée
        if self.niveau >= niveau_max:
            return -1  # Niveau maximum atteint
        if argent_joueur < cout_amelioration:
            return -1  # Pas assez d'argent
        
        # Améliore la tour
        self.niveau += 1
        self.portee += bonus_portee  # Augmente la portée
        self.cadence = max(0.15, self.cadence - bonus_cadence)  # Réduit la cadence (plus rapide)
        self._charger_image_tour()  # Recharge l'image du nouveau niveau
        return argent_joueur - cout_amelioration  # Retourne l'argent restant

    def valeur_revente(self):
        """
        A quoi sert la fonction : Calcule la valeur de revente de la tour.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Calcule la valeur de revente : base + bonus par niveau
        valeur_base = 6  # Valeur de base d'une tour
        bonus_niveaux = max(0, self.niveau - 1) * 3  # +3 par niveau au-dessus du 1er
        return valeur_base + bonus_niveaux

    def mettre_a_jour(self, delta_temps, liste_ennemis):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour mettre a jour pendant la partie.
        Les entrées : delta_temps, liste_ennemis.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Met à jour le timer de tir
        self.temps_depuis_dernier_tir += delta_temps

        # Vérifie si la tour peut tirer
        if self.temps_depuis_dernier_tir >= self.cadence:
            for ennemi in liste_ennemis:
                # Calcule la distance entre la tour et l'ennemi
                delta_x = ennemi.x - self.x
                delta_y = ennemi.y - self.y
                distance = (delta_x**2 + delta_y**2) ** 0.5
                
                # Si l'ennemi est dans la portée, tire dessus
                if distance <= self.portee:
                    nouveau_projectile = Projectile(self.x, self.y, ennemi)
                    self.liste_projectiles.append(nouveau_projectile)
                    self.temps_depuis_dernier_tir = 0  # Réinitialise le timer
                    break  # Un seul tir par cycle

        # Met à jour les projectiles et supprime les inactifs
        projectiles_actifs = []
        for projectile in self.liste_projectiles:
            projectile.mettre_a_jour(delta_temps)
            if projectile.actif:
                projectiles_actifs.append(projectile)
        self.liste_projectiles = projectiles_actifs

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Dessine l'image de la tour ou un cercle par défaut
        if self._image_tour:
            fenetre.blit(self._image_tour, (int(self.x - self._taille_image[0] // 2), int(self.y - self._taille_image[1] // 2)))
        else:
            pygame.draw.circle(fenetre, self.couleur, (int(self.x), int(self.y)), self.taille)
        
        # Dessine la portée de la tour (cercle semi-transparent)
        pygame.draw.circle(fenetre, (80, 80, 160), (int(self.x), int(self.y)), self.portee, 1)
        
        # Dessine le niveau de la tour
        police_niveau = pygame.font.SysFont("consolas", 10, bold=True)
        surface_niveau = police_niveau.render(str(self.niveau), True, (0, 0, 0))
        fenetre.blit(surface_niveau, (
            int(self.x) - surface_niveau.get_width() // 2,
            int(self.y) - surface_niveau.get_height() // 2
        ))
        
        # Dessine tous les projectiles de la tour
        for projectile in self.liste_projectiles:
            projectile.dessiner(fenetre)


class TourSniper(Tour):
    """Grande portée, cadence lente, dégâts élevés."""

    def __init__(self, position):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position)
        self.couleur = (20, 20, 20)
        self.cadence = 1.5
        self.portee = 250
        self.type_tour = "Sniper"
        self.degats_tir = 3

    def _chemins_images_possibles(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute chemins images possibles.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        return [
            "Tours/sniper/Tour sniper LVL1.png",
            "Tours/sniper/Tour sniper LVL2.png",
            "Tours/sniper/Tour sniper LVL3.png",
        ]

    def mettre_a_jour(self, delta_temps, liste_ennemis):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour mettre a jour pendant la partie.
        Les entrées : delta_temps, liste_ennemis.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.temps_depuis_dernier_tir += delta_temps

        if self.temps_depuis_dernier_tir >= self.cadence:
            for ennemi in liste_ennemis:
                delta_x = ennemi.x - self.x
                delta_y = ennemi.y - self.y
                distance = (delta_x**2 + delta_y**2) ** 0.5
                if distance <= self.portee:
                    projectile = Projectile(self.x, self.y, ennemi)
                    projectile.degats = 3
                    projectile.couleur_projectile = (255, 80, 80)
                    self.liste_projectiles.append(projectile)
                    self.temps_depuis_dernier_tir = 0
                    break

        projectiles_actifs = []
        for projectile in self.liste_projectiles:
            projectile.mettre_a_jour(delta_temps)
            if projectile.actif:
                projectiles_actifs.append(projectile)
        self.liste_projectiles = projectiles_actifs


class TourCanonnier(Tour):
    """Courte portée, cadence très rapide."""

    def __init__(self, position):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position)
        self.couleur = (139, 69, 19)
        self.cadence = 0.5
        self.portee = 100
        self.type_tour = "Canonnier"
        self.degats_tir = 1

    def _chemins_images_possibles(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute chemins images possibles.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        return [
            "Tours/canon/Tour canon LVL1.png",
            "Tours/canon/Tour canon LVL2.png",
            "Tours/canon/Tour canon LVL3.png",
        ]


class TourRalentissement(Tour):
    """
    Ralentit les ennemis touchés.
    Projectiles bleus qui réduisent la vitesse de 50% pendant 2 secondes.
    """

    def __init__(self, position):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position)
        self.couleur = (40, 160, 220)
        self.cadence = 1.0
        self.portee = 150
        self.type_tour = "Ralentissement"
        self.facteur_ralentissement = 0.5
        self.duree_ralentissement = 2.0
        self.degats_tir = 1

    def _chemins_images_possibles(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute chemins images possibles.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        return [
            "Tours/ralentiseuse/Tour ralentiseuse lvl1.png",
            "Tours/ralentiseuse/Tour ralentiseus lvl2.png",
            "Tours/ralentiseuse/Tour ralentiseuse lvl3.png",
        ]

    def ameliorer(self, argent_joueur):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ameliorer.
        Les entrées : argent_joueur.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        resultat = super().ameliorer(argent_joueur)
        if resultat >= 0:
            # Chaque niveau améliore le ralentissement et la durée
            self.facteur_ralentissement = max(0.2, self.facteur_ralentissement - 0.05)
            self.duree_ralentissement = min(4.0, self.duree_ralentissement + 0.3)
        return resultat

    def mettre_a_jour(self, delta_temps, liste_ennemis):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour mettre a jour pendant la partie.
        Les entrées : delta_temps, liste_ennemis.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.temps_depuis_dernier_tir += delta_temps

        if self.temps_depuis_dernier_tir >= self.cadence:
            for ennemi in liste_ennemis:
                delta_x = ennemi.x - self.x
                delta_y = ennemi.y - self.y
                distance = (delta_x**2 + delta_y**2) ** 0.5 # Calcul de la distance entre la tour et l'ennemi
                if distance <= self.portee:
                    projectile = ProjectileRalentissement(
                        self.x, self.y, ennemi,
                        self.facteur_ralentissement,
                        self.duree_ralentissement
                    )
                    self.liste_projectiles.append(projectile)
                    self.temps_depuis_dernier_tir = 0
                    break

        projectiles_actifs = []
        for projectile in self.liste_projectiles:
            projectile.mettre_a_jour(delta_temps)
            if projectile.actif:
                projectiles_actifs.append(projectile)
        self.liste_projectiles = projectiles_actifs

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        super().dessiner(fenetre)
        # Plus d'anneau distinctif car la tour a maintenant son propre design


class TourSupport(Tour):
    """
    Tour de support : améliore la cadence de tir des tours voisines.
    N'attaque pas directement les ennemis.
    """

    def __init__(self, position):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position)
        self.couleur = (200, 180, 40)
        self.cadence = 999
        self.portee = 120
        self.type_tour = "Support"
        self.rayon_buff = 120
        self.bonus_cadence_buff = 0.25
        self.tours_bufferisees = []
        self.degats_tir = 0

    def _chemins_images_possibles(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute chemins images possibles.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        return [
            "Tours/soigneuse/Tour soigneuse lvl1.png",
            "Tours/soigneuse/Tour soigneuse lvl2.png",
            "Tours/soigneuse/Tour soigneuse lvl3.png",
        ]

    def ameliorer(self, argent_joueur):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ameliorer.
        Les entrées : argent_joueur.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        resultat = super().ameliorer(argent_joueur)
        if resultat >= 0:
            self.rayon_buff = min(200, self.rayon_buff + 15)
            self.bonus_cadence_buff = min(0.5, self.bonus_cadence_buff + 0.05)
        return resultat

    def mettre_a_jour(self, delta_temps, liste_ennemis):
        """
        Explication de ce que fais la fonction : Cette fonction met à jour mettre a jour pendant la partie.
        Les entrées : delta_temps, liste_ennemis.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        # La tour support ne tire pas, elle est mise à jour via appliquer_buff
        pass

    def appliquer_buff(self, liste_tours):
        """
        Explication de ce que fais la fonction : Cette fonction exécute appliquer buff.
        Les entrées : liste_tours.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        for autre_tour in liste_tours:
            if autre_tour is self:
                continue
            if autre_tour.type_tour == "Support":
                continue
            distance = ((autre_tour.x - self.x)**2 + (autre_tour.y - self.y)**2) ** 0.5
            if distance <= self.rayon_buff:
                # On applique le buff uniquement si pas déjà buffé par cette tour
                if autre_tour not in self.tours_bufferisees:
                    autre_tour.cadence = max(0.1, autre_tour.cadence * (1 - self.bonus_cadence_buff))
                    self.tours_bufferisees.append(autre_tour)

    def retirer_buff(self, liste_tours):
        """
        Explication de ce que fais la fonction : Cette fonction exécute retirer buff.
        Les entrées : liste_tours.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        for tour_buffee in self.tours_bufferisees:
            tour_buffee.cadence = min(2.0, tour_buffee.cadence / (1 - self.bonus_cadence_buff))
        self.tours_bufferisees.clear()

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if self._image_tour:
            fenetre.blit(self._image_tour, (int(self.x - self._taille_image[0] // 2), int(self.y - self._taille_image[1] // 2)))
        else:
            pygame.draw.circle(fenetre, self.couleur, (int(self.x), int(self.y)), self.taille)
        # Anneau du rayon de buff en jaune doré (gardé pour l'utilité gameplay)
        pygame.draw.circle(fenetre, (220, 200, 50), (int(self.x), int(self.y)), self.rayon_buff, 1)
        # Plus d'étoile au centre car la tour a maintenant son propre design

        police_niveau = pygame.font.SysFont("consolas", 10, bold=True)
        surface_niveau = police_niveau.render(str(self.niveau), True, (0, 0, 0))
        fenetre.blit(surface_niveau, (
            int(self.x) - surface_niveau.get_width() // 2,
            int(self.y) - surface_niveau.get_height() // 2
        ))
