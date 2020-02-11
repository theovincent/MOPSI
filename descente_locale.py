"""
Ce module permet de calculer un emplacement performant de l'entrepôt.
Nous utilisons ici une descente locale.
"""
from random import randint
from evaluation import evalue_position, evalue_entrepot
from alea import alea
from generateur import extraction_commande
import numpy as np


def applique_cycle_rangees(positions, cycle, sens):
    """
    Applique le cycle aux rangées de "positions"
    Args:
        positions (Array de taille (longueur_rangees, nb_rangees): la position

        cycle (Liste d'entiers) : liste d'indice des rangées qui composent le cycle
        
        sens (Booléreen): donne le sens du cycle

    Returns:
        positions_essai (Array de taille (longueur_rangees, nb_rangees): la position
            des références dans l'entrepôt.
    >>> position = np.array([[0, 1, 4, 6], [3, 2, 5, 7]])
    >>> permutation = [0, 1, 3]
    >>> applique_cycle_rangees(position, permutation, True)
    array([[1, 6, 4, 0],
           [2, 7, 5, 3]])
    >>> applique_cycle_rangees(position, permutation, False)
    array([[6, 0, 4, 1],
           [7, 3, 5, 2]])
    """
    longeur_rangees = len(positions)
    cycle_longueur = len(cycle)
    positions_essai = positions.copy()
    
    if sens:
        for profondeur in range(longeur_rangees):
            memoire = positions_essai[profondeur, cycle[0]]
            for index_rangee in range(cycle_longueur - 1):
                positions_essai[profondeur, cycle[index_rangee]] = positions_essai[profondeur, cycle[index_rangee + 1]]
            positions_essai[profondeur, cycle[-1]] = memoire
    else:
        for profondeur in range(longeur_rangees):
            memoire = positions_essai[profondeur, cycle[-1]]
            for index_rangee in range(cycle_longueur - 1, 0, -1):
                positions_essai[profondeur, cycle[index_rangee]] = positions_essai[profondeur, cycle[index_rangee - 1]]
            positions_essai[profondeur, 0] = memoire

    return positions_essai
    
    
def cycle_rangees(longueur_cycle, positions, sens):
    """
    Calcul et effectue un cycle de longueur donnée sur les rangées de la matrice "positions"
    
    Paramètres:
        longueur_cycle (Entier positif): longueur du cycle appliqué aux positions

        positions (Array de taille (longueur_rangees, nb_rangees): les positions
            des références dans l'entrepôt.

        sens (Booléreen): donne le sens du cycle

    Returns:
        positions (Array de taille (longueur_rangees, nb_rangees): les positions
            permutées des références dans l'entrepôt.


    >>> position = np.array([[0, 1], [3, 2]])
    >>> cycle_rangees(2, position, True)
    array([[1, 0],
           [2, 3]])
    """
    nb_rangees = len(positions[0])

    # --- Calcul de la permutation --- #
    rangee1 = randint(0, nb_rangees - 1)
    cycle = [rangee1] * longueur_cycle
    nb_rangees_cycle = 1
    while nb_rangees_cycle < longueur_cycle:
        # On choisit la rangée à rajouter
        rangee = randint(0, nb_rangees - 1)
        while rangee in cycle:
            rangee = randint(0, nb_rangees - 1)
        cycle[nb_rangees_cycle] = rangee
        nb_rangees_cycle += 1

    # --- On applique le cycle --- #
    return applique_cycle_rangees(positions, cycle, sens)


def applique_cycle_elements(positions, cycle, sens):
    """
    Applique le cycle aux éléments de "positions"
    Args:
        positions (Array de taille (longueur_rangees, nb_rangees): la position

        cycle (Liste de liste d'entiers) : liste d'indices des éléments qui composent le cycle

        sens (Booléreen): donne le sens du cycle

    Returns:
        positions_essai (Array de taille (longueur_rangees, nb_rangees): la position
            des références dans l'entrepôt.
    >>> position = np.array([[0, 1, 4, 6], [3, 2, 5, 7]])
    >>> permutation = [[0, 1], [1, 2], [1, 3]]
    >>> applique_cycle_elements(position, permutation, True)
    array([[0, 5, 4, 6],
           [3, 2, 7, 1]])
    >>> applique_cycle_elements(position, permutation, False)
    array([[0, 7, 4, 6],
           [3, 2, 1, 5]])
    """
    cycle_longueur = len(cycle)
    positions_essai = positions.copy()

    if sens:
        memoire = positions_essai[cycle[0][0], cycle[0][1]]
        for index_element in range(cycle_longueur - 1):
            element1 = cycle[index_element]
            element2 = cycle[index_element + 1]
            positions_essai[element1[0], element1[1]] = positions_essai[element2[0], element2[1]]
        positions_essai[cycle[-1][0], cycle[-1][1]] = memoire
    else:
        memoire = positions_essai[cycle[-1][0], cycle[-1][1]]
        for index_element in range(cycle_longueur - 1, 0, -1):
            element1 = cycle[index_element]
            element2 = cycle[index_element - 1]
            positions_essai[element1[0], element1[1]] = positions_essai[element2[0], element2[1]]
        positions_essai[cycle[0][0], cycle[0][1]] = memoire

    return positions_essai


def cycle_elements(longueur_cycle, positions, sens):
    """
    Calcul et effectue un cycle de longueur donnée sur les éléments de la matrice "positions"

    Paramètres:
        longueur_cycle (Entier positif): longueur du cycle appliqué aux positions

        positions (Array de taille (longueur_rangees, nb_rangees): les positions
            des références dans l'entrepôt.

        sens (Booléreen): donne le sens du cycle

    Returns:
        positions (Array de taille (longueur_rangees, nb_rangees): les positions
            permutées des références dans l'entrepôt.


    >>> position = np.array([[0], [1]])
    >>> cycle_elements(2, position, True)
    array([[1],
           [0]])
    """
    longueur_rangees = len(positions)
    nb_rangees = len(positions[0])

    # --- Calcul de la permutation --- #
    rangee1 = randint(0, nb_rangees - 1)
    element1 = randint(0, longueur_rangees - 1)
    cycle = [[element1, rangee1]]
    nb_rangees_cycle = 1
    while nb_rangees_cycle < longueur_cycle:
        # On choisit l'élément à rajouter
        element = randint(0, longueur_rangees - 1)
        rangee = randint(0, nb_rangees - 1)
        couple = [element, rangee]
        while couple in cycle:
            element = randint(0, longueur_rangees - 1)
            rangee = randint(0, nb_rangees - 1)
            couple = [element, rangee]
        cycle.append(couple)
        nb_rangees_cycle += 1

    # --- On applique le cycle --- #
    return applique_cycle_elements(positions, cycle, sens)


def verif_minimum_local(positions, proba, temps_entrepot):
    """
    Permet de vérifier si positions est un minimum local de la fonction evalue_position.
    On ne vérifie que les permutations de deux éléments ou deux rangées

    Parametres:
        positions:
        proba:
        temps_entrepot:

    Returns:
        minimum_local (Booléen): True si positions est un minimum local
            et False sinon
    """
    valeur_opt = evalue_position(positions, temps_entrepot, proba)
    longueur_rangees = len(positions)
    nb_rangees = len(positions[0])

    for rangee1 in range(nb_rangees - 1):
        for rangee2 in range(rangee1 + 1, nb_rangees):
            essai_rangee = applique_cycle_rangees(positions, [rangee1, rangee2], True)
            valeur_rangee = evalue_position(essai_rangee, temps_entrepot, proba)
            if valeur_rangee < valeur_opt:
                return False

    for profondeur1 in range(longueur_rangees):
        for profondeur2 in range(profondeur1, longueur_rangees):
            for rangee1 in range(nb_rangees):
                for rangee2 in range(rangee1, nb_rangees):
                    element1 = [profondeur1, rangee1]
                    element2 = [profondeur2, rangee2]
                    if element1 != element2:
                        essai_element = applique_cycle_elements(positions, [element1, element2], True)
                        valeur_element = evalue_position(essai_element, temps_entrepot, proba)
                        if valeur_element < valeur_opt:
                            return False
    return True


def descente(positions, proba, temps_entrepot):
    """
    Permet de trouver le minimum local de la fonction evalue.
    Prend comme point de départ le positionnement obtenu avec
    une méthode.
    Effectue nb_permutations permutations sur le positionnement
    d'origine. Le voisinage est tiré aléatoirement.

    Parametres:
        position (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt précédemment calculé au moyen d'une méthode.

        praba (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.

    Return:
        pos_opt (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt optimale.
    """
    # Initialisation des variables
    pos_opt = positions.copy()
    minimum = evalue_position(positions, temps_entrepot, proba)
    nb_rangees = len(positions[0])
    longueur_rangee = len(positions)
    nb_ref = nb_rangees * longueur_rangee
    nb_essaie = 0

    while nb_essaie < nb_ref * nb_ref * 2:
        # On modifie le positionnement en selectionnant au hasard le voisinnage
        if nb_rangees > 3:  # On peut effectuer des cycles de rangées
            if nb_ref > 3:  # On peut effectuer des cycles d'éléments
                voisinnage = randint(0, 3)
            else:
                voisinnage = randint(0, 2)
        else:  # On ne peut pas effectuer des cycles de rangées
            if nb_ref > 3:  # On peut effectuer des cycles d'éléments
                voisinnage = randint(0, 2)
                if voisinnage == 2:
                    voisinnage = 3
            else:
                voisinnage = randint(0, 1)
        if nb_rangees == 1:
            voisinnage = 1

        if voisinnage == 0:  # Permutation de rangées
            essai_position = cycle_rangees(2, positions, True)
        elif voisinnage == 1:  # Permutation d'éléments
            essai_position = cycle_elements(2, positions, True)
        elif voisinnage == 2:  # Cycle de rangées
            longueur_cycle = randint(3, nb_rangees)
            sens = randint(0, 1)
            essai_position = cycle_rangees(longueur_cycle, positions, sens)
        else:  # Cycle d'éléments
            longueur_cycle = randint(3, nb_ref)
            sens = randint(0, 1)
            essai_position = cycle_elements(longueur_cycle, positions, sens)

        # On regarde si le nouveau positionnement fait mieux
        valeur = evalue_position(essai_position, temps_entrepot, proba)
        if valeur < minimum:
            nb_essaie = 0
            minimum = valeur
            pos_opt = essai_position
            print("La nouvelle valeur de notre positionnement est {}".format(minimum))
        else:
            nb_essaie += 1

    if verif_minimum_local(pos_opt, proba, temps_entrepot):
        return pos_opt
    else:
        print("Le minimum local n'est pas pos_opt...")
        return descente(pos_opt, proba, temps_entrepot)


if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

    # Paramètre pour charger les probabilités des commandes
    PATH_COMMANDE = "test"
    PROBA = extraction_commande(PATH_COMMANDE)[0]
    NB_REF = len(PROBA)

    # Définition arbitraire de la longueur et du nombre des rangées
    NB_RANGEES = 1
    LONGUEUR_RANGEES = NB_REF // NB_RANGEES

    # Calcul du S-Shape
    TEMPS_ENTREPOT = evalue_entrepot(LONGUEUR_RANGEES, NB_RANGEES)

    # Calcul de la position de manière aléatoire
    POSITIONS = alea(LONGUEUR_RANGEES, NB_RANGEES)
    VAL_ALEA = evalue_position(POSITIONS, TEMPS_ENTREPOT, PROBA)
    print("Le positionnement aléatoire est :")
    print(POSITIONS)

    # Calcul de la position optimale
    POSITIONS_OPT = descente(POSITIONS, PROBA, TEMPS_ENTREPOT)
    print("La solution trouvée est :")
    print(POSITIONS_OPT)
    VAL_NOTRE_ALGO = evalue_position(POSITIONS_OPT, TEMPS_ENTREPOT, PROBA)

    # Résultats
    print("Nous sommes passé de {} à {}".format(VAL_ALEA, VAL_NOTRE_ALGO))

