import numpy.random as rd


def fromFichierToMatrice(fichier):
    """Permet d'obtenir la version matricielle de fichier
    >>> fromFichierToMatrice(open("PosTest.txt", "r"))
    [[2, 3], [1, 0]]
    """
    # Initialisation des variable
    lines = fichier.readlines()
    largeur = len(lines)
    longeur = len(lines[0])
    emplacements = [[[0] * longeur] for i in range(largeur)]

    # On parcourt le fichier
    for (i, line) in enumerate(lines):
        line = line[:-1].split(" ")  # Transforme [0 1 4] en [0, 1, 4]
        emplacements[i][:] = [int(element) for element in line]

    return emplacements


def permutation_rangee(Positions):
    """Effectue une permutation de rangées
    >>> Positions = [[2, 3], [1, 0]]
    >>> permutation_rangee(Positions)
    >>> Positions
    [[3, 2], [0, 1]]
    """
    largeur = len(Positions)
    longeur = len(Positions[0])

    # On prend 2 indices de rangées differentes
    rangee1 = rd.randint(0, longeur)
    rangee2 = rd.randint(0, longeur)
    while rangee2 == rangee1:
        rangee2 = rd.randint(0, longeur)

    # On les échange
    for i in range(largeur):
        memoir = Positions[i][rangee1]
        Positions[i][rangee1] = Positions[i][rangee2]
        Positions[i][rangee2] = memoir


def permutation_element(Positions):
    """Effectue une permutation d'elements
    >>> Positions = [[0, 1]]
    >>> permutation_element(Positions)
    >>> Positions
    [[1, 0]]
    """
    largeur = len(Positions)
    longeur = len(Positions[0])

    # On prend 2 indices d'elements differentes
    element1 = [rd.randint(0, largeur), rd.randint(0, longeur)]
    element2 = [rd.randint(0, largeur), rd.randint(0, longeur)]
    while element2 == element1:
        element2 = [rd.randint(0, largeur), rd.randint(0, longeur)]

    # On les échange
    memoir = Positions[element1[0]][element1[1]]
    Positions[element1[0]][element1[1]] = Positions[element2[0]][element2[1]]
    Positions[element2[0]][element2[1]] = memoir


def min_local(technique, nb_ite_rangee, nb_ite_element):
    """Permet de trouver le minimum local de la fonction evalue.
    Prend comme point de départ le positionnement obtenu avec
    la technique "technique".
    Effectue nb_ite_rangee sur les rangees et
    nb_ite_element entre deux elements quelconques."""
    # On va chercher les emplacements
    chemin_fichier = "Algorithme\\Pos{}.txt".format(technique)
    fichier_emplacements = open(chemin_fichier, "r")

    # Initialisation des variables
    emplacements = fromFichierToMatrice(fichier_emplacements)
    minimum = evalue(emplacements)
    emplacementMin = emplacements[:]

    # On effectue des permutations sur rangee
    for i in range(nb_ite_rangee + nb_ite_element):
        # On modifie emplacements
        if i < nb_ite_rangee:
            permutation_rangee(emplacements)
        else:
            permutation_element(emplacements)
        # On regarde si le nouveau positionnement fait mieux
        valeur = evalue(emplacements)
        if valeur < minimum:
            minimum = valeur
            emplacementMin = emplacements[:]

    return emplacementMin


if __name__ == "__main__":
    import doctest
    doctest.testmod()
