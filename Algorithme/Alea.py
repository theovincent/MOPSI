import numpy.random as rd
import numpy as np

# --- Positionne les références de manière aléatoir dans l'entrepôt --- #
# Crée un fichier texte du positionnement

def alea(nb_rangees, longueur_rangees):
    # nb_ref = nb_rangees * longueur_rangees
    position = np.zeros((longueur_rangees, nb_rangees))

    refs = [k for k in range(nb_rangees * longueur_rangees)]
    rd.shuffle(refs)

    for i in range(longueur_rangees):
        for j in range(nb_rangees):
            position[i, j] = refs[i * nb_rangees + j]

    return position


# Inutile
def store_position(Position, file_name):
    with open(file_name, 'w') as f:
        for ligne in Position:
            string_row = ""
            for ref in ligne:
                ref = int(ref)
                string_row += str(ref) + " "
            string_row += "\n"
            f.write(string_row)


if __name__ == "__main__":
    nb_rangees = 10
    longueur_rangees = 3
    positionnement = alea(nb_rangees, longueur_rangees)
    print(positionnement)

    # store_position(positionnement, "Test_PosAlea.txt")
