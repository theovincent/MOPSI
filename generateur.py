import numpy as np
import numpy.random as rd
from pulp import LpVariable, LpProblem, LpMinimize


class DimensionError(Exception):
    """Classe d'exception si la dimension n'est pas adaptée"""
    def __repr__(self):
        return "Le nombre de référence doit être un multiple de 3 différent de 3"


def extraction_commande(path):
    """
    Permet d'obtenir une matrice des commandes
    à partir d'un fichier texte.
    """
    with open(path, "r") as fichier:
        lines = fichier.readlines()
        commande = np.zeros((len(lines), len(lines[0])))
        nb_ref = len(lines)

        for index_line, line in enumerate(lines):
            line = line.split(" ")
            for index_ref in range(nb_ref):
                commande[index_line, index_ref] = line[index_ref]

    return commande


def matrice_proba(nb_ref):
    """
    Permet de générer une matrice de probabilité de la forme
    [alpha,          0       ,       0        ]
    [  0  ,   alpha - epsilon,    epsilon     ]
    [  0  ,      epsilon     , alpha - epsilon]
    avec alpha une matrice de taille n / 3 avec alpha à tous les coefficients
    sauf sur la diagonale où il y a des zéros. Pareil pour les autres blocs.
    """
    # -- Le nombre de référence doit être un multiple de 3 -- #
    if nb_ref % 3 != 0 or nb_ref == 3:
        raise DimensionError

    # -- Paramètres -- #
    # La norme 1 de proba doit être égale à 1
    alpha = 3 / ((nb_ref - 3) * nb_ref)
    epsilon = alpha / 7
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
    proba = np.concatenate((proba_ligne1, proba_ligne2, proba_ligne3), axis=0)

    return proba


def norme_matrice(matrice):
    """
    Calcul la norme 1 d'une matrice
    >>> norme_matrice([[1, 3], [4, 4]])
    12
    """
    norme = 0

    for ligne in matrice:
        norme += sum(ligne)

    return norme


def proba_to_jacquard(proba):
    """
    Génère une matrice la matrice Jacquard
    à partir de la matrice des probabilités
    """
    nb_ref = len(proba)
    jacquard = np.zeros((nb_ref, nb_ref))

    for ref1 in range(nb_ref):
        for ref2 in range(nb_ref):
            proba_ref1_ref2 = proba[ref1, ref2]
            if proba_ref1_ref2 == 0:
                jacquard[ref1, ref2] = 0
            else:
                proba_sans_ref2 = sum(proba[ref1, :]) - proba_ref1_ref2
                proba_sans_ref1 = sum(proba[:, ref2]) - proba_ref1_ref2
                jacquard[ref1, ref2] = proba_ref1_ref2 / (proba_ref1_ref2 + proba_sans_ref1 + proba_sans_ref2)

    return jacquard


def jacquard_to_proba(jacquard):
    """
    Renvoie une matrice de probabilité correspondant à la matrice de Jacquard.
    """
    # -- Définissons des paramètres -- #
    nb_ref = len(jacquard)
    nb_commandes = nb_ref * nb_ref

    # -- Définissons les variables -- #
    ref = ["0"] * nb_ref
    for i in range(nb_ref):
        ref[i] = "ref{}".format(i)

    commandes = ["({}, {})".format(refi, refj) for refi in ref for refj in ref]

    var_ref = LpVariable.dicts("Reference", commandes, lowBound=0, upBound=1000, cat='float')

    # -- Définissons le problème -- #
    prob = LpProblem("Ax_B", LpMinimize)

    # -- Définissons la fonction de coût -- #
    prob += 1

    # -- Définissons les contraintes -- #
    # Contraintes liées à la définition de la matrice de Jacquard
    # (x_i,j + J_i,j * sum(x_i,k) + J_i,j * sum(x_p,j)) * J_i,j = x_i,j pour k != j et p != j
    for ref1 in range(nb_ref):
        for ref2 in range(nb_ref):
            jacquard_ref1_ref2 = jacquard[ref1, ref2]
            ref1_ref2 = var_ref[commandes[ref1 * nb_ref + ref2]]
            if jacquard_ref1_ref2 == 0:
                prob += ref1_ref2 == 0
            else:
                ref1_autres = 0
                ref2_autres = 0
                for index_ref in range(nb_ref):
                    if index_ref != ref2:
                        ref1_autres += var_ref[commandes[ref1 * nb_ref + index_ref]]
                    if index_ref != ref1:
                        ref2_autres += var_ref[commandes[index_ref * nb_ref + ref2]]

                prob += (ref1_ref2 + ref1_autres + ref2_autres) * jacquard_ref1_ref2 == ref1_ref2

    # Contraintes liées à la définition d'une probabilité
    # sum(x_i,j) = 1
    prob += sum([var_ref[commandes[refi * nb_ref + refj]] for refi in range(nb_ref) for refj in range(nb_ref)]) == 1

    # Contraintes liées au fait que dans une commande, il a deux références différentes
    # x_i,i = 0
    for refi in range(nb_ref):
        prob += var_ref[commandes[refi * nb_ref + refi]] == 0

    # -- Résolvons le problème -- #
    prob.solve()

    # -- Enregistrons les résultats -- #
    probabilites = np.zeros((nb_ref, nb_ref))
    index_refi = 0
    index_refj = 0
    for v in prob.variables():
        if v.name[-1] == ")":
            probabilites[index_refi, index_refj] = v.varValue
        index_refj += 1
        if index_refj == nb_ref:
            index_refj = 0
            index_refi += 1

    return probabilites


def store_matrice(matrice, file_name):
    """
    Permet d'enregistrer la matrice en format texte.
    """
    nb_reference = len(matrice)

    with open(file_name, 'w') as f:
        for ref1 in range(nb_reference):
            string_row = ""
            for ref2 in range(nb_reference):
                # On arrondi à la 3ième décimale
                string_row += str(round(matrice[ref1, ref2], 3)) + " "
            string_row += "\n"
            f.write(string_row)


def generation_commande(nb_ref, nom_instance):
    """
    Génère un fichier texte donnant les probabilités.
    Renvoie la matrice des probabilités.
    """
    try:
        proba = matrice_proba(nb_ref)
        store_matrice(proba, nom_instance + ".txt")
    except DimensionError:
        print("Le nombre de référence doit être un multiple de 3 différent de 3")

    return proba


if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

    # -- Paramètres -- #
    nb_ref = 9

    try:
        proba = matrice_proba(nb_ref)
        jacquard = proba_to_jacquard(proba)
        proba_gene = jacquard_to_proba(jacquard)
        # print(jacquard)
        print(proba_gene)
        # print(norme_matrice(proba_gene))
        print("Jacquard Théorique")
        print(proba_to_jacquard(proba_gene))
    except DimensionError:
        print("Le nombre de référence doit être un multiple de 3 différent de 3")
