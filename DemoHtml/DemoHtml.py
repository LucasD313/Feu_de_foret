from feu_foret.simulateur import Simulateur

def demander_entier(message, min_val=0, max_val=None):
    while True:
        try:
            valeur = int(input(message))
            if valeur < min_val or (max_val is not None and valeur > max_val):
                print(f"Veuillez entrer une valeur entre {min_val} et {max_val}.")
            else:
                return valeur
        except ValueError:
            print("Veuillez entrer un entier valide.")

def demander_float(message, min_val=0.0, max_val=1.0):
    while True:
        try:
            valeur = float(input(message))
            if valeur < min_val or valeur > max_val:
                print(f"Veuillez entrer une valeur entre {min_val} et {max_val}.")
            else:
                return valeur
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def main():
    # largeur = 10
    # hauteur = 10
    # pourcentage_arbres = 0.6
    # point_depart = (5, 5)

    print(" Simulation de feu de forêt")

    largeur = demander_entier("Largeur de la carte (ex: 10) : ", min_val=1)
    hauteur = demander_entier("Hauteur de la carte (ex: 10) : ", min_val=1)
    pourcentage_arbres = demander_float("Pourcentage d'arbres (0.0 à 1.0, ex: 0.6) : ")

    max_x = largeur - 1
    max_y = hauteur - 1
    x = demander_entier(f"Position X du départ du feu (0 à {max_x}) : ", 0, max_x)
    y = demander_entier(f"Position Y du départ du feu (0 à {max_y}) : ", 0, max_y)
    point_depart = (x, y)

    # Étape 1 : Génération de la carte initiale
    sim = Simulateur(largeur, hauteur, pourcentage_arbres)
    sim.exporter_html("1_carte_originale.html")

    # Étape 2 : Simulation du feu sans déboisement
    sim_sans = Simulateur(largeur, hauteur, pourcentage_arbres)
    sim_sans.carte = [row[:] for row in sim.carte]
    sim_sans.propager_feu(*point_depart)
    sim_sans.exporter_html("2_feu_sans_deboisement.html")
    brulees_sans = sim_sans.compter_cases_brulees()

    # Étape 3 : Recherche du meilleur arbre à déboiser
    meilleur = sim.trouver_meilleur_deboisement(*point_depart)
    if meilleur:
        x, y = meilleur
        sim.carte[y][x] = Simulateur.COUPE  # Marquer l'arbre coupé
        print(f" Meilleur arbre à couper : {meilleur}")
    else:
        print(" Aucun arbre à couper trouvé.")

    # Étape 4 : Simulation du feu après déboisement
    sim_avec = Simulateur(largeur, hauteur, pourcentage_arbres)
    sim_avec.carte = [row[:] for row in sim.carte]
    sim_avec.propager_feu(*point_depart)
    sim_avec.exporter_html("3_feu_avec_deboisement.html")
    brulees_avec = sim_avec.compter_cases_brulees()

if __name__ == "__main__":
    main()