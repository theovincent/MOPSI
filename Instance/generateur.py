import numpy as np
import numpy.random as rd
from pulp import LpVariable, LpProblem, LpMinimize

# ---- Ce programme permet de générer une loi de commande de taille 2 ----
# Pour cela, nous prenons une matrice de Jacquard aléatoire et
# nous résolvons un problème linéaire Ax = B avec x le vecteur
# donnant la loi des commandes.


# -- Paramètres --
nb_ref = 2 # Il s'agit du nombre de références différentes


# -- Commençons par obtenir les matrices A et B --
# Voici un exemple pour nb_ref = 2
# Mat Aj  (1, 1)    (1, 2)   (2, 1)  (2, 2)
#(1, 1)  J[i, j]   J[i, j]  J[i, j]    0
#(1, 2)  J[i, j]   J[i, j]     0    J[i, j]
#(2, 1)  J[i, j]      0     J[i, j] J[i, j]
#(2, 2)     0      J[i, j ] J[i, j] J[i, j]

# Mat C  (1, 1)    (1, 2)   (2, 1)  (2, 2)
#(1, 1)    1         0         0       0
#(2, 2)    0         0         0       1

# Variable fixes
R = nb_ref * nb_ref

L1 = np.ones((1, R))

C = np.zeros((nb_ref, R))
for k in range(R):
    i = k % nb_ref
    j = k // nb_ref
    if i == j:
        C[i, k] = 1

B = np.zeros(R + nb_ref + 1)
B[-1] = 1


# Renvoie la liste des probabilité des commandes
def resout():
    # Initialisation de J
    J = rd.random((R, R))


    for i in range(R):
        sum_ligne = sum(J[i][:])
        for j in range(R):
            # sum_ligne / 7 est arbitraire, il sert à équilibrer la matrice de Jacquard
            J[i][j] /= sum_ligne + sum_ligne / 7
        sum_ligne = sum(J[i][:])
        # (1 - sum_ligne) / 3 est arbitraire, il sert à se que la somme des coefficients sur une ligne soit inférieur à 1
        J[i][-1] = (1 - sum_ligne) / 3
        
    for i in range(R):
        j = 0
        while j < i:
            J[i, j] = J[j, i]
            j += 1
    print(J)

    # Calculons A
    Aj = np.zeros((R, R))
    for m in range(R):
        i_ord = m % nb_ref
        j_ord = m // nb_ref
        for n in range(R):
            i_abs = n % nb_ref
            j_abs = n // nb_ref
            if i_ord == i_abs:
                Aj[m, n] = J[i_ord, j_ord]
            elif j_ord == j_abs:
                Aj[m, n] = J[i_ord, j_ord]
            else:
                pass

    A = np.concatenate((Aj - np.eye(R), C, L1), axis=0)
    
    # -- Résolvons le problème linéaire Ax = B
    # Definissons les variables :
    Ref = [0] * nb_ref
    for i in range(nb_ref):
        Ref[i] = "ref{}".format(i)
    
    RefProb = ["({}, {})".format(Refi, Refj) for Refi in Ref for Refj in Ref]
    
    VarRef = LpVariable.dicts("Reference", RefProb, lowBound=0., upBound=1., cat='float')
    
    # Définissons le problème
    prob = LpProblem("Ax_B", LpMinimize)
    
    # Définissons la fonction de coût
    prob += 2 #sum([VarRef[ref] for ref in RefProb])
    
    # Définissons les contraintes
    for i in range(R + nb_ref + 1):
        prob += sum([A[i, j] * VarRef[RefProb[j]] for j in range(len(RefProb))]) == B[i]
    
    # Résolvons le problème
    prob.solve()
    
    # Enregistrons les résultats
    Prob = np.zeros((nb_ref, nb_ref))
    i = 0
    j = 0
    for v in prob.variables():
        if v.name[-1] == ")":
            Prob[i, j] = v.varValue
        j += 1
        if j== nb_ref:
            j = 0
            i += 1

    return Prob


def diagNulle(Mat):
    n = len(Mat)
    
    for i in range(n):
        if abs(Mat[i, i]) > 0.001:
            return False
    
    return True


def verify(Prob):
    nb_zero = 0
    for i in range(nb_ref):
        for j in range(nb_ref):
            proba = Prob[i, j]
            if proba == 0:
                nb_zero += 1
            if (proba < 0) or (proba > 1) or (nb_zero > nb_ref) or not diagNulle(Prob):
                return False
    return True


def store_proba(Prob,file_name):
    with open(file_name,'w') as f:
        for i in range(nb_ref):
            string_row = ""
            for j in range(nb_ref):
                string_row += str(round(Prob[i, j], 3)) + " "
            string_row += "\n"
            f.write(string_row)


if __name__ == "__main__":

    Prob = resout()
    """
    # Nous nous assurons que les probabilités soient comprises entre 0 et 1 et qu'il n'y a pas trop de zéro (nb_zero < nb_ref)
    essai = 0
    while not verify(Prob):
        essai += 1
        Prob = resout()
    """
    print(Prob)
    store_proba(Prob, "test_historique.txt")
    sum_ligne = [sum(Prob[i, :]) for i in range(nb_ref)]
    print(sum(sum_ligne))