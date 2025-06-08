import random
import copy

class Simulateur:
    VIDE = '.'
    ARBRE = 'A'
    EAU = 'E'
    FEU = 'F'
    BRULE = 'B'
    COUPE = 'X'
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
            copie[j][i] = self.VIDE  # Simule le déboisement
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
            return None, float('inf')  # Important : brulees_actuelles > float('inf') sera toujours faux

    def compter_cases_brulees(self):
        return sum(row.count(self.BRULE) for row in self.carte)

    def exporter_html(self, nom_fichier="carte.html", point_depart=None, nb_brulees=None, arbres_coupes=None,
                      nb_brulees_avant=None):
        couleurs = {
            self.VIDE: "#c2b280",  # beige
            self.ARBRE: "#228B22",  # vert
            self.EAU: "#1E90FF",  # bleu
            self.BRULE: "#8B0000",  # rouge foncé
            self.COUPE: "#FFD700",  # or
            self.DEPART_FEU: "#FFA500"  # orange
        }

        html = """
        <html><head>
        <meta charset="utf-8">
        <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 40px 10px;
            display: block;
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
            text-align: center;
        }
        table {
            border-collapse: collapse;
            margin: 0 auto 25px auto;
        }
        td {
            width: 20px;
            height: 20px;
            border: 1px solid #ccc;
        }
        h3 {
            color: #222;
            font-size: 18px;
            margin: 20px 0 10px 0;
        }
        ul {
            padding-left: 0;
            list-style-type: none;
            margin: 0;
        }
        li {
            margin: 5px 0;
            font-size: 15px;
        }
    
        @media (max-height: 600px), (max-width: 600px) {
            .container {
                padding: 15px;
            }
            td {
                width: 16px;
                height: 16px;
            }
            h3 {
                font-size: 16px;
            }
            li {
                font-size: 13px;
            }
        }
        </style>
        </head><body><div class="container">
        <table>
        """

        for ligne in self.carte:
            html += "<tr>"
            for case in ligne:
                couleur = couleurs.get(case, "#000000")
                html += f'<td style="background-color:{couleur}"></td>'
            html += "</tr>"
        html += "</table>"

        html += "<h3> Résumé de la simulation</h3><ul>"
        if point_depart:
            html += f"<li> Départ du feu : ({point_depart[0]}, {point_depart[1]})</li>"
        if nb_brulees_avant is not None:
            html += f"<li> Avant déboisement : {nb_brulees_avant} cases brûlées</li>"
        if nb_brulees is not None:
            html += f"<li> Après déboisement : {nb_brulees} cases brûlées</li>"
        if arbres_coupes is not None:
            html += f"<li> Arbres coupés : {arbres_coupes}</li>"
        html += "</ul></div></body></html>"

        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(html)




