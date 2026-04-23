class ProgressionMonde:
    def __init__(self):
        self.niveaux_conquis = {
            "pirate": [False] * 8,
            "medieval": [False] * 8,
            "samourai": [False] * 8,
            "demoniaque": [False] * 8,
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

    def est_conquis(self, continent, numero_niveau):
        if continent not in self.niveaux_conquis:
            return False
        if 1 <= numero_niveau <= 8:
            return self.niveaux_conquis[continent][numero_niveau - 1]
        return False
