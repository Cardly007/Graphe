import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import community  
import community.community_louvain as community_louvain  # Algorithme de Louvain
import numpy as np 


file_path = "reciprocal_relation_sample.csv"
df = pd.read_csv(file_path)


node_counts = df["FromNodeId"].value_counts() + df["ToNodeId"].value_counts()
node_counts = node_counts.fillna(0).astype(int) 


node_counts.sort_values(ascending=False)
high_degree_nodes = set(node_counts[node_counts > 150].index)

# Filtrer les relations où les deux nœuds ont un degré > 5
df_filtered = df[
    df["FromNodeId"].isin(high_degree_nodes) & df["ToNodeId"].isin(high_degree_nodes)
]

# Supprimer les relations avec eux-mêmes (self-loops)
df_filtered = df_filtered[df_filtered["FromNodeId"] != df_filtered["ToNodeId"]]

# Afficher le DataFrame filtré
df_filtered
# Création du graphe
G = nx.Graph()
for _, row in df_filtered.iterrows():
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
nx.draw(G, pos, with_labels=False, node_color=node_colors, edge_color='black',
        node_size=0.8, font_size=6, width=0.08)
plt.title("Graphe des liens d'amitié (coloration par communauté)")
plt.show()
