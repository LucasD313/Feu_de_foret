import os
from feu_foret.simulateur import Simulateur

def test_propagation_du_feu():
    sim = Simulateur(3, 3, 0)
    sim.carte = [
        ['.', 'A', '.'],
        ['A', 'A', 'A'],
        ['.', 'A', '.'],
    ]
    sim.propager_feu(1, 1)

    # Toutes les cases A doivent être brûlées
    for y in range(3):
        for x in range(3):
            case = sim.carte[y][x]
            if case == 'A':
                assert False, f"Case ({x},{y}) aurait dû brûler"
    assert sim.carte[1][1] == 'B'  # Le point de départ

def test_trouver_meilleur_deboisement():
    sim = Simulateur(3, 3, 0)
    sim.carte = [
        ['.', 'A', '.'],
        ['A', 'A', 'A'],
        ['.', 'A', '.'],
    ]
    meilleur = sim.trouver_meilleur_deboisement(1, 1)

    # Vérifie que la position est bien un arbre dans la configuration d'origine
    assert isinstance(meilleur, tuple)
    x, y = meilleur
    assert 0 <= x < sim.largeur and 0 <= y < sim.hauteur
    assert sim.carte[y][x] == 'A'

def test_export_html():
    sim = Simulateur(2, 2, 0)
    sim.carte = [
        ['A', '.'],
        ['E', 'B'],
    ]
    chemin_fichier = "test_carte.html"
    sim.exporter_html(chemin_fichier)

    assert os.path.exists(chemin_fichier)

    with open(chemin_fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    assert "<table>" in contenu
    assert "#228B22" in contenu  # vert = arbre
    assert "#8B0000" in contenu  # rouge foncé = brûlé

    os.remove(chemin_fichier)  # Nettoyage
