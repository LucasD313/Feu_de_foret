import random
import copy

class Simulateur:
    VIDE = '.'
    ARBRE = 'A'
    EAU = 'E'
    FEU = 'F'
    BRULE = 'B'
    DEBOISE = 'X'
    DEPART_FEU = 'D'

    def __init__(self, largeur, hauteur, pourcentage_arbres):
        self.largeur = largeur
        self.hauteur = hauteur
        self.pourcentage_arbres = pourcentage_arbres
        self.carte = self.generer_carte()

    def generer_carte(self):
        carte = []
        for y in range(self.hauteur):
            ligne = []
            for x in range(self.largeur):
                r = random.random()
                if r < self.pourcentage_arbres:
                    ligne.append(self.ARBRE)
                else:
                    ligne.append(self.VIDE)
            carte.append(ligne)
        return carte

    def propager_feu(self, x, y):
        if self.carte[y][x] != self.ARBRE:
            return

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1),  (1, 0), (1, 1)]

        def feu_recursive(x, y):
            if not (0 <= x < self.largeur and 0 <= y < self.hauteur):
                return
            if self.carte[y][x] != self.ARBRE:
                return
            self.carte[y][x] = self.BRULE
            for dx, dy in directions:
                feu_recursive(x + dx, y + dy)

        feu_recursive(x, y)

    def trouver_meilleur_deboisement(self, x, y):
        arbres = [(i, j) for j in range(self.hauteur)
                  for i in range(self.largeur)
                  if self.carte[j][i] == self.ARBRE]

        meilleur = None
        min_brulure = None

        for i, j in arbres:
            copie = copy.deepcopy(self.carte)
            copie[j][i] = self.VIDE  # simulate tree removal
            sim_temp = Simulateur(self.largeur, self.hauteur, self.pourcentage_arbres)
            sim_temp.carte = [
                [self.ARBRE if cell == self.DEPART_FEU else cell for cell in row]
                for row in copie
            ]
            sim_temp.propager_feu(x, y)
            brulees = sim_temp.compter_cases_brulees()

            if min_brulure is None or brulees < min_brulure:
                min_brulure = brulees
                meilleur = (i, j)

        if meilleur is not None:
            return meilleur, min_brulure
        else:
            return None, float('inf')

    def compter_cases_brulees(self):
        return sum(row.count(self.BRULE) for row in self.carte)

    def exporter_html(self, nom_fichier="carte.html", point_depart=None,
                      nb_brulees=None, arbres_coupes=None, nb_brulees_avant=None):

        images = {
            self.VIDE: "../Assets/terrain.png",
            self.ARBRE: "../Assets/arbre.png",
            self.EAU: "../Assets/eau.png",
            self.BRULE: "../Assets/feu.png",
            self.DEBOISE: "../Assets/sol.png",
            self.DEPART_FEU: "../Assets/feu.png"
        }

        html = """
        <html><head>
        <meta charset="UTF-8">
        <title>Simulation de feu de forêt</title>
        <style>
            body {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', sans-serif;
                margin: 0;
                padding: 40px 10px;
                text-align: center;
            }
            .container {
                background: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                display: inline-block;
                padding: 25px 30px;
                max-width: 90vw;
            }
            table {
                border-collapse: collapse;
                margin: 0 auto 25px auto;
            }
            td {
                width: 20px;
                height: 20px;
                padding: 0;
                border: 1px solid #ccc;
            }
            td img {
                display: block;
                width: 20px;
                height: 20px;
            }
            h3 {
                font-size: 20px;
                margin-bottom: 10px;
            }
            li {
                margin: 6px 0;
                font-size: 15px;
                list-style: none;
            }
            .resume ul {
                padding: 0;
            }
            .legend {
                margin-top: 20px;
            }
            .legend div {
                display: inline-block;
                margin: 0 15px;
                text-align: center;
            }
            .legend img {
                width: 24px;
                height: 24px;
            }
            .legend small {
                display: block;
                margin-top: 5px;
                font-size: 13px;
                color: #333;
            }
        </style>
        </head><body><div class="container">
        <table>
        """

        for ligne in self.carte:
            html += "<tr>"
            for case in ligne:
                image = images.get(case, "../Assets/terrain.png")  # valeur par défaut sécurisée
                html += f'<td><img src="{image}" alt="{case}"></td>'
            html += "</tr>"

        html += "</table>"

        # Résumé de la simulation
        html += "<div class='resume'>"
        html += "<h3> Résumé de la simulation</h3><ul>"
        if point_depart:
            html += f"<li> Départ du feu : ({point_depart[0]}, {point_depart[1]})</li>"
        if nb_brulees_avant is not None:
            html += f"<li> Avant déboisement : {nb_brulees_avant} cases brûlées</li>"
        if nb_brulees is not None:
            html += f"<li> Après déboisement : {nb_brulees} cases brûlées</li>"
        if arbres_coupes is not None:
            html += f"<li> Arbres déboisés : {arbres_coupes}</li>"
        html += "</ul></div>"

        # Légende
        html += """
        <hr style="margin: 25px auto; width: 60%; border: none; border-top: 1px solid #ccc;">
        <div class="legend">
            <div><img src="../Assets/arbre.png"><small>Arbre</small></div>
            <div><img src="../Assets/eau.png"><small>Eau</small></div>
            <div><img src="../Assets/feu.png"><small>Feu / Départ</small></div>
            <div><img src="../Assets/terrain.png"><small>Terrain</small></div>
            <div><img src="../Assets/sol.png"><small>Sol déboisé</small></div>
        </div>
        """

        html += "</div></body></html>"

        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(html)
