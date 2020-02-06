"""
Ce module permet d'évaluer un emplacement en utilisant la méthode du S-shape.
-------
Paramètres
-------
entrepot est une matrice ligne de longueur : longueur_rangees * nb_rangees.
    entrepot[i] donne le numéro de la rangée de la i-ième référence.

positionnements est une matrice 2D  de taille : longueur_rangees * nb_rangees donnant.
    Il s'agit de la position de chaque référence. C'est-à-dire, pos[i, j] est le numéro
    de la référence sur le i-ième emplacement de la j-ième colonne.

historique est une matrice 2D de taille : nb_ref * nb_ref donnant les probas de chaque
    couple de références d'être commandée.
"""

from pathlib import Path
import numpy as np
from alea import alea
from generateur import extraction_commande



def sshape(longueur_rangees, nb_rangees, commande):
    """
    Calcul le coût d'aller chercher la commande.

    Parametres:
        commande (array de taille 2) : commande[0] correspond à la position [rangee, casier] de la 1e référence à aller chercher, commande[1] à la position de la 2e

        longueur_rangees (Entier): la longueur des rangées dans l'entrepôt.

        nb_rangees (Entier): le nombre de rangées dans l'entrepôt.

    Return:
        temps (Entier): le nombre de casse que met le robot à aller les deux références

    >>> sshape(3, 3, [[0, 2], [1, 0]])
    14
    >>> sshape(3, 3, [[1, 0], [1, 1]])
    12
    >>> sshape(3, 3, [[0, 2], [2, 0]])
    18
    """
    # Il y a les couloirs à prendre en compte
    largeur_entrepot = nb_rangees * 2 + 1
    longueur_entrepot = longueur_rangees + 2
    rangee1 = commande[0][0]
    casier1 = commande[0][1]
    rangee2 = commande[1][0]
    casier2 = commande[1][1]

    # L'entrée est au milieu de l'entrepot. largeur_entrepot est impaire.
    entree = largeur_entrepot // 2
    num_rangee1 = 2 * rangee1 + 1
    # On passe à droite des rangées
    num_allee_ref1 = num_rangee1 + 1
    # Le coût de récupération de la première référence est :
    # temps = coût_d'entrée + coût_devant_allée1 + cout_traverser_allée1
    temps = 1 + abs(num_allee_ref1 - entree) + (longueur_entrepot - 1)

    if rangee1 == rangee2:
        # On fait le même chemin pour le retour
        temps *= 2
    else:
        num_rangee2 = 2 * rangee2 + 1
        # On passe à droite des rangées
        num_allee_ref2 = num_rangee2 + 1
        # Le coût pour aller prendre la 2ième référence et revenir est :
        # coût_devant_allée2 + coût_tranversée_allée2 + coût_devant_sortie + coût_sortie
        temps += 2*abs(rangee2-rangee1) + (longueur_entrepot - 1) + abs(num_allee_ref2 - entree) + 1

    return temps



def evalue_entrepot(longueur_rangees, nb_rangees):
    """
    Evalue le temps de récupération pour chaque paire de positions.

    Parametres:
        longueur_rangees (Entier): la longueur des rangées dans l'entrepôt.

        nb_rangees (Entier): le nombre de rangées dans l'entrepôt

    Return:
        temps (Array de taille (nb_ref, nb_ref)): temps[i, j] du temps que le robot met à chercher 2 objets en position i et j dans l'entrepôt (attention, les positions sont codées en 1D : [rangee, casier] = [rangee + casier*nb_rangees])

    >>> evalue_entrepot(1, 4)
    array([[10., 10., 14., 18.], [10., 6., 10., 14.], [14., 10., 10., 14.], [18., 14., 14., 14.]])
    >>> evalue_entrepot(2, 2)
    array([[8., 12., 8., 12.], [12., 12., 12., 12.], [8., 12., 8., 12.], [12., 12., 12., 12.]])
    """
    nb_places = longueur_rangees*nb_rangees
    temps = np.zeros((nb_places, nb_places))
    for rangee1 in range(nb_rangees):
        for casier1 in range(longueur_rangees):
            for rangee2 in range(nb_rangees):
                for casier2 in range(longueur_rangees):
                    commande = [[rangee1, casier1], [rangee2, casier2]]
                    place1 = rangee1 + casier1*nb_rangees
                    place2 = rangee2 + casier2*nb_rangees
                    temps[place1, place2] = sshape(longueur_rangees, nb_rangees, commande)
    return temps



def inverse_positionnement(positionnement):
    """
    Attribue à chaque référence sa position, à partir de la matrice qui associe à chaque position sa référence

    Parametres:
        positionnement (Array de taille (longueur_rangees, nb_rangees)): positionnement[i, j] renvoie la référence placée au casier j de la rangée i

    Return:
        entrepot (array de taille nb_ref) : entrepot[refi] = [rangee, casier] qui indique la rangée et le casier où est placé refi

    >>> inverse_positionnement(np.array([[3, 1], [0, 2]]))
    [[0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [0.0, 0.0]]
    """
    longueur_rangees = len(positionnement)
    nb_rangees = len(positionnement[0])
    nb_ref = nb_rangees * longueur_rangees
    entrepot = np.zeros((nb_ref, 2))

    for rangee in range(nb_rangees):
        for casier in range(longueur_rangees):
            entrepot[positionnement[casier, rangee], 0] = rangee
            entrepot[positionnement[casier, rangee], 1] = casier

    return entrepot



def evalue_position(positionnement, temps_entrepot, proba):
    """
    Evalue le temps moyen d'un positionnement.

    Parametres:
        positionnement (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt.

        temps_entrepot (Array de taille (nb_ref, nb_ref)): temps[i, j] du temps que le robot met à chercher 2 objets en position i et j dans l'entrepôt (attention, les positions sont codées en 1D : [rangee, casier] = [rangee + casier*nb_rangees])

        proba (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.

    Return:
        esperance (entier): le temps moyen mis pour collecter une commande

    >>> evalue_position(np.array([[1, 3], [0, 2]]), evalue_entrepot(2, 2), np.array([[0.0, 0.2, 0.4, 0.0], [0.2, 0, 0.1, 0.1], [0.4, 0.1, 0.0, 0.2], [0.0, 0.1, 0.3, 0.0]]))
    11.2
    """
    nb_rangees = len(positionnement[0])
    longueur_rangees = len(positionnement)
    nb_ref = nb_rangees * longueur_rangees
    position_ref = inverse_positionnement(positionnement)

    esperance = 0
    for ref1 in range(nb_ref):
        for ref2 in range(ref1 + 1, nb_ref):
            position_ref1 = int(position_ref[ref1, 0] + position_ref[ref1, 1]*nb_rangees)
            position_ref2 = int(position_ref[ref2, 0] + position_ref[ref2, 1]*nb_rangees)
            temps_commande = temps_entrepot[position_ref1, position_ref2]
            esperance += temps_commande * proba[ref1, ref2]

    return esperance



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Paramètre pour charger les probabilités des commandes
    PATH_COMMANDE = Path("test.txt")
    PROBA = extraction_commande(PATH_COMMANDE)
    NB_REF = len(PROBA)

    # Définition arbitraire de la longueur et du nombre des rangées
    LONGUEUR_RANGEES = 3
    NB_RANGEES = NB_REF // LONGUEUR_RANGEES

    # Chargement d'un positionnement aléatoire
    POS_ALEA = alea(LONGUEUR_RANGEES, NB_RANGEES)

    #print(evalue(POS_ALEA, PROBA))
