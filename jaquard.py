import numpy as np
# besoin du sshape calculé sur l'entrepôt


def indice_jacquard(historique):
    """
    Calcule les indices de Jacquard

    Paramètres:
        historique (array de taille (nb_ref, nb_ref)) : matrice des probabilités des commandes

    Return:
        J (array de taille (nb_ref, nb_ref)): contenant les indices de Jacquard de chaque couple de références

    >>> indice_jacquard(np.array([[0, 2, 4], [2, 0, 3], [4, 3, 1]]))
    np.array([[0., 0.22222222, 0.4], [0.22222222, 0., 0.3], [0.4, 0.3, 0.06666667]])
    """
    nb_ref = len(historique)
    J = np.zeros((nb_ref, nb_ref))
    for i in range(nb_ref):
        for j in range(i, nb_ref):
            denominateur = 0
            for k in range(nb_ref):
                denominateur += historique[i, k] + historique[j, k]
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

        seuil (float) : seuil de corrélation "suffisante"

    Return:
        E (liste de listes de taille nb_ref) : E[refi] est l'ensemble de corrélation de refi

    >>> ens_correlation(np.array([[0., 0.22222222, 0.4], [0.22222222, 0., 0.3], [0.4, 0.3, 0.06666667]]), 0.25)
    [[2], [2], [0, 1]]
    >>> ens_correlation(np.array([[0., 0.22222222, 0.4], [0.22222222, 0., 0.3], [0.4, 0.3, 0.06666667]]), 0.35)
    [[2], [], [0]]
    """
    nb_ref = len(jacquard)
    E = [[] for k in range(nb_ref)]
    for i in range(nb_ref):
        for j in range(i, nb_ref):
            if j!=i and jacquard[i, j] >= seuil :
                E[i] += [j]
                E[j] += [i]
    return E



def from_historique_to_frequence(historique):
    """
    Calcule la fréquence de commande de chaque référence (= fréquence d'apparition dans les commandes).

    Paramètres:
        historique (array de taille (nb_ref, nb_ref)) : matrice des probabilités des commandes.

    Return:
        frequence (array de taille nb_ref) donnant la probabilité de chaque référence.

    >>> from_historique_to_frequence(np.array([[0.3, 0.1, 0.2], [0.1, 0, 0.4], [0.2, 0.4, 0]]))
    np.array([0.6, 0.5, 0.6])
    >>> from_historique_to_frequence(np.array([[0.1, 0.4, 0.5, 0.3], [0.4, 0, 1, 0], [0.5, 1, 0.2, 0.7], [0.3, 0, 0.7, 0.3]]))
    np.array([1.3, 1.4, 2.4, 1.3])
    """
    nb_ref = len(historique[0])
    frequence = np.zeros(nb_ref)
    for ref in range(nb_ref):
        frequence[ref] = sum(historique[ref])
    return frequence



def proche_entree(positionnement_en_cours, temps_entrepot):
    """
    Trouve la place disponible la plus proche de l'entrée de l'entrepôt.

    Paramètres:
        positionnement_en_cours (array de taille (longueur_rangees, nb_rangees)).

        temps_entrepot (array de taille (nb_ref, nb_ref)): temps[i, j] du temps que le robot met à chercher 2 objets en positions i et j dans l'entrepôt (attention, les positions sont codées en 1D): [rangee, casier] = [rangee + casier*nb_rangees])

    Return:
        position (liste [r, c]) : donne les coordonnees de la rangee r et de le casier c de la place disponible la plus proche de l'entrée
    """
    nb_rangees = len(positionnement_en_cours[0])
    longueur_rangees = len(positionnement_en_cours)

    place_min = [-1, -1] # place absurde
    distance_min = 10*(nb_rangees + longueur_rangees) # borne sup des distances

    for rangee in range(nb_rangees):
        for casier in range(longueur_rangees):
            # si la place est libre
            if positionnement_en_cours[rangee, casier] < 0 :
                place = rangee + casier * nb_rangees
                # si la place est plus proche de l'entrée
                if temps_entrepot[place, place] < distance_min :
                    place_min = [rangee, casier]
                    distance_min = temps_entrepot[place, place]

    return place_min



def proche_place(positionnement_en_cours, place, temps_entrepot):
    """
    Trouve la place disponible la plus proche de la place en question.
    Attention dans cette fonction on considère que les casier plus proche de l'entrée dans la même range sont déjà pris

    Paramètres:
        positionnement_en_cours (array de taille (longueur_rangees, nb_rangees)).

        place (liste [r, c]) : donne les coordonnees de la rangee r et de le casier c de la place à côté de laquelle on veut se placer

        temps_entrepot (array de taille (nb_ref, nb_ref)): temps[i, j] du temps que le robot met à chercher 2 objets en positions i et j dans l'entrepôt (attention, les positions sont codées en 1D): [rangee, casier] = [rangee + casier*nb_rangees])

    Return:
        position (liste [r, c]) : donne les coordonnees de la rangee r et de le casier c de la place disponible la plus proche de la place donnée

    >>> proche_place(np.array([[-1, 1], [0, -1]]), [0,1])
    [0, 0]
    >>> proche_place(np.array([[-1, 1, -1], [0, 2, -1]]), [1,0])
    [2, 1]
    >>> proche_place(np.array([[-1, 1]]), [1,0])
    [0, 0]
    """
    nb_rangees = len(positionnement_en_cours[0])
    longueur_rangees = len(positionnement_en_cours)

    rangee_ref = place[0]
    casier_ref = place[1]

    place_min = [-1, -1] # place absurde
    distance_min = 100*(nb_rangees + longueur_rangees) # borne sup des distances

    for rangee in range(nb_rangees):
        for casier in range(longueur_rangees):
            # si la place est libre
            if positionnement_en_cours[rangee, casier] < 0 :
                place_ref = rangee_ref + casier_ref * nb_rangees
                place = rangee + casier * nb_rangees
                # si la place est plus proche de la place en argument
                if temps_entrepot[place_ref, place] < distance_min :
                    place_min = [rangee, casier]
                    distance_min = temps_entrepot[place_ref, place]

    return place_min



def jacquard(historique, nb_rangees, longueur_rangees, temps_entrepot, seuil):
    """
    Crée un positionnement des références sous le critère de Jacquard.

    Paramètres:
        historique (array de taille (nb_ref, nb_ref)) : matrice des probabilités des commandes.

        nb_rangees (Entier): le nombre de rangées dans l'entrepôt.

        longueur_rangees (Entier): la longueur des rangées dans l'entrepôt.

        temps_entrepot (array de taille (nb_ref, nb_ref)): temps[i, j] du temps que le robot met à chercher 2 objets en positions i et j dans l'entrepôt (attention, les positions sont codées en 1D): [rangee, casier] = [rangee + casier*nb_rangees]).

        seuil (float) : seuil de corrélation "suffisante".

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
    positionnement = -1*np.zeros((nb_rangees, longueur_rangees))

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
    #import doctest
    #doctest.testmod()

    print(proche_entree(np.array([[-1, 1], [0, -1]])))

