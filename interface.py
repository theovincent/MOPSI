from alea import alea
from notre_algo import notre_algo
from evaluation import evalue
from generateur import generation_commande, extraction_commande


# --- Paramètres --- #
nb_rangees = 30
longueur_rangees = 10
nb_ref = nb_rangees * longueur_rangees
nom_instance_theo = "test"
# nom_instance_pia =
nom_instance = nom_instance_theo


# --- Historique des commandes --- #
print("Chargement de la commande...")
historique = generation_commande(nb_ref,  nom_instance)

print("L'historique des commandes est :")
print(historique)


# --- Calcul des emplacements par différentes méthodes --- #
print("Calcul des positionnements...")
# Partie calcul
positionnement_alea = alea(nb_rangees, longueur_rangees)
positionnement_notre_algo = notre_algo(positionnement_alea.copy(), 200, historique)

# Partie affichage
print("Le positionnement aléatoire est :")
print(positionnement_alea)
print("Notre positionnement est :")
print(positionnement_notre_algo)


# --- Evaluation des différents emplacements --- #
print("Evaluation des positionnement...")
alea = evalue(positionnement_alea, historique)
notre_algo = evalue(positionnement_notre_algo, historique)

# Affichage des résultats
print("Le résultat pour le positionnement aléaoire est de {}".format(alea))
print("Le résultat pour notre positionnement est de {}".format(notre_algo))


if __name__ == "__main__":
    pass
