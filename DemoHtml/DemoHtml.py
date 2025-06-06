from feu_foret.simulateur import Simulateur

def main():
    largeur = 10
    hauteur = 10
    pourcentage_arbres = 0.6
    point_depart = (5, 5)

    # Étape 1 : Génération de la carte initiale
    sim = Simulateur(largeur, hauteur, pourcentage_arbres)
    sim.exporter_html("1_carte_originale.html")

if __name__ == "__main__":
    main()