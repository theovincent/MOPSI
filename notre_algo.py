import numpy.random as rd
from evaluation import evalue
from alea import alea
from generateur import extraction_commande


def permutation_rangee(positions):
    """
    Effectue une permutation de rangées aléatoire
    >>> positions = [[2, 3], [1, 0]]
    >>> permutation_rangee(positions)
    >>> positions
    [[3, 2], [0, 1]]
    """
    longeur_rangees = len(positions)
    nb_rangees = len(positions[0])

    # On prend 2 indices de rangées differentes
    rangee1 = rd.randint(0, nb_rangees)
    rangee2 = rd.randint(0, nb_rangees)
    while rangee2 == rangee1:
        rangee2 = rd.randint(0, nb_rangees)

    # On les échange
    for profondeur in range(longeur_rangees):
        memoire = positions[profondeur][rangee1]
        positions[profondeur][rangee1] = positions[profondeur][rangee2]
        positions[profondeur][rangee2] = memoire


def permutation_element(positions):
    """
    Effectue une permutation de deux éléments.
    Les permutations intra rangée ne servent à rien,
    on les interdits.
    >>> positions = [[0, 1]]
    >>> permutation_element(positions)
    >>> positions
    [[1, 0]]
    """
    longeur_rangees = len(positions)
    nb_rangees = len(positions[0])

    # On prend 2 indices d'éléments différents
    element1 = [rd.randint(0, longeur_rangees), rd.randint(0, nb_rangees)]
    element2 = [rd.randint(0, longeur_rangees), rd.randint(0, nb_rangees)]
    while element2[1] == element1[1]:
        element2[1] = rd.randint(0, nb_rangees)

    # On les échange
    memoire = positions[element1[0]][element1[1]]
    positions[element1[0]][element1[1]] = positions[element2[0]][element2[1]]
    positions[element2[0]][element2[1]] = memoire


def notre_algo(positionnement, nb_permutation, historique):
    """
    Permet de trouver le minimum local de la fonction evalue.
    Prend comme point de départ le positionnement obtenu avec
    une technique.
    Effectue nb_ite_rangee sur les rangees et
    nb_ite_element entre deux elements quelconques.
    """
    # Initialisation des variables
    minimum = evalue(positionnement, historique)
    pos_opt = positionnement.copy()

    for index_permut in range(nb_permutation):
        # On modifie le positionnement en selectionnant au hasard le voisinnage
        voisinnage = 0
        if voisinnage:
            permutation_rangee(positionnement)
        else:
            permutation_element(positionnement)

        # On regarde si le nouveau positionnement fait mieux
        valeur = evalue(positionnement, historique)
        if valeur < minimum:
            minimum = valeur
            pos_opt = positionnement.copy()
            print("La nouvelle valeur de notre positionnement est {}".format(minimum))
            print(pos_opt)

    return pos_opt


if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

    # Paramètre pour charger l'historique des commandes
    path_commande = "test.txt"
    commande = extraction_commande(path_commande)

    # Calcul de la position de manière aléatoire
    position = alea(3, 3)
    print("Le positionnement aléatoire est :")
    print(position)

    # Calcul de la position optimale
    print(notre_algo(position.copy(), 10, commande))
