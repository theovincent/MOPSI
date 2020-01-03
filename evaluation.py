import numpy as np
## S-shape

def sshape_2(nb_rangees, longueur_rangees, positionnements, commande):

    largeur_entrepot = nb_rangees*2 + 1
    longueur_entrepot = longueur_rangees + 2
    positionnements = positionnements + 1 # les rangees sont numerotees à partir de 0

    rangee1 = positionnements[commande[0]]
    rangee2 = positionnements[commande[1]]
    x_milieu = (largeur_entrepot + 1)/2 # largeur_entrepot est impaire
    temps = 1 + abs(1+2*rangee1 - x_milieu) + (longueur_entrepot - 1)

    if (rangee1==rangee2):
        temps *= 2 # on fait le même chemin pour le retour
    else:
        temps += 2*abs(rangee2-rangee1) + (longueur_entrepot - 1) + abs(1+2*rangee2 - x_milieu) + 1

    return temps


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


## Evaluation une configuration donnée

# entrepot est une matrice 2D (longueur_rangees)*(nb_rangees) correspondant à une vue du dessus de l'entrepôt
# positionnements est une matrice ligne (longueur_rangees*nb_rangees) donnant la rangee de chaque référence
# historique est une matrice 2D (longueur_rangees*nb_rangees)*(longueur_rangees*nb_rangees) donnant les probas

def entrepot_to_positionnements(nb_rangees, longueur_rangees, entrepot):

    positionnements = np.zeros(nb_rangees*longueur_rangees)
    for l in range(longueur_rangees):
        for r in range(nb_rangees):
            positionnements[entrepot[l,r]] = r

    return positionnements


def evalue(entrepot, historique):

    nb_rangees = len(entrepot[0])
    longueur_rangees = len(entrepot)
    positionnements = entrepot_to_positionnements(nb_rangees, longueur_rangees, entrepot)

    esperance = 0
    for i in range(nb_rangees*longueur_rangees):
        for j in range(nb_rangees*longueur_rangees):
            esperance += sshape_2(nb_rangees, longueur_rangees, positionnements, [i,j]) * historique[i,j]

    return esperance


## Tests

entrepot = np.array([[1, 0, 5], [2, 6, 8], [4, 3, 7]])
print(entrepot)

positionnements = entrepot_to_positionnements(3, 3, entrepot)
print(positionnements)
print(positionnements + 1)

commande = [3, 8]
print(sshape_2(3, 3, positionnements, commande))

# historique =
# print(evalue(3, 3, entrepot, historique))

