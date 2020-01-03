import numpy as np
from evaluation import *
from Algorithme.Alea import *
from abc import *
# from jacquard import *
# from nous import *


## Dimensions de l'entrepôt

nb_rangees = 0
longueur_rangees = 0


## Historique de l'entrepôt

historique = np.zeros((longueur_rangees, nb_rangees))

with open("Instance\\test_historique.txt", "r") as fichier:
    lines = fichier.readlines()
    for index, line in enumerate(lines):
        line = line.split(" ")
        for r in range(nb_rangees):
            historique[index, r] = ligne[r]


## Calcul des emplacements par différentes méthodes

positionnement_alea = alea(nb_rangees, longueur_rangees)
# positionnement_NotreAlgo = NotreAlgo(nb_rangees, longueur_rangees, technique)



## Evaluation des différents emplacements

alea = evalue(nb_rangees, longueur_rangees, positionnement_alea, historique)
# NotreAlgo = evalue(nb_rangees, longueur_rangees, positionnement_NotreAlgo, historique)
print(alea)
