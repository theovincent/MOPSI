import numpy as np
# rappel : les rangées sont numérotées à partir de 0


def indice_jacquard(historique):
    """
    Calcule les indices de Jacquard

    Paramètres:
        historique (array de taille (nb_ref, nb_ref)) : matrice des probabilités des commandes

    Return:
        J (array de taille (nb_ref, nb_ref)): contenant les indices de Jacquard de chaque couple de références

    >>> indice_jacquard(np.array([[0.3, 0.1, 0.2], [0.1, 0, 0.4], [0.2, 0.4, 0]]))
    [[1/3, 0.1, 0.2], [0.1, 0, 4/7], [0.2, 4/7, 0]]
    """
    nb_ref = len(historique)
    J = np.zeros((nb_ref, nb_ref))
    for i in range(nb_ref):
        for j in range(i, nb_ref):
            denominateur = 0
            for k in range(nb_ref):
                denominateur += historique[i, k] + historique[k, i]
            denominateur -= historique[i, j]
            J[i, j] = historique[i, j]/denominateur
            J[j, i] = J[i, j]
    return J


def ens_correlation(jacquard, seuil):
    """
    Crée les ensemble de corrélation de chaque référence.
    L'ensemble de corrélation de refi est l'ensemble des refj (j!=i) suffisament corrélés, ie J[refi, refj] >= seuil donné

    Paramètres:
        jacquard (array de taille (nb_ref, nb_ref)) : matrice des indices de jacquard

        seuil (float) : seuil de corrélation "suffisante".

    Return:
        E (array de taille nb_ref) : E[refi] est l'ensemble de corrélation de refi

    >>> ens_correlation(np.array([[0.3, 0.1, 0.2], [0.1, 0, 0.4], [0.2, 0.4, 0]]), 0.19)
    [[2], [], [0]]
    """
    nb_ref = len(jacquard)
    E = np.zeros(nb_ref)
    for i in range(nb_ref):
        for j in range(nb_ref):
            if j!=i and jacquard[i, j]>=seuil :
                E[i] += [j]
    return E


def from_historique_to_frequence(historique):
    """
    Calcule la fréquence de commande de chaque référence (= fréquence d'apparition dans les commandes).

    Paramètres:
        historique (array de taille (nb_ref, nb_ref)) : matrice des probabilités des commandes.

    Return:
        frequence (array de taille nb_ref) donnant la probabilité de chaque référence.

    >>> from_historique_to_frequence(np.array([[0.3, 0.1, 0.2], [0.1, 0, 0.4], [0.2, 0.4, 0]]))
    [0.5, 0.5, 0.6]
    """
    nb_ref = len(historique[0])
    frequence = np.zeros(nb_ref)
    for ref in range(nb_ref):
        for ref2 in range(nb_ref):
            frequence[ref] += historique[ref, ref2]
    return frequence


def proche_entree(positionnement_en_cours):
    """
    Trouve la place disponible la plus proche de l'entrée de l'entrepôt.

    Paramètres:
        positionnement_en_cours (array de taille (longueur_rangees, nb_rangees)).

    Return:
        position (liste [r, c]) : donne les coordonnees de la rangee r et de le casier c de la place disponible la plus proche de l'entrée

    >>> proche_entree(np.array([[-1, 1], [0, -1]]))
    [0, 0]
    >>> proche_entree(np.array([[-1, 1]]))
    [0, 0]
    >>> proche_entree(np.array([[0, -1]]))
    [1, 0]
    >>> proche_entree(np.array([[-1, 1, 3], [0, -1, -1]]))
    [1, 1]
    """
    nb_rangees = len(positionnement_en_cours)
    longueur_rangees = len(positionnement_en_cours[0])
    # on définit un ordre allant de la rangée la plus proche de l'entrée
    # à la rangée la plus éloignée
    ordre_rangee = []
    # si le nombre de rangées est impair
    if nb_rangees%2!=0:
        rangee_milieu_gauche = (nb_rangees - 1)/2
        rangee_milieu_droite = (nb_rangees + 1)/2
        for k in range(0, int((nb_rangees - 1)/2 + 1)):
            ordre_rangee.append(rangee_milieu_gauche - k)
            ordre_rangee.append(rangee_milieu_droite + k)
        ordre_rangee.append(nb_rangees - 1)
    # si le nombre de rangées est pair
    else :
        rangee_entree = nb_rangees/2
        ordre_rangee.append(rangee_entree)
        for k in range(1, int(nb_rangees/2)):
            ordre_rangee.append(rangee_entree - k)
            ordre_rangee.append(rangee_entree + k)
        ordre_rangee.append(nb_rangees - 1)

    index_rangee = 0 # nombre de rangees déjà visitées
    rangee = ordre_rangee[index_rangee]
    casier = longueur_rangees - 1
    while positionnement_en_cours[rangee, casier]>=0: # tant que la place est occupée
        if casier>0: # si est pas encore au bout de la rangée
            casier -= 1
        else: # si on est arrivé au bout de la rangée
            index_rangee += 1
            rangee = ordre_rangee[index_rangee]
            casier = longueur_rangees -1

    return [rangee, casier]


def proche_place(positionnement_en_cours, place):
    """
    Trouve la place disponible la plus proche de la place en question.
    Attention dans cette fonction on considère que les casier plus proche de l'entrée dans la même range sont déjà pris

    Paramètres:
        positionnement_en_cours (array de taille (longueur_rangees, nb_rangees)).

        place (liste [r, c]) : donne les coordonnees de la rangee r et de le casier c de la place à côté de laquelle on veut se placer

    Return:
        position (liste [r, c]) : donne les coordonnees de la rangee r et de le casier c de la place disponible la plus proche de la place donnée

    >>> proche_place(np.array([[-1, 1], [0, -1]]), [0,1])
    [0, 0]
    >>> proche_place(np.array([[-1, 1, -1], [0, 2, -1]]), [1,0])
    [2, 1]
    >>> proche_place(np.array([[-1, 1]]), [1,0])
    [0, 0]
    """
    nb_rangees = len(positionnement_en_cours)
    longueur_rangees = len(positionnement_en_cours[0])
    rangee = place[0]
    casier = place[1]
    while positionnement_en_cours[rangee, casier] >= 0:
        # si on est pas au bout de la rangée
        if place[1]>0:
            casier -= 1
        # si on est au bout de la rangée, il faut changer de rangée
        else:
            # si on est dans la rangée la plus à gauche, on repart du milieu droite
            if rangee == 0:
                rangee = int(nb_rangees/2) + 1
            # si on est dans la rangée la plus à droite, on repart du milieu gauche
            elif rangee == nb_rangees - 1:
                rangee = int(nb_rangees/2)
            # si on est dans la partie gauche, on se déplace dans la rangée à gauche
            elif rangee <= nb_rangees/2:
                rangee = rangee - 1
            # si on est dans la partie droite, on se déplace dans la rangée à droite
            else:
                rangee = rangee + 1
            casier = longueur_rangees - 1
    return [rangee, casier]


def jacquard(historique, nb_rangees, longueur_rangees, seuil):
    """
    Crée un positionnement des références sous le critère de Jacquard.

    Paramètres:
        historique (array de taille (nb_ref, nb_ref)) : matrice des probabilités des commandes.

        nb_rangees (Entier): le nombre de rangées dans l'entrepôt.

        longueur_rangees (Entier): la longueur des rangées dans l'entrepôt.

        seuil (float) : seuil de corrélation "suffisante"

    Return:
        positionnement (array de taille (longueur_rangees, nb_rangees)) : la position des références dans l'entrepôt.

    >>> from_historique_to_frequence(np.array([[0.3, 0.1, 0.2], [0.1, 0, 0.4], [0.2, 0.4, 0]]))
    [0.5, 0.5, 0.6]
    """

    nb_ref = len(historique)
    frequence = from_historique_to_frequence(historique)
    J = indice_jacquard(historique)
    E = ens_correlation(J, seuil)
    # on initialise le positionnement à -1 (-1 signifie donc que la place est libre)
    positionnement = np.zeros((nb_rangees, longueur_rangees))*(-1)

    nb_restant = nb_ref
    while nb_restant>0:
        i_max = np.argmax(frequence)
        place_pour_i = proche_entree(positionnement)
        positionnement[place_pour_i[0], place_pour_i[1]] = i_max
        nb_restant -= 1
        frequence[i_max] = -1 # i ne pourra plus être sélectionné dans argmax
        W = [ref for ref in E[i_max] if frequence[ref]>=0] # références suffisamment corrélées à i_max, pas encore placées
        J_W = [J[i_max, ref] for ref in W]
        for iter in range(len(W)):
            j_max = W[np.argmax(J_W)] # référence n'ayant pas encore été placée la plus proche de i_max
            place_pour_j = proche_place(positionnement, place_pour_i)
            positionnement[place_pour_j[0], place_pour_j[1]] = j_max
            J_W[j_max] = -1 # j ne pourra plus être sélectionné dans argmax des Jacquard
            frequence[j_max] = -1 # j ne pourra plus être sélectionné dans argmax des freq

    return positionnement



if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()