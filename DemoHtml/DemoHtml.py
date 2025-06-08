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

    # Nombre de déboisement possible
    nb_deboisements_max = demander_entier("Nombre maximum d'arbres à couper : ", min_val=0)

    # Étape 1 : Génération de la carte initiale
    sim = Simulateur(largeur, hauteur, pourcentage_arbres)
    sim.carte[y][x] = Simulateur.DEPART_FEU  # Marque le départ du feu
    sim.exporter_html("1_carte_originale.html", point_depart=point_depart)

    # Étape 2 : Simulation du feu sans déboisement
    sim_sans = Simulateur(largeur, hauteur, pourcentage_arbres)
    sim_sans.carte = [
        [Simulateur.ARBRE if cell == Simulateur.DEPART_FEU else cell for cell in row]
        for row in sim.carte
    ]
    sim_sans.propager_feu(*point_depart)
    brulees_actuelles = sim_sans.compter_cases_brulees()
    sim_sans.exporter_html("2_feu_sans_deboisement.html",
                           point_depart=point_depart,
                           nb_brulees=brulees_actuelles,
                           arbres_coupes=0)

    # Étape 3 : Recherche des meilleurs arbres à couper
    print("\n Déboisement intelligent en cours...")
    arbres_coupes = 0
    while arbres_coupes < nb_deboisements_max:
        meilleur, brulees_apres = sim.trouver_meilleur_deboisement(*point_depart)

        if meilleur is None:
            print(f" Aucun arbre à couper trouvé à l'itération {arbres_coupes + 1}.")
            break

        if brulees_apres < brulees_actuelles:
            mx, my = meilleur
            sim.carte[my][mx] = Simulateur.COUPE
            brulees_actuelles = brulees_apres
            arbres_coupes += 1
            print(f" Arbre #{arbres_coupes} coupé à : {meilleur} → {brulees_apres} cases brûlées")
        else:
            print(f" Arbre {meilleur} ignoré (aucune amélioration)")
            break

    # Étape 4 : Simulation du feu après déboisement
    sim_avec = Simulateur(largeur, hauteur, pourcentage_arbres)
    sim_avec.carte = [
        [Simulateur.ARBRE if cell == Simulateur.DEPART_FEU else cell for cell in row]
        for row in sim.carte
    ]
    sim_avec.propager_feu(*point_depart)
    brulees_final = sim_avec.compter_cases_brulees()
    sim_avec.exporter_html("3_feu_avec_deboisement.html",
                           point_depart=point_depart,
                           nb_brulees=brulees_final,
                           arbres_coupes=arbres_coupes,
                           nb_brulees_avant=brulees_actuelles)

    # Résumé
    print("\n✅ Simulation terminée !")
    print(f"🔥 Cases brûlées sans déboisement : {sim_sans.compter_cases_brulees()}")
    print(f"🪓 Cases brûlées avec {arbres_coupes} déboisement(s) : {brulees_final}")
    print("📄 Fichiers générés :")
    print(" - 1_carte_originale.html")
    print(" - 2_feu_sans_deboisement.html")
    print(" - 3_feu_avec_deboisement.html")

if __name__ == "__main__":
    main()