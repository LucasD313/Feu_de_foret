import os
import tempfile
from feu_foret.simulateur import Simulateur

def test_propagation_du_feu_complete():
    """Test de propagation du feu dans toutes les directions depuis le centre."""
    sim = Simulateur(3, 3, 0)
    sim.carte = [
        ['.', 'A', '.'],
        ['A', 'A', 'A'],
        ['.', 'A', '.'],
    ]
    sim.propager_feu(1, 1)  # centre

    attendu = [
        ['.', 'B', '.'],
        ['B', 'B', 'B'],
        ['.', 'B', '.'],
    ]
    assert sim.carte == attendu, f"Carte après propagation incorrecte : {sim.carte}"
    assert sim.compter_cases_brulees() == 5

def test_propagation_pas_sur_arbre():
    """La propagation ne commence pas sur une case qui n'est pas un arbre."""
    sim = Simulateur(2, 2, 0)
    sim.carte = [
        ['.', 'E'],
        ['X', 'B']
    ]
    sim.propager_feu(0, 0)
    assert sim.carte == [
        ['.', 'E'],
        ['X', 'B']
    ], "La propagation ne devrait pas modifier la carte"

def test_trouver_meilleur_deboisement_minimise_brule():
    """Teste que le meilleur déboisement réduit le nombre de cases brûlées."""
    sim = Simulateur(3, 3, 0)
    sim.carte = [
        ['A', 'A', 'A'],
        ['A', 'A', 'A'],
        ['A', 'A', 'A'],
    ]
    meilleur, brulees = sim.trouver_meilleur_deboisement(1, 1)
    assert isinstance(meilleur, tuple)
    assert brulees < 9, "Déboisement devrait réduire le nombre de brûlés"

def test_compter_cases_brulees_correctement():
    sim = Simulateur(3, 3, 0)
    sim.carte = [
        ['B', 'A', 'B'],
        ['A', 'B', 'A'],
        ['B', '.', 'B'],
    ]
    assert sim.compter_cases_brulees() == 5

def test_export_html_contenu_et_elements():
    sim = Simulateur(2, 2, 0)
    sim.carte = [
        ['A', 'E'],
        ['B', 'X']
    ]
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        chemin = tmp.name
    try:
        sim.exporter_html(
            chemin_fichier=chemin,
            point_depart=(0, 0),
            nb_brulees=1,
            arbres_coupes=[(1, 1)],
            nb_brulees_avant=3
        )

        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()

        # Vérifie les chemins d'images spécifiques
        assert "../Assets/arbre.png" in contenu
        assert "../Assets/eau.png" in contenu
        assert "../Assets/feu.png" in contenu
        assert "../Assets/sol.png" in contenu
        assert "../Assets/terrain.png" in contenu

        # Vérifie la présence du résumé
        assert "Départ du feu" in contenu
        assert "Après déboisement" in contenu
        assert "Avant déboisement" in contenu
        assert "Arbres déboisés" in contenu

    finally:
        os.remove(chemin)

def test_export_html_fonctionne_meme_sans_resume():
    sim = Simulateur(1, 1, 0)
    sim.carte = [['A']]
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        chemin = tmp.name
    try:
        sim.exporter_html(chemin_fichier=chemin)
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
        assert "<table>" in contenu
    finally:
        os.remove(chemin)
