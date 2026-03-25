import random
from mob import Mob, MobRapide


def generer_vague(numero_vague):
    liste_mobs = []
    temps_courant = 0.0
    intervalle = max(0.4, 0.9 - numero_vague * 0.05)
    nombre_total = 8 + (numero_vague - 1) * 4

    for i in range(nombre_total):
        seuil_rapide = min(0.6, 0.1 + numero_vague * 0.08)
        if random.random() < seuil_rapide:
            liste_mobs.append((MobRapide, temps_courant))
        else:
            liste_mobs.append((Mob, temps_courant))
        temps_courant += intervalle

    return liste_mobs


class GestionnaireVague:
    def __init__(self):
        self.numero_vague = 0
        self.mobs_a_spawner = []
        self.minuterie = 0.0
        self.vague_en_cours = False
        self.vague_terminee = False

    def demarrer_vague(self, point_depart_chemin):
        self.numero_vague += 1
        self.mobs_a_spawner = generer_vague(self.numero_vague)
        self.minuterie = 0.0
        self.vague_en_cours = True
        self.vague_terminee = False

    def mettre_a_jour(self, delta_temps, liste_ennemis, chemin):
        if not self.vague_en_cours:
            return

        self.minuterie += delta_temps

        mobs_restants = []
        for (ClasseMob, temps_spawn) in self.mobs_a_spawner:
            if self.minuterie >= temps_spawn:
                liste_ennemis.append(ClasseMob(chemin[0]))
            else:
                mobs_restants.append((ClasseMob, temps_spawn))
        self.mobs_a_spawner = mobs_restants

        if not self.mobs_a_spawner and len(liste_ennemis) == 0:
            self.vague_en_cours = False
            self.vague_terminee = True