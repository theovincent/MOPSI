import numpy as np
import random
# rappel : les rangées sont numérotées à partir de 0


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
        for ref2 in range(nb_ref):
            frequence[ref] += historique[ref, ref2]
    return frequence



def rang_frequence(historique):
    """
    Donne le rang de chaque référence (en fonction de leur fréquence)

    Paramètres:
        historique (array de taille (nb_ref, nb_ref)) : matrice des probabilités des commandes.

    Return:
        rang_ref (array de taille (nb_ref)) : rang_ref[refi] = rang de refi lorsque les références sont rangées par fréquences croissantes

    >>> rang_frequence(np.array([[0.3, 0.1, 0.2], [0.1, 0, 0.4], [0.2, 0.4, 0]]))
    array([0., 2., 1.])
    >>> rang_frequence(np.array([[0.1, 0.4, 0.5, 0.3], [0.4, 0, 1, 0], [0.5, 1, 0.2, 0.7], [0.3, 0, 0.7, 0.3]]))
    array([2., 1., 0., 3.])
    """
    frequence = from_historique_to_frequence(historique)
    nb_ref = len(historique[0])
    rang_ref = -1*np.zeros(nb_ref)
    for k in range(nb_ref):
        ref_max = np.argmax(frequence)
        rang_ref[k] = ref_max
        frequence[ref_max] = -1
    return rang_ref



def classify_rangees(nb_rangees):
    """
    Regroupe les rangées en 3 groupes, 1 pour chaque classe.

    Paramètres:
        nb_rangees (entier) : correspond au nombre de rangées dans l'entrepôt

    Return:
        rangees_classe (liste de 3 listes) : rangees_classe[0] correspond à la liste des rangees allouées pour la classe A, rangees_classe[1] pour la classe B et rangees_classe[2] pour la classe C

    >>> classify_rangees(4)
    [[1], [0, 2], [3]]
    >>> classify_rangees(7)
    [[2, 3], [1, 4], [0, 5, 6]]
    >>> classify_rangees(14)
    [[6], [3, 4, 5, 7, 8, 9], [0, 1, 2, 10, 11, 12, 13]]
    """
    rangees_classe = [[], [], []]

    # cas nb_rangees < 4 : on a moins de 3 classes
    if nb_rangees == 1 :
        # on rajoute la seule rangées dans la classe A
        rangees_classe[0].append(0)
    elif nb_rangees == 2 :
        # on rajoute la rangée 0 dans la classe A (car en face de l'entrée) et l'autre dans la classe B
        rangees_classe[0].append(0)
        rangees_classe[1].append(1)
    elif nb_rangees == 3 :
        # les rangées 0 et 1 sont à équidistance de l'entrée, on les mets dans la classe A
        rangees_classe[0].append(0)
        rangees_classe[0].append(1)
        rangees_classe[1].append(2)

    # cas nb_rangees >= 4 : on a 3 classes
    else:

        # détermination de la classe A

        # si on a un nombre de rangées pair, alors l'entrée se trouve en face d'une allée
        # cette allée est celle de la rangée numéro (nb_rangees/2 - 1)
        # cette rangée forme la classe A
        if nb_rangees%2 == 0 :
            rangees_classe[0].append(int(nb_rangees/2 - 1))
        # si on a un nombre de rangées impair, alors l'entrée se trouve en face d'une rangée
        # les 2 allées les plus proches sont celles des rangées ((nb_rangees+1)/2 - 1) et (nb_rangees+1)/2 - 2)
        # ces 2 rangées forment la classe A
        else :
            rangees_classe[0].append(int((nb_rangees+1)/2 - 2))
            rangees_classe[0].append(int((nb_rangees+1)/2 - 1))

        # détermination des classes B et C

        # on regarde la première rangée de classe A (donc la limite gauche)
        limite_gauche = int(rangees_classe[0][0])
        # on regarde la dernière rangée de classe A (donc la limite droite)
        limite_droite = int(rangees_classe[0][-1])
        # on calcule le nombre de rangées à gauche et à droite restantes
        # il y a une rangee de plus restante à droite (cf schéma)
        nb_rangees_gauche = limite_gauche
        nb_rangees_droite = nb_rangees_gauche + 1
        # on prendra autant de rangees de classe B de chaque côté
        nb_rangees_classeB = int(nb_rangees_gauche/3) + 1  # arbitraire
        # à gauche on part de la rangee du milieu (celle de classe A)
        # et on compte nb_rangees_classeB vers la gauche, et on les mets dans la classe B
        # le reste vers la gauche va dans la classe C
        for rangeeB in range(limite_gauche - nb_rangees_classeB, limite_gauche):
            rangees_classe[1].append(rangeeB)
        for rangeeC in range(0, limite_gauche - nb_rangees_classeB):
            rangees_classe[2].append(rangeeC)
        # on fait de même à droite
        for rangeeB in range(limite_droite + 1, limite_droite + nb_rangees_classeB + 1):
            rangees_classe[1].append(rangeeB)
        for rangeeC in range(limite_droite + 1 + nb_rangees_classeB, nb_rangees):
            rangees_classe[2].append(rangeeC)

    return rangees_classe



def ABC(historique, nb_rangees, longueur_rangees):
    """
    Regroupe les références en 3 groupes, 1 pour chaque classe.

    Paramètres:
        historique (array de taille (nb_ref, nb_ref)) : matrice des probabilités des commandes.

        nb_rangees (entier) : correspond au nombre de rangées dans l'entrepôt.

        longueur_rangees (entier) : correspond à la longueur d'une rangée.

    Return:
        positionnement (array de taille (longueur_rangees, nb_rangees): la position
        des références dans l'entrepôt.
    """
    nb_ref = nb_rangees*longueur_rangees
    rang_ref = rang_frequence(historique)

    # on calcule le nombre de références par classe
    rangees_classe = classify_rangees(nb_rangees)
    nb_ref_classeA = longueur_rangees*len(rangees_classe[0])
    nb_ref_classeB = longueur_rangees*len(rangees_classe[1])
    nb_ref_classeC = longueur_rangees*len(rangees_classe[2])

    # on remplie les classes avec les références
    # pour cela on crée 3 listes (une par classe) que l'on pourra shuffle pour rendre
    # le positionnement aléatoire dans chaque classe
    classeA = []
    classeB = []
    classeC = []
    for ref in range(nb_ref):
        if rang_ref[ref] < nb_ref_classeA :
            classeA.append(ref)
        elif rang_ref[ref] < nb_ref_classeA + nb_ref_classeB :
            classeB.append(ref)
        else :
            classeC.append(ref)
    random.shuffle(classeA)
    random.shuffle(classeB)
    random.shuffle(classeC)

    # on peut enfin attribuer une position à chaque référence
    positionnement = -1*np.ones((longueur_rangees, nb_rangees))
    # classe A
    casier = 0
    compteur_rangee = 0
    rangee = rangees_classe[0][compteur_rangee]
    for ref in classeA:
        if casier < longueur_rangees:
            positionnement[casier, rangee] = ref
        else :
            casier = 0
            compteur_rangee += 1
            rangee = rangees_classe[0][compteur_rangee]
            positionnement[casier, rangee] = ref
        casier += 1
    # classe B
    if len(classeB) == 0:
        return positionnement
    else :
        casier = 0
        compteur_rangee = 0
        rangee = rangees_classe[1][compteur_rangee]
        for ref in classeB:
            if casier < longueur_rangees:
                positionnement[casier, rangee] = ref
            else :
                casier = 0
                compteur_rangee += 1
                rangee = rangees_classe[1][compteur_rangee]
                positionnement[casier, rangee] = ref
            casier += 1
    # classe C
    if len(classeC) == 0:
        return positionnement
    else :
        casier = 0
        compteur_rangee = 0
        rangee = rangees_classe[2][compteur_rangee]
        for ref in classeC:
            if casier < longueur_rangees:
                positionnement[casier, rangee] = ref
            else :
                casier = 0
                compteur_rangee += 1
                rangee = rangees_classe[2][compteur_rangee]
                positionnement[casier, rangee] = ref
            casier += 1

    return positionnement




if __name__ == "__main__":
    # -- Doc tests -- #
    import doctest
    doctest.testmod()

    historique = np.array([[0.1, 0.4, 0.5, 0.3], [0.4, 0, 1, 0], [0.5, 1, 0.2, 0.7], [0.3, 0, 0.7, 0.3]])
    print(ABC(historique, 2, 2))

