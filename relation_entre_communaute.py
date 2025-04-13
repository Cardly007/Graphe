import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community.community_louvain as community_louvain
import numpy as np

# Charger les données
file_path = "reciprocal_relation_sample.csv"
df = pd.read_csv(file_path)

# Filtrer les nœuds avec un degré élevé
node_counts = df["FromNodeId"].value_counts() + df["ToNodeId"].value_counts()
node_counts = node_counts.fillna(0).astype(int)

high_degree_nodes = set(node_counts[node_counts > 25].index)

# Filtrer les relations où les deux nœuds ont un degré élevé
df_filtered = df[
    df["FromNodeId"].isin(high_degree_nodes) & df["ToNodeId"].isin(high_degree_nodes)
]

# Supprimer les self-loops
df_filtered = df_filtered[df_filtered["FromNodeId"] != df_filtered["ToNodeId"]]

# Création du graphe
G = nx.Graph()
edges = list(zip(df_filtered["FromNodeId"], df_filtered["ToNodeId"]))
G.add_edges_from(edges)

# Détection des communautés avec Louvain
partition = community_louvain.best_partition(G)

# Trouver les communautés et leurs nœuds
communities = list(set(partition.values()))
community_nodes = {comm: [node for node, comm_id in partition.items() if comm_id == comm] for comm in communities}

# Sélectionner trois paires de communautés
selected_pairs = [(communities[i], communities[i+1]) for i in range(min(3, len(communities) - 1))]

# Générer une palette de couleurs avec Matplotlib
color_map = plt.colormaps["tab10"]

# Créer et afficher les sous-graphes avec toutes les connexions internes
for idx, (comm1, comm2) in enumerate(selected_pairs, 1):
    nodes1 = community_nodes[comm1]
    nodes2 = community_nodes[comm2]
    
    # Regrouper tous les nœuds des deux communautés
    all_nodes = set(nodes1 + nodes2)

    # Créer le sous-graphe contenant tous les nœuds des deux communautés et leurs liens internes
    subgraph = G.subgraph(all_nodes).copy()

    # Vérifier si le sous-graphe contient des nœuds
    if len(subgraph.nodes) == 0:
        print(f"⚠️ Pas de nœuds visibles pour les communautés {comm1} et {comm2}.")
        continue

    # Générer la disposition des nœuds
    pos = nx.spring_layout(subgraph, seed=42)

    # Vérifier quels nœuds sont dans `pos`
    nodes1_in_pos = [n for n in nodes1 if n in pos]
    nodes2_in_pos = [n for n in nodes2 if n in pos]

    plt.figure(figsize=(8, 6))

    # Définir les couleurs
    color1 = color_map(comm1 % 10)  
    color2 = color_map((comm2 + 1) % 10)  

    # Dessiner les nœuds de la première communauté
    nx.draw_networkx_nodes(subgraph, pos, nodelist=nodes1_in_pos, node_color=color1, 
                           label=f"Communauté {comm1}", node_size=100)

    # Dessiner les nœuds de la deuxième communauté
    nx.draw_networkx_nodes(subgraph, pos, nodelist=nodes2_in_pos, node_color=color2, 
                           label=f"Communauté {comm2}", node_size=100)

    # Dessiner toutes les arêtes du sous-graphe
    nx.draw_networkx_edges(subgraph, pos, edge_color="gray", alpha=0.5)

    plt.title(f"Sous-graphe {idx} : Communautés {comm1} et {comm2}")
    plt.legend()
    plt.show()

    # Enregistrer le sous-graphe
    filename = f"subgraph_{comm1}_{comm2}.gexf"
    nx.write_gexf(subgraph, filename)
    print(f"✅ Sous-graphe {idx} enregistré sous {filename}.")
