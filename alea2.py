import numpy.random as rd
import numpy as np

# --- Positionne les références de manière aléatoir dans l'entrepôt --- #
# Crée un fichier texte du positionnement


def pos_alea(largeur, longueur):
    # nb_ref = longeur * largeur
    position = np.zeros((longueur, largeur))

    refs = [k for k in range(longeur * largeur)]
    rd.shuffle(refs)

    for i in range(longueur):
        for j in range(largeur):
            position[i,j] = refs[i * largeur + j]

    return position


def store_position(Position, file_name):
    with open(file_name, 'w') as f:
        for ligne in Position:
            string_row = ""
            for ref in ligne:
                ref = int(ref)
                string_row += str(ref) + " "
            string_row += "\n"
            f.write(string_row)


def alea(largeur, longueur):
    positionnement = pos_alea(largeur, longueur)
    store_position(positionnement, "pos_alea.txt")
    return positionnement
