# Analyse et Visualisation de Graphes

Ce projet contient plusieurs scripts Python pour analyser et visualiser des graphes basés sur des relations entre nœuds. Les scripts utilisent des bibliothèques comme `pandas`, `networkx`, `matplotlib` et l'algorithme de Louvain pour détecter les communautés.

## Structure des fichiers

### 1. **relation_entre_communaute.py**
- **Description** : Ce script analyse les relations entre communautés dans un graphe. Il détecte les communautés à l'aide de l'algorithme de Louvain, sélectionne des paires de communautés, et visualise leurs sous-graphes.
- **Sortie** : Génère des visualisations des sous-graphes et les enregistre au format `.gexf`.

---

### 2. **Visualisation_3d.py**
- **Description** : Ce script visualise un graphe en 3D avec une coloration basée sur les communautés détectées. Il utilise `mpl_toolkits.mplot3d` pour afficher les graphes en trois dimensions.
- **Sortie** : Affiche une visualisation 3D des graphes avec des couleurs distinctes pour chaque communauté.

---

### 3. **intersection.py**
- **Description** : Ce script analyse les intersections entre deux communautés dans un graphe. Il sélectionne des nœuds appartenant à deux communautés et visualise les sous-graphes correspondants.
- **Sortie** : Génère des visualisations des sous-graphes avec des nœuds d'intersection mis en évidence.

---

### 4. **voisin.py**
- **Description** : Ce script explore les voisins d'un nœud aléatoire dans le graphe. Il étend l'exploration pour inclure les voisins des voisins et visualise le sous-graphe résultant.
- **Sortie** : Affiche un sous-graphe centré sur un nœud aléatoire.

---

### 5. **degre.py**
- **Description** : Ce script analyse les nœuds ayant un degré élevé dans le graphe. Il filtre les relations pour ne garder que celles entre ces nœuds et visualise les communautés détectées.
- **Sortie** : Affiche un graphe avec une coloration par communauté.

---

### 6. **Random.py**
- **Description** : Ce script extrait un sous-graphe aléatoire à partir d'un graphe plus grand. Il est utile pour visualiser une partie du graphe sans surcharger la mémoire.
- **Sortie** : Affiche un sous-graphe aléatoire.

---

### 7. **reciproque.py**
- **Description** : Ce script filtre les relations pour ne garder que celles entre les nœuds les plus connectés. Il génère un fichier CSV contenant un sous-ensemble des relations.
- **Sortie** : Crée un fichier `reciprocal_relation_sample.csv`.

---

### 8. **transfrmcsv.py**
- **Description** : Ce script convertit un fichier texte contenant des relations en un fichier CSV. Il ignore les lignes de commentaires et formate les données pour une utilisation ultérieure.
- **Sortie** : Crée un fichier CSV à partir d'un fichier texte brut.

---

## Dépendances

Pour exécuter ces scripts, installez les bibliothèques suivantes :

```plaintext
pandas
networkx
matplotlib
numpy
python-louvain