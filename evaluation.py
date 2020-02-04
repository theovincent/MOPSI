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


# --- S-shape --- #
def sshape_2(entrepot, commande, longueur_rangees, nb_rangees):
    """
    Calcul le coût d'aller chercher la commande.

    Parametres:
        entrepot (array de taille nb_ref) : entrepot[refi] indique le numéro de la
        rangée de la référence d'indice refi.

        commande (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.

        longueur_rangees (Entier): la longueur des rangées dans l'entrepôt.

        nb_rangees (Entier): le nombre de rangées dans l'entrepôt.

    Return:
        temps (Entier): le nombre de casse que met le robot à aller les deux références

    >>> sshape_2([0, 1], [0, 1], 1, 2)
    10
    """
    # Il y a les couloirs à prendre en compte
    largeur_entrepot = nb_rangees * 2 + 1
    longueur_entrepot = longueur_rangees + 2
    rangee1 = entrepot[commande[0]]
    rangee2 = entrepot[commande[1]]

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
def positionnement_to_entrepot(positionnement):
    """
    Permet de créer un entrepot à partir de positionnement

    Parametres:
        positionnement (Array de taille (longueur_rangees, nb_rangees)): la position
        des références dans l'entrepôt.

    Return:
        entrepot (array de taille nb_ref) : entrepot[refi] indique le numéro de la
        rangée de la référence d'indice refi.

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


def evalue(positionnement, proba):
    """
    Evalue la valeur d'un positionnement, connaîssant
    les probabilités des commandes

    Parametres:
        positionnement (Array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt.

        praba (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.

    Return:
        esperance (Réelle): l'esperance du temps que le robot met à chercher une commande.

    >>> proba = np.array([[0, 1], [1, 0]])
    >>> evalue(np.array([[1, 0]]), proba)
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
            temps_commande = sshape_2(entrepot, [ref1, ref2], longeur_rangees, nb_rangees)
            esperance += temps_commande * proba[ref1, ref2]

    return esperance


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
    NB_RANGEES = NB_REF // 3

    # Chargement d'un positionnement aléatoire
    POS_ALEA = alea(LONGUEUR_RANGEES, NB_RANGEES)

    print(evalue(POS_ALEA, PROBA))
