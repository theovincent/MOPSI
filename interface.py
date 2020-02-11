"""
Ce script permet de charger les probabilités sur les commandes
et de calculer les différents emplacements que propose les algorithmes.
"""

from alea import alea
from abc_classique import ABC
from jaquard import jacquard
from descente_locale import descente
from evaluation import evalue_position, evalue_entrepot
from generateur import extraction_commande


# --- Paramètres --- #
LONGUEUR_RANGEES = 10
NB_RANGEES = 21
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
POSITIONNEMENT_ALEA = alea(LONGUEUR_RANGEES, NB_RANGEES)
POSITIONNEMENT_ABC = ABC(PROBA, NB_RANGEES, LONGUEUR_RANGEES)
print(POSITIONNEMENT_ABC)
# POSITIONNEMENT_JACQUARD = jacquard(PROBA, NB_RANGEES, LONGUEUR_RANGEES, TEMPS_ENTREPOT, 0.25)
POSITIONNEMENT_DESCENTE_LOCALE = descente(POSITIONNEMENT_ABC.copy(), PROBA, TEMPS_ENTREPOT)

# Partie affichage
print("Le positionnement aléatoire est :")
print(POSITIONNEMENT_ALEA)
print("Le positionnement ABC est :")
print(POSITIONNEMENT_ABC)
print("Le positionnement Jacquard est :")
# print(POSITIONNEMENT_JACQUARD)
print("Le positionnement descente locale est :")
print(POSITIONNEMENT_DESCENTE_LOCALE)


# --- Evaluation des différents emplacements --- #
print("Evaluation des positionnement...")
ALEA = evalue_position(POSITIONNEMENT_ALEA, TEMPS_ENTREPOT, PROBA)
ABC = evalue_position(POSITIONNEMENT_ABC, TEMPS_ENTREPOT, PROBA)
# JACQUARD = evalue_position(POSITIONNEMENT_JACQUARD, TEMPS_ENTREPOT, PROBA)
DESCENTE_LOCALE = evalue_position(POSITIONNEMENT_DESCENTE_LOCALE, TEMPS_ENTREPOT, PROBA)


# Affichage des résultats
print("Le résultat pour le positionnement aléaoire est de {}".format(ALEA))
print("Le résultat pour le positionnement ABC est de {}".format(ABC))
# print("Le résultat pour le positionnement Jacquard est de {}".format(JACQUARD))
print("Le résultat pour le positionnement descente locale est de {}".format(DESCENTE_LOCALE))
print("Pourcentage de gain par rapport à ABC : {}".format((ABC - DESCENTE_LOCALE) / ABC))


if __name__ == "__main__":
    pass
