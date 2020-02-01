import numpy.random as rd
import numpy as np


def alea(nb_rangees, longueur_rangees):
    """
    Réparti les références de manière aléatoire dans l'entrepot
    """
    # nb_ref = nb_rangees * longueur_rangees
    position = np.zeros((longueur_rangees, nb_rangees))

    refs = [k for k in range(nb_rangees * longueur_rangees)]
    rd.shuffle(refs)

    for i in range(longueur_rangees):
        for j in range(nb_rangees):
            position[i, j] = refs[i * nb_rangees + j]

    return position


if __name__ == "__main__":
    rangees = 10
    longueur = 3
    positionnement = alea(rangees, longueur)
    print(positionnement)
