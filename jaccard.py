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
    array([[0., 0.22222222, 0.4], [0.22222222, 0., 0.3], [0.4, 0.3, 0.06666667]])
    """
    nb_ref = len(historique)
    J = np.zeros((nb_ref, nb_ref))
    for i in range(nb_ref):
        for j in range(i, nb_ref):
            denominateur = 0
            for k in range(nb_ref):
                denominateur += historique[i, k] + historique[j, k]
            denominateur -= historique[i, j]
            if denominateur == 0:
                J[i, j] = 0
                J[j, i] = J[i, j]
            else :
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
    array([0.6, 0.5, 0.6])
    >>> from_historique_to_frequence(np.array([[0.1, 0.4, 0.5, 0.3], [0.4, 0, 1, 0], [0.5, 1, 0.2, 0.7], [0.3, 0, 0.7, 0.3]]))
    array([1.3, 1.4, 2.4, 1.3])
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

    >>> temps = np.array([[8, 12, 16, 8, 12, 16], [12, 8, 14, 12, 8, 14], [16, 14, 12, 16, 14, 12], [8, 12, 16, 6, 10, 14], [12, 8, 14, 10, 6, 12], [16, 14, 12, 14, 12, 10]])
    >>> proche_entree(np.array([[-1, 0, -1], [-1, 2, -1]]), temps)
    [1, 0]
    >>> proche_entree(np.array([[-1, 0, -1], [4, 2, -1]]), temps)
    [0, 0]
    >>> proche_entree(np.array([[3, 0, -1], [4, 2, -1]]), temps)
    [1, 2]
    >>> proche_entree(np.array([[3, 0, -1], [4, 2, 5]]), temps)
    [0, 2]
    """
    nb_rangees = len(positionnement_en_cours[0])
    longueur_rangees = len(positionnement_en_cours)

    place_min = [-1, -1] # place absurde
    distance_min = 10*(nb_rangees + longueur_rangees) # borne sup des distances

    for rangee in range(nb_rangees):
        for casier in range(longueur_rangees):
            # si la place est libre
            if positionnement_en_cours[casier, rangee] < 0 :
                place = rangee + casier * nb_rangees
                # si la place est plus proche de l'entrée
                if temps_entrepot[place, place] < distance_min :
                    place_min = [casier, rangee]
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
        position (liste [c, r]) : donne les coordonnees de la rangee r et de le casier c de la place disponible la plus proche de la place donnée

    >>> temps = np.array([[8, 12, 16, 8, 12, 16], [12, 8, 14, 12, 8, 14], [16, 14, 12, 16, 14, 12], [8, 12, 16, 6, 10, 14], [12, 8, 14, 10, 6, 12], [16, 14, 12, 14, 12, 10]])
    >>> proche_place(np.array([[-1, -1, -1], [-1, 2, -1]]), [1, 1], temps)
    [0, 1]
    >>> proche_place(np.array([[-1, 2, -1], [-1, -1, -1]]), [1, 1], temps)
    [1, 1]
    >>> proche_place(np.array([[-1, 2, -1], [-1, 1, -1]]), [1, 1], temps)
    [1, 0]
    >>> proche_place(np.array([[-1, 2, -1], [0, 1, -1]]), [1, 1], temps)
    [0, 0]
    >>> proche_place(np.array([[3, 2, -1], [0, 1, -1]]), [1, 1], temps)
    [1, 2]
    """
    nb_rangees = len(positionnement_en_cours[0])
    longueur_rangees = len(positionnement_en_cours)

    casier_ref = place[0]
    rangee_ref = place[1]

    place_min = [-1, -1] # place absurde
    distance_min = 100*(nb_rangees + longueur_rangees) # borne sup des distances

    for rangee in range(nb_rangees):
        for casier in range(longueur_rangees):
            # si la place est libre
            if positionnement_en_cours[casier, rangee] < 0 :
                place_ref = rangee_ref + casier_ref * nb_rangees
                place = rangee + casier * nb_rangees
                # si la place est plus proche de la place en argument
                if temps_entrepot[place_ref, place] < distance_min :
                    place_min = [casier, rangee]
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

    >>> temps22 = np.array([[6, 12, 6, 12], [12, 10, 12, 10], [6, 12, 4, 10], [12, 10, 10, 8]])
    >>> temps14 = np.array([[8, 10, 14, 18], [10, 4, 10, 14], [14, 10, 8, 14], [18, 14, 14, 12]])
    >>> temps41 = np.array([[12, 12, 12, 12], [12, 10, 10, 10], [12, 10, 8, 8], [12, 10, 8, 6]])
    >>> jacquard(historique, 1, 4, temps41, 0.2)
    array([[3.], [1.], [0.], [2.]])
    >>> jacquard(historique, 4, 1, temps14, 0.2)
    array([[0., 2., 1., 3.]])
    >>> jacquard(historique, 2, 2, temps22, 0.2)
    array([[0., 3.], [2., 1.]])
    """

    nb_ref = len(historique)
    frequence = from_historique_to_frequence(historique)
    J = indice_jacquard(historique)
    E = ens_correlation(J, seuil)
    # on initialise le positionnement à -1 (-1 signifie donc que la place est libre)
    positionnement = -1*np.ones((longueur_rangees, nb_rangees))

    nb_restant = nb_ref
    while nb_restant > 0 :
        # on cherche la référence la plus fréquente parmis celles qui n'ont pas été placées
        i_max = np.argmax(frequence)
        # on cherche une place proche de l'entrée pour i_max
        place_pour_i = proche_entree(positionnement, temps_entrepot)
        # on place i_max
        positionnement[place_pour_i[0], place_pour_i[1]] = i_max
        nb_restant -= 1
        # i_max ne pourra plus être sélectionné dans argmax
        frequence[i_max] = -1
        # on regroupe les références suffisamment corrélées à i_max, qui pas encore placées
        W = [ref for ref in E[i_max] if frequence[ref]>=0]
        # on va placer les références en fonction de leur corrélation à i_max
        J_W = [J[i_max, ref] for ref in W]
        for iter in range(len(W)):
            # on cherche la référence (pas encore placée) la plus corrélé à i_max
            j_max = np.argmax(J_W)
            # on cherche une place proche de i_max pour j_max
            place_pour_j = proche_place(positionnement, place_pour_i, temps_entrepot)
            # on place j_max
            positionnement[place_pour_j[0], place_pour_j[1]] = W[j_max]
            nb_restant -= 1
            # j_max ne pourra plus être sélectionné dans argmax des Jacquard
            J_W[j_max] = -1
            # j_max ne pourra plus être sélectionné dans argmax des freq
            frequence[W[j_max]] = -1

    return positionnement



if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

