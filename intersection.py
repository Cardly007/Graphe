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

# Créer et afficher les sous-graphes avec une sélection de nœuds
for idx, (comm1, comm2) in enumerate(selected_pairs, 1):
    nodes1 = community_nodes[comm1]
    nodes2 = community_nodes[comm2]
    
    # Sélectionner plus de nœuds pour chaque communauté (par exemple, 30 nœuds par communauté)
    sample_size = min(30, len(nodes1), len(nodes2))  # 30 nœuds par groupe maximum
    selected_nodes1 = np.random.choice(nodes1, sample_size, replace=False).tolist()
    selected_nodes2 = np.random.choice(nodes2, sample_size, replace=False).tolist()
    
    # Créer le sous-ensemble de nœuds qui sera affiché
    selected_nodes = set(selected_nodes1 + selected_nodes2)

    # Trouver les nœuds qui sont dans l'intersection des deux communautés
    intersection_nodes = set(selected_nodes1).intersection(selected_nodes2)

    # Filtrer les arêtes qui relient ces communautés
    edges_between = [(u, v) for u, v in G.edges() if u in selected_nodes and v in selected_nodes]

    # Créer le sous-graphe
    subgraph = nx.Graph()
    subgraph.add_edges_from(edges_between)
    subgraph.add_nodes_from(selected_nodes)  # Ajouter explicitement les nœuds sélectionnés

    # Vérifier si le sous-graphe contient des nœuds
    if len(subgraph.nodes) == 0:
        print(f"⚠️ Pas de nœuds visibles pour les communautés {comm1} et {comm2}.")
        continue

    # Générer la disposition des nœuds
    pos = nx.spring_layout(subgraph, seed=42)

    plt.figure(figsize=(10, 8))

    # Définir les couleurs
    color1 = color_map(comm1 % 10)  
    color2 = color_map((comm2 + 1) % 10)  
    intersection_color = 'black'  # Couleur pour les nœuds d'intersection

    # Dessiner les nœuds de la première communauté
    nx.draw_networkx_nodes(subgraph, pos, nodelist=selected_nodes1, node_color=color1, 
                           label=f"Communauté {comm1}", node_size=150)

    # Dessiner les nœuds de la deuxième communauté
    nx.draw_networkx_nodes(subgraph, pos, nodelist=selected_nodes2, node_color=color2, 
                           label=f"Communauté {comm2}", node_size=150)

    # Dessiner l'intersection des deux communautés avec une couleur distincte
    nx.draw_networkx_nodes(subgraph, pos, nodelist=list(intersection_nodes), node_color=intersection_color, 
                           label="Intersection", node_size=200)

    # Dessiner les arêtes reliant les nœuds sélectionnés
    nx.draw_networkx_edges(subgraph, pos, edgelist=edges_between, edge_color="gray", alpha=0.7, width=2)

    # Ajouter les labels des nœuds pour mieux visualiser (si tu veux)
    nx.draw_networkx_labels(subgraph, pos, font_size=8, font_color="black", font_weight="bold")

    plt.title(f"Sous-graphe {idx} : Communautés {comm1} et {comm2} avec intersection")
    plt.legend()
    plt.show()

    # Enregistrer le sous-graphe
    filename = f"subgraph_{comm1}_{comm2}.gexf"
    nx.write_gexf(subgraph, filename)
    print(f"✅ Sous-graphe {idx} enregistré sous {filename}.")
