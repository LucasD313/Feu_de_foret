Tests et intégration continue
Etude de cas
Réalisez en Python avec une classe un simulateur de feux de forêts. La carte sera représentée par des cases représentant
chacune un terrain nu, des arbres ou un plan d’eau.
Le simulateur doit pouvoir construire aléatoirement une carte avec une certaine quantité d’arbres (à gérer sous la forme
d’un pourcentage).
Sachant que le feu progresse en passant par les cases avec des arbres (y compris en diagonale), créez une fonction
permettant de générer la carte montrant le résultat suite à un incendie déclenché à une position donnée.
Créer une méthode pour trouver la case d’arbre à déboiser la plus efficace pour réduire le plus possible (minimiser le
nombre de cases de forêt brulées) un incendie déclenché à une position donnée.
Votre simulateur disposera d’une méthode permettant de faire une exportation HTML pour visualiser le résultat. Aucun
affichage ne sera réalisé en mode console.
Vous travaillerez avec un dépôt Git qui sera déployé sur Github. Vous devrez penser à mettre en place les tests unitaires
et vous devrez planifier, avec Github Actions, un lancement de ces tests à chaque nouvel envoi. Vous devez travailler
dans différentes branches en organisant bien votre travail et en documentant bien vos différents commits.