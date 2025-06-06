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

if __name__ == "__main__":
    main()