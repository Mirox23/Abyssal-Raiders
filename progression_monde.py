"""
A quoi sert le fichier : Ce fichier gère la progression du joueur à travers les différents continents et niveaux du jeu. Il contient la classe ProgressionMonde qui suit quels niveaux ont été débloqués dans chaque continent (pirate, samouraï, médiéval, démoniaque) et quels succès ont été obtenus pour chaque vague. Il permet de vérifier si un niveau est accessible et de stocker la progression globale du joueur.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""


class ProgressionMonde:
    def __init__(self):
        """
        A quoi sert la fonction : Initialise la progression du joueur avec tous les niveaux verrouillés et aucun succès obtenu.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Crée un objet progression avec 5 niveaux par continent et des grilles de succès vides.
        """
        self.nom = "Joueur"  # Nom de la sauvegarde, rempli au chargement
        self.niveaux_conquis = {
            "pirate": [False] * 5,
            "medieval": [False] * 5,
            "samourai": [False] * 5,
            "demoniaque": [False] * 5,
        }
        self.succes_vagues = {
            cle: [[False] * 4 for _ in range(5)]
            for cle in self.niveaux_conquis
        }

    def est_niveau_debloque(self, continent, numero_niveau):
        """
        A quoi sert la fonction : Vérifie si un niveau spécifique est débloqué en fonction du niveau précédent dans le même continent.
        Entrée : continent (le nom du continent à vérifier), numero_niveau (le numéro du niveau à vérifier).
        Sortie : Retourne True si le niveau est débloqué, False sinon.
        """
        if numero_niveau <= 1:
            return True
        liste = self.niveaux_conquis.get(continent, [])
        if len(liste) < (numero_niveau - 1):
            return False
        return liste[numero_niveau - 2]

    def marquer_conquis(self, continent, numero_niveau):
        """
        A quoi sert la fonction : Marque un niveau comme conquis dans un continent et débloque automatiquement les succès de ce niveau.
        Entrée : continent (le nom du continent où marquer le niveau), numero_niveau (le numéro du niveau à marquer).
        Sortie : Met à jour les niveaux conquis et les succès associés dans la progression.
        """
        if continent not in self.niveaux_conquis:
            return
        if 1 <= numero_niveau <= 5:
            self.niveaux_conquis[continent][numero_niveau - 1] = True
            self.succes_vagues[continent][numero_niveau - 1] = [True, True, True, True]

    def est_conquis(self, continent, numero_niveau):
        """
        A quoi sert la fonction : Vérifie si un niveau spécifique a déjà été conquis dans un continent.
        Entrée : continent (le nom du continent à vérifier), numero_niveau (le numéro du niveau à vérifier).
        Sortie : Retourne True si le niveau est conquis, False sinon.
        """
        if continent not in self.niveaux_conquis:
            return False
        if 1 <= numero_niveau <= 5:
            return self.niveaux_conquis[continent][numero_niveau - 1]
        return False

    def marquer_succes_vague(self, continent, numero_niveau, numero_vague):
        """
        A quoi sert la fonction : Marque une vague spécifique comme réussie dans un niveau et continent donnés.
        Entrée : continent (le nom du continent), numero_niveau (le numéro du niveau), numero_vague (le numéro de la vague).
        Sortie : Met à jour le tableau des succès pour la vague spécifiée.
        """
        if continent not in self.succes_vagues:
            return
        if not (1 <= numero_niveau <= 5 and 1 <= numero_vague <= 4):  # 5 niveaux maintenant
            return
        succes = self.succes_vagues[continent][numero_niveau - 1]
        while len(succes) < 4:
            succes.append(False)
        self.succes_vagues[continent][numero_niveau - 1][numero_vague - 1] = True

    def succes_niveau(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction exécute succes niveau.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.succes_vagues or not (1 <= numero_niveau <= 5):  # 5 niveaux maintenant
            return [False, False, False, False]
        succes = list(self.succes_vagues[continent][numero_niveau - 1])
        while len(succes) < 4:
            succes.append(False)
        return succes[:4]

    def bonus_fidelite_argent(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction exécute bonus fidelite argent.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.niveaux_conquis:
            return 0
        nb_conquis = sum(1 for c in self.niveaux_conquis[continent][:numero_niveau] if c)
        return nb_conquis * 3

    def bonus_fidelite_vie(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction exécute bonus fidelite vie.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.niveaux_conquis:
            return 0
        nb_conquis = sum(1 for c in self.niveaux_conquis[continent][:numero_niveau] if c)
        return nb_conquis // 3

    def continent_termine(self, continent):
        """
        Explication de ce que fais la fonction : Cette fonction vérifie si un continent est entièrement terminé.
        Les entrées : continent.
        Le résultat : Retourne True si tous les niveaux du continent sont conquis.
        """
        if continent not in self.niveaux_conquis:
            return False
        return all(self.niveaux_conquis[continent])

    def charger_depuis_data(self, data):
        """
        Explication de ce que fais la fonction : Initialise la progression depuis un dictionnaire JSON de sauvegarde.
        Les entrées : data (dict issu du fichier JSON).
        Le résultat : Remplit self.nom et les niveaux conquis depuis la sauvegarde.
        """
        self.nom = data.get("nom", "Joueur")
        niveaux_data = data.get("niveaux_conquis", {})
        for continent, liste in niveaux_data.items():
            if continent in self.niveaux_conquis and isinstance(liste, list):
                for i, val in enumerate(liste[:5]):
                    self.niveaux_conquis[continent][i] = bool(val)
        succes_data = data.get("succes_vagues", {})
        for continent, niveaux in succes_data.items():
            if continent in self.succes_vagues and isinstance(niveaux, list):
                for i, vagues in enumerate(niveaux[:5]):
                    if isinstance(vagues, list):
                        for j, val in enumerate(vagues[:4]):
                            self.succes_vagues[continent][i][j] = bool(val)