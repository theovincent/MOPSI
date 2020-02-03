"""
Ce script permet de charger les probabilités sur les commandes
et de calculer les différents emplacements que propose les algorithmes.
"""

from alea import alea
from notre_algo import notre_algo
from evaluation import evalue
from generateur import generation_commande


# --- Paramètres --- #
LONGUEUR_RANGEES = 6
NB_RANGEES = 10
# Attention : le nombre de réference doit être un multiple de trois
NB_REF = LONGUEUR_RANGEES * NB_RANGEES
NOM_INSTANCE_THEO = "essai_{}fois{}".format(LONGUEUR_RANGEES, NB_RANGEES)
# NOM_INSTANCE_PIA =
NOM_INSTANCE = NOM_INSTANCE_THEO


# --- HISTORIQUE des commandes --- #
print("Chargement de la commande...")
HISTORIQUE = generation_commande(NB_REF, NOM_INSTANCE)

print("L'historique des commandes est :")
print(HISTORIQUE)


# --- Calcul des emplacements par différentes méthodes --- #
print("Calcul des positionnements...")
# Partie calcul
POSITIONNEMENT_ALEA = alea(LONGUEUR_RANGEES, NB_RANGEES)
POSITIONNEMENT_NOTRE_ALGO = notre_algo(POSITIONNEMENT_ALEA.copy(), 20, HISTORIQUE)

# Partie affichage
print("Le positionnement aléatoire est :")
print(POSITIONNEMENT_ALEA)
print("Notre positionnement est :")
print(POSITIONNEMENT_NOTRE_ALGO)


# --- Evaluation des différents emplacements --- #
print("Evaluation des positionnement...")
ALEA = evalue(POSITIONNEMENT_ALEA, HISTORIQUE)
NOTRE_ALGO = evalue(POSITIONNEMENT_NOTRE_ALGO, HISTORIQUE)

# Affichage des résultats
print("Le résultat pour le positionnement aléaoire est de {}".format(ALEA))
print("Le résultat pour notre positionnement est de {}".format(NOTRE_ALGO))


if __name__ == "__main__":
    pass
