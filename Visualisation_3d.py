import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import community
import community.community_louvain as community_louvain
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # Importer le module 3D

file_path = "reciprocal_relation_sample.csv"
df = pd.read_csv(file_path)

# Calcul du degré des nœuds
node_counts = df["FromNodeId"].value_counts() + df["ToNodeId"].value_counts()
node_counts = node_counts.fillna(0).astype(int)  # Remplacer les NaN
node_counts.sort_values(ascending=False)

# Filtrer les nœuds de degré élevé
high_degree_nodes = set(node_counts[node_counts > 600].index)

# Filtrer les relations où les deux nœuds ont un degré élevé
df_filtered = df[
    df["FromNodeId"].isin(high_degree_nodes) & df["ToNodeId"].isin(high_degree_nodes)
]

# Supprimer les relations avec eux-mêmes (self-loops)
df_filtered = df_filtered[df_filtered["FromNodeId"] != df_filtered["ToNodeId"]]

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

# Positionnement des nœuds en 3D
pos = nx.spring_layout(G, dim=3, seed=42)  # Utilisation de 3 dimensions

# Visualisation en 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Dessiner les arêtes
for edge in G.edges():
    x_vals = [pos[edge[0]][0], pos[edge[1]][0]]
    y_vals = [pos[edge[0]][1], pos[edge[1]][1]]
    z_vals = [pos[edge[0]][2], pos[edge[1]][2]]
    ax.plot(x_vals, y_vals, z_vals, color='black', alpha=0.5)

# Dessiner les nœuds
x_vals = [pos[node][0] for node in G.nodes()]
y_vals = [pos[node][1] for node in G.nodes()]
z_vals = [pos[node][2] for node in G.nodes()]

# Scatter plot pour les nœuds avec couleur
ax.scatter(x_vals, y_vals, z_vals, c=node_colors, s=50, marker='o')


# Titre et labels des axes
ax.set_title("Graphe des liens d'amitié (3D, coloration par communauté)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()
