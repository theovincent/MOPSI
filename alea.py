"""
Ce module permet de générer un emplacement aléatoire.
"""

import numpy.random as rd
import numpy as np


def alea(longueur_rangees, nb_rangees):
    """
    Réparti les références de manière aléatoire dans l'entrepot.

    Parametres:
        longueur_rangees (Entier): la longueur des rangées dans l'entrepôt.

        nb_rangees (Entier): le nombre de rangées dans l'entrepôt.

    Return:
        position (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt.

    >>> alea(1, 1)
    array([[0.]])
    """
    # nb_ref = nb_rangees * longueur_rangees
    position = np.zeros((longueur_rangees, nb_rangees))

    refs = [ref for ref in range(nb_rangees * longueur_rangees)]
    rd.shuffle(refs)

    for index_refi in range(longueur_rangees):
        for index_refj in range(nb_rangees):
            position[index_refi, index_refj] = refs[index_refi * nb_rangees + index_refj]

    return position


if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

    NB_RANGEES = 10
    LONGUEUR_RANGEES = 3
    POS = alea(LONGUEUR_RANGEES, NB_RANGEES)
    print(POS)
