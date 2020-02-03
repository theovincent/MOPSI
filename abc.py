import numpy as np
import random
# rappel : les rangées sont numérotées à partir de 0



## Classer les références selon leur fréquence d'apparition


# historique est une matrice 2D (nb_ref)*(nb_ref) donnant les probas des couples de ref
# frequence est une matrice 1D (nb_ref) donnant la proba d'une ref
def from_historique_to_frequence(historique):
    nb_ref = len(historique[0])
    frequence = np.zeros(nb_ref)
    for ref in range(nb_ref):
        for ref2 in range(nb_ref):
            frequence[ref] += historique[ref, ref2]
    return frequence



# donne le rang de chaque element de la liste (si la liste était triée)
def rang_triee(liste):
    ordre = [i for i in range(len(liste))]
    # on fait un tri par selection en répercutant toutes les modifs sur la liste ordre
    n = len(liste)
    for i in range(n) :
        k = i
        for j in range(i+1,n) :
            if liste[k] > liste[j] :
                k = j
        liste[k], liste[i] = liste[i], liste[k]
        ordre[k], ordre[i] = ordre[i], ordre[k]
    rang = np.zeros(len(liste))
    for i in range(len(liste)):
        rang[ordre[i]] = i
    return rang

# donne le rang de chaque référence (en fonction de leur fréquence)
def rang_frequence(historique):
    frequence = from_historique_to_frequence(historique)
    rang_ref = rang_triee(frequence)
    return rang_ref


## Regrouper les rangées en 3 groupes


# rangees_classe[i] correspond à la liste (pas un array) des rangées dans la classe i
def classify_rangees(nb_rangees):

    rangees_classe = [[], [], []]

    # cas nb_rangees < 4 : on a moins de 3 classes
    if nb_rangees == 1 :
        # on rajoute la seule rangées dans la classe A
        rangees_classe[0].append(0)
    if nb_rangees == 2 :
        # on rajoute la rangée 0 dans la classe A (car en face de l'entrée) et l'autre dans la classe B
        rangees_classe[0].append(0)
        rangees_classe[1].append(1)
    if nb_rangees == 3 :
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
        # les 2 allées les plus proches sont les rangées ((nb_rangees+1)/2 - 1) et (nb_rangees+1)/2 - 2)
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
        nb_rangees_classeB = int(nb_rangees_gauche/3) + 1 # arbitraire
        # à gauche on part de la rangee du milieu (celle de classe A)
        # et on compte nb_rangees_classeB vers la gauche, et on les mets dans la classe B
        # le reste vers la gauche va dans la classe C
        for rangeeB in range(limite_gauche - nb_rangees_classeB, limite_gauche):
            rangees_classe[1].append(rangeeB)
        for rangeeC in range(0, limite_gauche - nb_rangees_classeB):
            rangees_classe[2].append(rangeeC)
        # on fait de même à droite
        for rangeeB in range(limite_droite + 1, limite_droite + 1 + nb_rangees_classeB):
            rangees_classe[1].append(rangeeB)
        for rangeeC in range(limite_droite + 1 + nb_rangees_classeB, nb_rangees):
            rangees_classe[2].append(rangeeC)

    return rangees_classe


## Positionner les références selon la méthode ABC


# crée 3 classes de références, rangées par ordre de grandeur de fréquence d'apparition
def ABC(historique, nb_rangees, longueur_rangees):

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
        elif rang_ref[ref] < nb_ref_classeB :
            classeB.append(ref)
        else :
            classeC.append(ref)
    random.shuffle(classeA)
    random.shuffle(classeB)
    random.shuffle(classeC)

    # on peut enfin attribuer une position à chaque référence
    positionnement = -1*np.ones((longueur_rangees, nb_rangees))
    # classe A
    compteur_ref = 0
    for rangee in rangees_classe[0]:
        for casier in range(longueur_rangee):
            compteur_ref += 1
            positionnement[casier, rangee] = classeA[compteur_ref]
    # classe B
    compteur_ref = 0
    for rangee in rangees_classe[1]:
        for casier in range(longueur_rangee):
            compteur_ref += 1
            positionnement[casier, rangee] = classeB[compteur_ref]
    # classe C
    compteur_ref = 0
    for rangee in rangees_classe[2]:
        for casier in range(longueur_rangee):
            compteur_ref += 1
            positionnement[casier, rangee] = classeC[compteur_ref]

    return positionnement


## Tests


if __name__ == "__main__":
    print(classify_rangees(13))


