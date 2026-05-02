"""
Qu'est-ce que le fichier gère :
La progression globale du joueur (niveaux conquis + succès de vagues) par continent.
Entrée :
Nom du continent, numéro de niveau, numéro de vague.
Résultat :
Un suivi persistant des déblocages et succès, utilisable par la map et les écrans de succès.
"""


class ProgressionMonde:
    def __init__(self):
        """
        Explication de ce que fais la fonction :
        Initialise toutes les structures de progression avec des valeurs par défaut.
        Les entrées :
        Aucune.
        Le résultat :
        Un objet prêt à enregistrer les succès du joueur.
        """
        self.niveaux_conquis = {
            "pirate": [False] * 8,
            "medieval": [False] * 8,
            "samourai": [False] * 8,
            "demoniaque": [False] * 8,
        }
        self.succes_vagues = {
            cle: [[False] * 4 for _ in range(8)]
            for cle in self.niveaux_conquis
        }

    def est_niveau_debloque(self, continent, numero_niveau):
        if numero_niveau <= 1:
            return True
        liste = self.niveaux_conquis.get(continent, [])
        if len(liste) < (numero_niveau - 1):
            return False
        return liste[numero_niveau - 2]

    def marquer_conquis(self, continent, numero_niveau):
        if continent not in self.niveaux_conquis:
            return
        if 1 <= numero_niveau <= 8:
            self.niveaux_conquis[continent][numero_niveau - 1] = True
            self.succes_vagues[continent][numero_niveau - 1] = [True, True, True, True]

    def est_conquis(self, continent, numero_niveau):
        if continent not in self.niveaux_conquis:
            return False
        if 1 <= numero_niveau <= 8:
            return self.niveaux_conquis[continent][numero_niveau - 1]
        return False

    def marquer_succes_vague(self, continent, numero_niveau, numero_vague):
        """
        Explication de ce que fais la fonction :
        Active une case de succes de vague (1..4) pour le niveau cible.
        Les entrées :
        continent (str), numero_niveau (int), numero_vague (int).
        Le résultat :
        Progression des succès de vagues modifiée.
        """
        if continent not in self.succes_vagues:
            return
        if not (1 <= numero_niveau <= 8 and 1 <= numero_vague <= 4):
            return
        succes = self.succes_vagues[continent][numero_niveau - 1]
        while len(succes) < 4:
            succes.append(False)
        self.succes_vagues[continent][numero_niveau - 1][numero_vague - 1] = True

    def succes_niveau(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction :
        Renvoie les 4 succes de vagues d'un niveau.
        Les entrées :
        continent (str), numero_niveau (int).
        Le résultat :
        Liste de 4 booleens [v1, v2, v3, v4].
        """
        if continent not in self.succes_vagues or not (1 <= numero_niveau <= 8):
            return [False, False, False, False]
        succes = list(self.succes_vagues[continent][numero_niveau - 1])
        while len(succes) < 4:
            succes.append(False)
        return succes[:4]

    def bonus_fidelite_argent(self, continent, numero_niveau):
        """
        Bonus de fidélité : +3 or de départ par niveau déjà conquis
        dans ce continent. Récompense les joueurs qui reviennent sur des niveaux maîtrisés.
        """
        if continent not in self.niveaux_conquis:
            return 0
        nb_conquis = sum(1 for c in self.niveaux_conquis[continent][:numero_niveau] if c)
        return nb_conquis * 3

    def bonus_fidelite_vie(self, continent, numero_niveau):
        """
        Bonus de fidélité : +1 PV de mur par tranche de 3 niveaux conquis dans le continent.
        """
        if continent not in self.niveaux_conquis:
            return 0
        nb_conquis = sum(1 for c in self.niveaux_conquis[continent][:numero_niveau] if c)
        return nb_conquis // 3
