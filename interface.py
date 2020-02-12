"""
Ce script permet de charger les probabilités sur les commandes
et de calculer les différents emplacements que propose les algorithmes.
"""

from alea import alea
from abc_classique import ABC
from jaccard import jacquard
from descente_locale import descente
from evaluation import evalue_position, evalue_entrepot
from generateur import extraction_commande
from time import time


# --- Paramètres --- #
LONGUEUR_RANGEES = 5
NB_RANGEES = 6
# Attention : le nombre de réference doit être un multiple de trois
NB_REF = LONGUEUR_RANGEES * NB_RANGEES
NOM_INSTANCE_THEO = "entrepot{}x{}_{}".format(LONGUEUR_RANGEES, NB_RANGEES, NB_REF)
# NOM_INSTANCE_PIA =
NOM_INSTANCE = NOM_INSTANCE_THEO

# --- Probabilité des commandes --- #
print("Chargement de la commande...")
PROBA = extraction_commande(NOM_INSTANCE)[0]

# --- Calcul du S-Shape --- #
print("Calcul du S_Shape...")
TEMPS_ENTREPOT = evalue_entrepot(LONGUEUR_RANGEES, NB_RANGEES)


# --- Calcul des emplacements par différentes méthodes --- #
print("Calcul des positionnements...")
# Partie calcul
TIME_ALEA = time()

POSITIONNEMENT_ALEA = alea(LONGUEUR_RANGEES, NB_RANGEES)

TIME_ALEA_ABC = time()

POSITIONNEMENT_ABC = ABC(PROBA, NB_RANGEES, LONGUEUR_RANGEES)

TIME_ABC = time()
print(POSITIONNEMENT_ABC)
TIME_JACCARD = time()

POSITIONNEMENT_JACCARD = jacquard(PROBA, NB_RANGEES, LONGUEUR_RANGEES, TEMPS_ENTREPOT, 0.2)

TIME_JACCARD_DESCENTE = time()

POSITIONNEMENT_DESCENTE_LOCALE = descente(POSITIONNEMENT_JACCARD.copy(), PROBA, TEMPS_ENTREPOT)

TIME_DESCTENTE = time()

# Partie affichage
print("Le positionnement aléatoire est :")
print(POSITIONNEMENT_ALEA)
print("Le positionnement ABC est :")
print(POSITIONNEMENT_ABC)
print("Le positionnement Jacquard est :")
print(POSITIONNEMENT_JACCARD)
print("Le positionnement descente locale est :")
print(POSITIONNEMENT_DESCENTE_LOCALE)


# --- Evaluation des différents emplacements --- #
print("Evaluation des positionnement...")
ALEA = evalue_position(POSITIONNEMENT_ALEA, TEMPS_ENTREPOT, PROBA)
ABC = evalue_position(POSITIONNEMENT_ABC, TEMPS_ENTREPOT, PROBA)
JACCARD = evalue_position(POSITIONNEMENT_JACCARD, TEMPS_ENTREPOT, PROBA)
DESCENTE_LOCALE = evalue_position(POSITIONNEMENT_DESCENTE_LOCALE, TEMPS_ENTREPOT, PROBA)


# Affichage des résultats
print("Le résultat pour le positionnement aléaoire est de {}".format(ALEA))
print(" Temps : {}".format(TIME_ALEA_ABC - TIME_ALEA))

print("Le résultat pour le positionnement ABC est de {}".format(ABC))
print(" Temps : {}".format(TIME_ABC - TIME_ALEA_ABC))

print("Le résultat pour le positionnement Jacquard est de {}".format(JACCARD))
print(" Temps : {}".format(TIME_JACCARD_DESCENTE - TIME_JACCARD))

print("Le résultat pour le positionnement descente locale est de {}".format(DESCENTE_LOCALE))
print(" Temps : {}".format(TIME_DESCTENTE - TIME_JACCARD))

print("Pourcentage de gain par rapport à ABC : {}".format((ABC - DESCENTE_LOCALE) / ABC))
print("Pourcentage de gain par rapport à Jaccard : {}".format((JACCARD - DESCENTE_LOCALE) / JACCARD))


if __name__ == "__main__":
    pass
