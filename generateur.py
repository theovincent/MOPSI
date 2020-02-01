"""
Ce module permet de générer un historique de commande.
Il s'agit en réalité des probobilités de chaque commande
"""

from random import randint
from pulp import LpVariable, LpProblem, LpMinimize
import numpy as np


class DimensionError(Exception):
    """Classe d'exception si la dimension n'est pas adaptée"""
    def __repr__(self):
        return "Le nombre de référence doit être un multiple de 3 différent de 3"


def extraction_commande(path):
    """
    Permet d'obtenir une matrice des commandes
    à partir d'un fichier texte.

    Parametres:
        path (Chaîne de caractères) : le chemin où se situe les commandes à extraire

    Return:
        commande (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.
    """
    with open(path, "r") as fichier:
        lines = fichier.readlines()
        commande = np.zeros((len(lines), len(lines[0])))
        nb_reference = len(lines)

        for index_line, line in enumerate(lines):
            line = line.split(" ")
            for index_ref in range(nb_reference):
                commande[index_line, index_ref] = line[index_ref]

    return commande


def matrice_proba(nb_ref):
    """
    Permet de générer une matrice de probabilité de la forme
    [alpha,          0       ,       0        ]
    [  0  ,   alpha - epsilon,    epsilon     ]
    [  0  ,      epsilon     , alpha - epsilon]
    avec alpha une matrice de taille n / 3 avec le réelle alpha à tous les coefficients
    sauf sur la diagonale où il y a des zéros. Pareil pour les autres blocs.

    Parametres:
        nb_ref (Entier positif) : nombre de référence dans l'entrepôt.

    Return:
        praba (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.

    >>> proba = matrice_proba(6)
    >>> proba.shape
    (6, 6)
    """
    # -- Le nombre de référence doit être un multiple de 3 -- #
    if nb_ref % 3 != 0 or nb_ref == 3:
        raise DimensionError

    # -- Paramètres -- #
    # La norme 1 de proba doit être égale à 1
    alpha_1 = (nb_ref / 3) * (nb_ref / 3 - 1)
    alpha = 1 / alpha_1
    epsilon = alpha / randint(2, 10)
    taille_bloc = nb_ref // 3

    # -- Calcul des blocs -- #
    diagonale = np.eye(taille_bloc)
    bloc = np.ones((taille_bloc, taille_bloc)) - diagonale
    bloc_alpha = bloc * alpha
    bloc_epsilon = bloc * epsilon
    bloc_nul = np.zeros((taille_bloc, taille_bloc))

    # -- Calcul des lignes -- #
    proba_ligne1 = np.concatenate((bloc_alpha, bloc_nul, bloc_nul), axis=1)
    proba_ligne2 = np.concatenate((bloc_nul, bloc_alpha - bloc_epsilon, bloc_epsilon), axis=1)
    proba_ligne3 = np.concatenate((bloc_nul, bloc_epsilon, bloc_alpha - bloc_epsilon), axis=1)
    # Assemblage
    probabilite = np.concatenate((proba_ligne1, proba_ligne2, proba_ligne3), axis=0)

    return probabilite


def norme_matrice(matrice):
    """
    Calcul la norme 1 d'une matrice.

    Parametres:
        matrice (Array de taille quelconque)

    Return:
        norme (Réel): norme 1 de la matrice.

    >>> norme_matrice([[1, 3], [4, -4]])
    12
    """
    norme = 0

    for ligne in matrice:
        for element in ligne:
            norme += abs(element)

    return norme


def proba_to_jaccard(proba):
    """
    Génère une matrice la matrice jaccard
    à partir de la matrice des probabilités.

    Parametres:
        praba (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.

    Return:
        jaccard (Array de taille (nb_ref, nb_ref)): matrice des indices de jaccard des commandes.

    >>> test_proba = np.array([[0, 0.5], [0, 0]])
    >>> proba_to_jaccard(test_proba)[0, 1]
    1.0
    """
    nb_reference = len(proba)
    jaccard = np.zeros((nb_reference, nb_reference))

    for ref1 in range(nb_reference):
        for ref2 in range(nb_reference):
            proba_ref1_ref2 = proba[ref1, ref2]
            if proba_ref1_ref2 == 0:
                jaccard[ref1, ref2] = 0
            else:
                proba_sans_ref2 = sum(proba[ref1, :]) - proba_ref1_ref2
                proba_sans_ref1 = sum(proba[:, ref2]) - proba_ref1_ref2
                proba_avec_sans = proba_ref1_ref2 + proba_sans_ref1 + proba_sans_ref2
                jaccard[ref1, ref2] = proba_ref1_ref2 / proba_avec_sans

    return jaccard


def jaccard_to_proba(jaccard):
    """
    Renvoie une matrice de probabilité correspondant à la matrice de jaccard.
    """
    # -- Définissons des paramètres -- #
    nb_reference = len(jaccard)

    # -- Définissons les variables -- #
    ref = ["0"] * nb_reference
    for i in range(nb_reference):
        ref[i] = "ref{}".format(i)

    commandes = ["({}, {})".format(refi, refj) for refi in ref for refj in ref]

    var_ref = LpVariable.dicts("Reference", commandes, lowBound=0, upBound=1000, cat='float')

    # -- Définissons le problème -- #
    prob = LpProblem("Ax_B", LpMinimize)

    # -- Définissons la fonction de coût -- #
    prob += 1

    # -- Définissons les contraintes -- #
    # Contraintes liées à la définition de la matrice de jaccard
    # (x_i,j + J_i,j * sum(x_i,k) + J_i,j * sum(x_p,j)) * J_i,j = x_i,j pour k != j et p != j
    for ref1 in range(nb_reference):
        for ref2 in range(nb_reference):
            jaccard_ref1_ref2 = jaccard[ref1, ref2]
            ref1_ref2 = var_ref[commandes[ref1 * nb_reference + ref2]]
            if jaccard_ref1_ref2 == 0:
                prob += ref1_ref2 == 0
            else:
                ref1_autres = 0
                ref2_autres = 0
                for index_ref in range(nb_reference):
                    if index_ref != ref2:
                        ref1_autres += var_ref[commandes[ref1 * nb_reference + index_ref]]
                    if index_ref != ref1:
                        ref2_autres += var_ref[commandes[index_ref * nb_reference + ref2]]

                prob += (ref1_ref2 + ref1_autres + ref2_autres) * jaccard_ref1_ref2 == ref1_ref2

    # Contraintes liées à la définition d'une probabilité
    # sum(x_i,j) = 1
    somme = 0
    for refj in range(nb_reference):
        for refi in range(nb_reference):
            somme += var_ref[commandes[refi * nb_reference + refj]]
    prob += somme == 1

    # Contraintes liées au fait que dans une commande, il a deux références différentes
    # x_i,i = 0
    for refi in range(nb_reference):
        prob += var_ref[commandes[refi * nb_reference + refi]] == 0

    # -- Résolvons le problème -- #
    prob.solve()

    # -- Enregistrons les résultats -- #
    probabilites = np.zeros((nb_reference, nb_reference))
    index_refi = 0
    index_refj = 0
    for variable in prob.variables():
        if variable.name[-1] == ")":
            probabilites[index_refi, index_refj] = variable.varValue
        index_refj += 1
        if index_refj == nb_reference:
            index_refj = 0
            index_refi += 1

    return probabilites


def store_matrice(matrice, file_name):
    """
    Permet d'enregistrer la matrice en format texte.

    Parametres:
        matrice (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.

        file_name (Chaîne de caractères): chemin du nouveau fichier.
    """
    nb_reference = len(matrice)

    with open(file_name, 'w') as file:
        for ref1 in range(nb_reference):
            string_row = ""
            for ref2 in range(nb_reference):
                # On arrondi à la 3ième décimale
                string_row += str(round(matrice[ref1, ref2], 3)) + " "
            string_row += "\n"
            file.write(string_row)


def generation_commande(nb_ref, nom_instance):
    """
    Génère un fichier texte donnant les probabilités.
    Renvoie la matrice des probabilités.

    Parametres:
        nb_ref (Entier positif) : nombre de référence dans l'entrepôt.

        nom_instance (Chaîne de caractères): chemin du nouveau fichier.

    Return:
        commande (Array de taille (nb_ref, nb_ref)): matrice des probabilités des commandes.
    """
    try:
        probabilite = matrice_proba(nb_ref)
        store_matrice(probabilite, nom_instance + ".txt")
    except DimensionError:
        print("Le nombre de référence doit être un multiple de 3 différent de 3")

    return probabilite


if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

    # -- Paramètres -- #
    NB_REF = 9
    PROBA = "test"

    generation_commande(NB_REF, PROBA)
