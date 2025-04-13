import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import community.community_louvain as community_louvain
from itertools import combinations

# === Étape 1 : Chargement des données ===
file_path = "reciprocal_relation_sample.csv"
df = pd.read_csv(file_path)

# === Étape 2 : Calcul du degré total ===
node_counts = df["FromNodeId"].value_counts() + df["ToNodeId"].value_counts()
node_counts = node_counts.fillna(0).astype(int)

# === Étape 3 : Filtrage des nœuds avec fort degré ===
high_degree_nodes = set(node_counts[node_counts > 30].index)
df_filtered = df[
    df["FromNodeId"].isin(high_degree_nodes) & df["ToNodeId"].isin(high_degree_nodes)
]
df_filtered = df_filtered[df_filtered["FromNodeId"] != df_filtered["ToNodeId"]]

# === Étape 4 : Construction du graphe ===
G = nx.Graph()
for _, row in df_filtered.iterrows():
    G.add_edge(row['FromNodeId'], row['ToNodeId'])

# === Étape 5 : Détection des communautés ===
partition = community_louvain.best_partition(G)

# === Étape 6 : Mapping des couleurs des communautés ===
unique_communities = sorted(set(partition.values()))
colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_communities)))
community_color_map = {comm: colors[i] for i, comm in enumerate(unique_communities)}

# === Étape 7 : Identification des arêtes entre communautés ===
inter_edges = []
for u, v in G.edges():
    cu = partition[u]
    cv = partition[v]
    if cu != cv:
        inter_edges.append((u, v, cu, cv))

# === Étape 8 : Visualisation des connexions clés ===
pairs = set((min(c1, c2), max(c1, c2)) for _, _, c1, c2 in inter_edges)

for comm1, comm2 in pairs:
    connector_nodes = set()
    edges_between = []

    for u, v, c1, c2 in inter_edges:
        if set([c1, c2]) == set([comm1, comm2]):
            connector_nodes.update([u, v])
            edges_between.append((u, v))

    # Ajouter leurs voisins directs
    neighbor_nodes = set()
    for node in connector_nodes:
        neighbor_nodes.update(G.neighbors(node))

    # Rassembler tous les nœuds utiles
    total_nodes = connector_nodes.union(neighbor_nodes)
    subG = G.subgraph(total_nodes)

    # Préparer la position et les couleurs
    pos = nx.spring_layout(subG, seed=42)
    node_colors = [community_color_map[partition[node]] for node in subG.nodes()]
    edge_colors = ['gray' if (u, v) not in edges_between and (v, u) not in edges_between else 'black'
                   for u, v in subG.edges()]

    # Dessiner
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(subG, pos, node_color=node_colors, node_size=100)
    nx.draw_networkx_edges(subG, pos, edge_color=edge_colors, width=1.5)
    plt.title(f"Connexions clés entre les communautés {comm1} et {comm2}")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"liaison_{comm1}_{comm2}.png", dpi=300)
    plt.show()
