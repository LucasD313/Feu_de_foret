import os
from feu_foret.simulateur import Simulateur

def test_propagation_du_feu():
    sim = Simulateur(3, 3, 0)
    sim.carte = [
        ['.', 'A', '.'],
        ['A', 'A', 'A'],
        ['.', 'A', '.'],
    ]
    sim.propager_feu(1, 1) #ici on doit faire en sorte que l'utilisateur puisse rentrer ce qu'il veut

    nb_arbres_restants = sum(row.count('A') for row in sim.carte)
    assert nb_arbres_restants == 0, f"Des arbres n'ont pas brûlé : {nb_arbres_restants} restants"
    assert sim.carte[1][1] == 'B'  # Le point de départ

def test_trouver_meilleur_deboisement():
    sim = Simulateur(3, 3, 0)
    sim.carte = [
        ['.', 'A', '.'],
        ['A', 'A', 'A'],
        ['.', 'A', '.'],
    ]
    meilleur = sim.trouver_meilleur_deboisement(1, 1)
    assert isinstance(meilleur, tuple)
    x, y = meilleur
    assert 0 <= x < sim.largeur and 0 <= y < sim.hauteur
    assert sim.carte[y][x] == 'A'

def test_compter_cases_brulees():
    sim = Simulateur(3, 3, 0)
    sim.carte = [
        ['B', 'A', 'B'],
        ['A', 'B', 'A'],
        ['B', '.', 'B'],
    ]
    assert sim.compter_cases_brulees() == 5

def test_export_html():
    sim = Simulateur(2, 3, 0)
    sim.carte = [
        ['A', '.'],
        ['E', 'B'],
        ['X', '.'],
    ]
    chemin_fichier = "test_carte.html"
    sim.exporter_html(chemin_fichier)

    assert os.path.exists(chemin_fichier)

    with open(chemin_fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Vérifie que toutes les couleurs attendues sont bien exportées
    assert "<table>" in contenu
    assert "#228B22" in contenu  # arbre
    assert "#FFD700" in contenu  # arbre coupé
    assert "#8B0000" in contenu  # brûlé
    assert "#c2b280" in contenu  # terrain vide
    assert "#1E90FF" in contenu  # eau

    os.remove(chemin_fichier)


