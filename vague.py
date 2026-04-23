import random
from mob import Mob, MobRapide, MobTank, MobKamikaze, MobSoigneur


def generer_vague(numero_vague):
    liste_mobs = []
    temps_courant = 0.0
    intervalle = max(0.4, 0.9 - numero_vague * 0.05)
    nombre_total = 8 + (numero_vague - 1) * 4

    for i in range(nombre_total):
        tirage = random.random()

        # Plus la vague est avancée, plus les mobs rares apparaissent
        seuil_rapide = min(0.35, 0.05 + numero_vague * 0.04)
        seuil_tank = min(0.20, 0.0 + numero_vague * 0.025) if numero_vague >= 2 else 0
        seuil_kamikaze = min(0.15, 0.0 + numero_vague * 0.02) if numero_vague >= 3 else 0
        seuil_soigneur = min(0.10, 0.0 + numero_vague * 0.015) if numero_vague >= 4 else 0

        cumul_rapide = seuil_rapide
        cumul_tank = cumul_rapide + seuil_tank
        cumul_kamikaze = cumul_tank + seuil_kamikaze
        cumul_soigneur = cumul_kamikaze + seuil_soigneur

        if tirage < cumul_rapide:
            liste_mobs.append((MobRapide, temps_courant))
        elif tirage < cumul_tank:
            liste_mobs.append((MobTank, temps_courant))
        elif tirage < cumul_kamikaze:
            liste_mobs.append((MobKamikaze, temps_courant))
        elif tirage < cumul_soigneur:
            liste_mobs.append((MobSoigneur, temps_courant))
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