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

        min_brulure = float('inf')
        meilleur = None

        for i, j in arbres:
            copie = copy.deepcopy(self.carte)
            copie[j][i] = self.VIDE
            sim_temp = Simulateur(self.largeur, self.hauteur, self.pourcentage_arbres)
            sim_temp.carte = copie
            sim_temp.propager_feu(x, y)

            brulees = sum(row.count(self.BRULE) for row in sim_temp.carte)
            if brulees < min_brulure:
                min_brulure = brulees
                meilleur = (i, j)

        return meilleur

    def compter_cases_brulees(self):
        return sum(row.count(self.BRULE) for row in self.carte)

    def exporter_html(self, nom_fichier="carte.html"):
        couleurs = {
            self.VIDE: "#c2b280",    # beige
            self.ARBRE: "#228B22",   # vert
            self.EAU: "#1E90FF",     # bleu
            self.BRULE: "#8B0000",   # rouge foncé
            self.COUPE: "#FFD700",   # or (arbre coupé)
            self.DEPART_FEU: "#FFA500",  # orange pour le départ du feu

        }

        html = "<html><head><style>"
        html += "table {border-collapse: collapse;} td {width: 20px; height: 20px; border: 1px solid #ccc;}"
        html += "</style></head><body><table>"

        for ligne in self.carte:
            html += "<tr>"
            for case in ligne:
                couleur = couleurs.get(case, "#000000")
                html += f'<td style="background-color:{couleur}"></td>'
            html += "</tr>"

        html += "</table></body></html>"

        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(html)
