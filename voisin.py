import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import community  
import community.community_louvain as community_louvain  # Algorithme de Louvain
import numpy as np 

file_path = "reciprocal_relation_sample.csv"
df = pd.read_csv(file_path, sep=",", comment='#', header=None, names=["FromNodeId", "ToNodeId"])

start_node = df["FromNodeId"].sample(1).values[0]


# Récupération des arêtes où ce nœud apparaît
sample_df = df[(df["FromNodeId"] == start_node) | (df["ToNodeId"] == start_node)]

# Expansion pour inclure les voisins des voisins (augmenter la connectivité)
for _ in range(3):  # Profondeur d'exploration
    neighbor_nodes = sample_df["ToNodeId"].unique()
    new_links = df[df["FromNodeId"].isin(neighbor_nodes)]
    sample_df = pd.concat([sample_df, new_links]).drop_duplicates()

# Limiter à 1000 lignes
sample_df = sample_df.head(300000)

print(sample_df)


# Création du graphe
G = nx.Graph()
for _, row in sample_df.iterrows():
    G.add_edge(row['FromNodeId'], row['ToNodeId'])

# Détection des communautés avec Louvain
partition = community_louvain.best_partition(G)

# Attribution des couleurs aux communautés
communities = list(set(partition.values()))
colors = plt.cm.rainbow(np.linspace(0, 1, len(communities)))  # Génération de couleurs distinctes
node_colors = [colors[communities.index(partition[node])] for node in G.nodes()]

# Positionnement des nœuds
pos = nx.spring_layout(G, seed=42)

# Affichage du graphe avec coloration par communauté
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=False, node_color=node_colors, edge_color='gray',
        node_size=1, font_size=6, width=0.050)
plt.title("Graphe des liens d'amitié (coloration par communauté)")
plt.show()