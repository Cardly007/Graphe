import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Chemin du fichier
# file_path = "soc-LiveJournal1.txt"
# file_path = "reciprocal_relations.txt"
# file_path = "subgraphRdm3.csv"
file_path = "reciprocal_relation_sample.csv"

# Lire le fichier tout en ignorant les lignes de commentaires
# data = pd.read_csv(file_path, sep="\t", comment='#', header=None, names=["FromNodeId", "ToNodeId"])
data = pd.read_csv(file_path, sep=",", comment='#', header=None, names=["FromNodeId", "ToNodeId"])

# Afficher un aperçu des données
print(data.head()) 

# nrows=1000000
# Créer un graphe orienté
G = nx.DiGraph()

# Ajouter les arêtes au graphe
G.add_edges_from(data.values)

G.remove_edges_from(nx.selfloop_edges(G))

# Afficher des informations sur le graphe
print("Nombre de nœuds :", G.number_of_nodes())
print("Nombre d’arêtes :", G.number_of_edges())

# Extraire un sous-graphe pour visualisation
# subgraph = G.subgraph(list(G.nodes)[:100])  # Par exemple, les 100 premiers nœuds
random_nodes = random.sample(list(G.nodes), 1300)  # 100 nœuds aléatoires
subgraph = G.subgraph(random_nodes)  # Sous-graphe de 100 nœuds

# Visualiser le sous-graphe
plt.figure(figsize=(12, 10))
nx.draw(subgraph, with_labels=True, node_size=1, font_size=8,width=0.050)
plt.title("Sous-graphe de 100 nœuds")
plt.show()
