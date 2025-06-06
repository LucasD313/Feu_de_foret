from feu_foret.simulateur import Simulateur

def main():
    largeur = 10
    hauteur = 10
    pourcentage_arbres = 0.6
    point_depart = (5, 5)

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