import numpy as np


# --- S-shape --- #
def sshape_2(entrepot, commande, nb_rangees, longeur_rangees):
    """
    Calcul le coût d'aller chercher la commande.
    >>> sshape_2([0, 1], [0, 1], 2, 1)
    10.0
    """
    # Il y a les couloirs à prendre en compte
    largeur_entrepot = nb_rangees * 2 + 1
    longueur_entrepot = longeur_rangees + 2
    entrepot = entrepot + np.ones(len(entrepot))  # On passe à droite des rangées
    rangee1 = entrepot[commande[0]]
    rangee2 = entrepot[commande[1]]

    # L'entrée est au milieu de l'entrepot. largeur_entrepot est impaire
    entree = (largeur_entrepot + 1) / 2
    num_allee_ref1 = 1 + 2 * rangee1
    # Le coût de récupération de la première référence est :
    # temps = coût_d'entrée + coût_devant_allée1 + cout_traverser_allée1
    temps = 1 + abs(num_allee_ref1 - entree) + (longueur_entrepot - 1)

    if rangee1 == rangee2:
        # On fait le même chemin pour le retour
        temps *= 2
    else:
        num_allee_ref2 = 1 + 2 * rangee2
        # Le coût pour aller prendre la 2ième référence et revenir est :
        # coût_devant_allée2 + coût_tranversée_allée2 + coût_devant_sortie + coût_sortie
        temps += 2*abs(rangee2-rangee1) + (longueur_entrepot - 1) + abs(num_allee_ref2 - entree) + 1

    return temps


"""
def sshape_qlc(nb_rangees, longueur_rangees, positionnements, commande):

    largeur_entrepot = nb_rangees*2 + 1
    longueur_entrepot = longueur_rangees + 2
    positionnements = positionnements + 1 # les rangees sont numerotees à partir de 0

    rangees_a_visiter = []
    for ref in commande:
        if (positionnements[ref]) not in rangees_a_visiter:
            rangees_a_visiter.append(positionnements[ref])
    rangees_a_visiter.sort()

    temps = 1 # on rentre dans l'entrepot
    x_milieu = (largeur_entrepot + 1)/2 # largeur_entrepot est impair
    x_robot = x_milieu

    for r in rangees_a_visiter:
        temps += abs(1+2*r- x_robot) + (longueur_entrepot - 1)
        x_robot = 1+2*r

    # on calcule le temps restants pour sortir de l'entrepot
    if (len(rangees_a_visiter)%2 != 0): # si on se retrouve au fond de l'entrepot
        temps += longueur_entrepot - 1
    temps += abs(x_robot - x_milieu) + 1

    return temps
"""

# --- Evaluation une configuration donnée --- #
"""
entrepot est une matrice ligne (longueur_rangees * nb_rangees). entrepot[i] donne la rangée de la i-ième référence.
positionnements est une matrice 2D (longueur_rangees * nb_rangees) donnant la position de chaque référence.
C'est-à-dire, pos[i, j] est le numéro de la référence sur le i-ième emplacement de la j-ième colonne.
historique est une matrice 2D (longueur_rangees*nb_rangees)*(longueur_rangees*nb_rangees) donnant les probas
de chaque couple de références d'apparaître.
"""


def positionnement_to_entrepot(positionnement):
    """
    Permet de créer un entrepot à partir de positionnement
    >>> list(positionnement_to_entrepot(np.array([[0, 1], [3, 2]])))
    [0.0, 1.0, 1.0, 0.0]
    """
    longeur_rangees = len(positionnement)
    nb_rangees = len(positionnement[0])
    entrepot = np.zeros(nb_rangees * longeur_rangees)

    for profondeur in range(longeur_rangees):
        for index_rangee in range(nb_rangees):
            entrepot[int(positionnement[profondeur, index_rangee])] = index_rangee

    return entrepot


def evalue(positionnement, historique):
    """
    Evalue la valeur d'un positionnement, connaîssant l'historique
    >>> historique = np.array([[0, 1], [1, 0]])
    >>> evalue(np.array([[1, 0]]), historique)
    10.0
    """
    nb_rangees = len(positionnement[0])
    longeur_rangees = len(positionnement)
    nb_ref = nb_rangees * longeur_rangees
    entrepot = positionnement_to_entrepot(positionnement)

    # -- Calculons l'espérance du positionnement -- #
    esperance = 0
    for ref1 in range(nb_ref):
        # [ref1, ref2] et [ref2, ref1] sont les mêmes commandes
        for ref2 in range(ref1 + 1, nb_ref):
            esperance += sshape_2(entrepot, [ref1, ref2], nb_rangees, longeur_rangees) * historique[ref1, ref2]

    return esperance


if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

    commande = np.array([[0, 1], [1, 0]])
    print(evalue(np.array([[1, 0]]), commande))


