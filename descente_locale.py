"""
Ce module permet de calculer un emplacement performant de l'entrepôt.
Nous utilisons ici une descente locale.
"""
from random import randint
from pathlib import Path
from evaluation import evalue_position, evalue_entrepot
from alea import alea
from generateur import extraction_commande


def permutation_cyclique_trois(positions, sens):
    """
        Effectue une permatution cyclique de longueur trois sur les rangées.

        Parametres:
            position (Array de taille (longueur_rangees, nb_rangees): la position
            des références dans l'entrepôt.

            sens (Booléreen): donne le sens du cycle

        >>> pos = [[2, 3, 4], [1, 0, 5]]
        >>> permutation_cyclique_trois(pos, True)
        >>> pos
        [[3, 4, 2], [0, 5, 1]]
        >>> pos = [[2, 3, 4], [1, 0, 5]]
        >>> permutation_cyclique_trois(pos, False)
        >>> pos
        [[4, 2, 3], [5, 1, 0]]
        """
    longeur_rangees = len(positions)
    nb_rangees = len(positions[0])
    rangee1 = randint(1, nb_rangees - 2)
    rangee2 = randint(0, rangee1)
    rangee3 = randint(rangee1)
    permutation = [rangee1, rangee2, rangee3]

    # On effectue le cyclique
    if sens:
        for profondeur in range(longeur_rangees):
            memoire = positions[profondeur][0]
            for index_rangee in range(nb_rangees - 1):
                positions[profondeur][index_rangee] = positions[profondeur][index_rangee + 1]
            positions[profondeur][-1] = memoire
    else:
        for profondeur in range(longeur_rangees):
            memoire = positions[profondeur][-1]
            for index_rangee in range(nb_rangees - 1, 0, -1):
                positions[profondeur][index_rangee] = positions[profondeur][index_rangee - 1]
            positions[profondeur][0] = memoire


def permutation_cyclique(positions, sens):
    """
    Effectue une permatution cyclique des rangées.

    Parametres:
        position (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt.

        sens (Booléreen): donne le sens du cycle

    >>> pos = [[2, 3, 4], [1, 0, 5]]
    >>> permutation_cyclique(pos, True)
    >>> pos
    [[3, 4, 2], [0, 5, 1]]
    >>> pos = [[2, 3, 4], [1, 0, 5]]
    >>> permutation_cyclique(pos, False)
    >>> pos
    [[4, 2, 3], [5, 1, 0]]
    """
    longeur_rangees = len(positions)
    nb_rangees = len(positions[0])

    # On effectue le cyclique
    if sens:
        for profondeur in range(longeur_rangees):
            memoire = positions[profondeur][0]
            for index_rangee in range(nb_rangees - 1):
                positions[profondeur][index_rangee] = positions[profondeur][index_rangee + 1]
            positions[profondeur][-1] = memoire
    else:
        for profondeur in range(longeur_rangees):
            memoire = positions[profondeur][-1]
            for index_rangee in range(nb_rangees - 1, 0, -1):
                positions[profondeur][index_rangee] = positions[profondeur][index_rangee - 1]
            positions[profondeur][0] = memoire


def permutation_rangee(positions):
    """
    Effectue une permutation de deux rangées aléatoirement choisit.

    Parametres:
        position (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt.

    >>> pos = [[2, 3], [1, 0]]
    >>> permutation_rangee(pos)
    >>> pos
    [[3, 2], [0, 1]]
    """
    longeur_rangees = len(positions)
    nb_rangees = len(positions[0])

    # On prend 2 indices de rangées differentes
    rangee1 = randint(0, nb_rangees - 1)
    rangee2 = randint(0, nb_rangees - 1)
    while rangee2 == rangee1:
        rangee2 = randint(0, nb_rangees - 1)

    # On les échange
    for profondeur in range(longeur_rangees):
        memoire = positions[profondeur][rangee1]
        positions[profondeur][rangee1] = positions[profondeur][rangee2]
        positions[profondeur][rangee2] = memoire


def permutation_element(positions):
    """
    Effectue une permutation de deux éléments.
    Les permutations intra rangée ne servent à rien, on les interdits.

    Parametres:
        position (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt.

    >>> pos = [[0, 1]]
    >>> permutation_element(pos)
    >>> pos
    [[1, 0]]
    """
    longeur_rangees = len(positions)
    nb_rangees = len(positions[0])

    # On prend 2 indices d'éléments différents
    element1 = [randint(0, longeur_rangees - 1), randint(0, nb_rangees - 1)]
    element2 = [randint(0, longeur_rangees - 1), randint(0, nb_rangees - 1)]
    while element2[1] == element1[1] or element1 == element2:
        element1[0] = randint(0, longeur_rangees - 1)
        element2[1] = randint(0, nb_rangees - 1)

    # On les échange
    memoire = positions[element1[0]][element1[1]]
    positions[element1[0]][element1[1]] = positions[element2[0]][element2[1]]
    positions[element2[0]][element2[1]] = memoire


def descente(positions, nb_permutations, proba, temps_entrepot):
    """
    Permet de trouver le minimum local de la fonction evalue.
    Prend comme point de départ le positionnement obtenu avec
    une méthode.
    Effectue nb_permutations permutations sur le positionnement
    d'origine. Le voisinage est tiré aléatoirement.

    Parametres:
        position (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt précédemment calculé au moyen d'une méthode.

        nb_permutations (Entier): le nombre de permutation à effectuer.

        praba (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.
    """
    # Initialisation des variables
    pos_opt = positions.copy()
    minimum = evalue_position(positions, temps_entrepot, proba)

    for index_permut in range(nb_permutations):
        # On modifie le positionnement en selectionnant au hasard le voisinnage
        voisinnage = randint(0, 2)
        if voisinnage == 0:
            permutation_rangee(positions)
        elif voisinnage == 1:
            permutation_element(positions)
        else:
            sens = randint(0, 1)
            permutation_cyclique(positions, sens)

        # On regarde si le nouveau positionnement fait mieux
        valeur = evalue_position(positions, temps_entrepot, proba)
        if valeur < minimum:
            minimum = valeur
            pos_opt = positions.copy()
            print("La nouvelle valeur de notre positionnement est {}".format(minimum))

    return pos_opt


if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

    # Paramètre pour charger les probabilités des commandes
    PATH_COMMANDE = Path("test.txt")
    PROBA = extraction_commande(PATH_COMMANDE)
    NB_REF = len(PROBA)

    # Définition arbitraire de la longueur et du nombre des rangées
    LONGUEUR_RANGEES = 3
    NB_RANGEES = NB_REF // LONGUEUR_RANGEES

    # Calcul du S-Shape
    TEMPS_ENTREPOT = evalue_entrepot(LONGUEUR_RANGEES, NB_RANGEES)

    # Calcul de la position de manière aléatoire
    POSITIONS = alea(LONGUEUR_RANGEES, NB_RANGEES)
    VAL_ALEA = evalue_position(POSITIONS, TEMPS_ENTREPOT, PROBA)
    print("Le positionnement aléatoire est :")
    print(POSITIONS)

    # Calcul de la position optimale
    POSITIONS_OPT = descente(POSITIONS, 100, PROBA, TEMPS_ENTREPOT)
    print("La solution trouvée est :")
    print(POSITIONS_OPT)
    VAL_NOTRE_ALGO = evalue_position(POSITIONS_OPT, TEMPS_ENTREPOT, PROBA)

    # Résultats
    print("Nous sommes passé de {} à {}".format(VAL_ALEA, VAL_NOTRE_ALGO))
