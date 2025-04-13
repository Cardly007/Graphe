import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community.community_louvain as community_louvain
from sklearn.preprocessing import MinMaxScaler

# === Chargement ===
df = pd.read_csv("reciprocal_relation_sample.csv")

# === Calcul des connexions ===
node_counts = df["FromNodeId"].value_counts() + df["ToNodeId"].value_counts()
node_counts = node_counts.fillna(0).astype(int)

# === Filtrage des nœuds les plus actifs ===
core_nodes = set(node_counts[node_counts > 30].index)
df_filtered = df[
    df["FromNodeId"].isin(core_nodes) & df["ToNodeId"].isin(core_nodes)
]
df_filtered = df_filtered[df_filtered["FromNodeId"] != df_filtered["ToNodeId"]]

# === Graphe ===
G = nx.from_pandas_edgelist(df_filtered, "FromNodeId", "ToNodeId")
partition = community_louvain.best_partition(G)

# === Métriques ===
degree = dict(G.degree())
betweenness = nx.betweenness_centrality(G, k=300, normalized=True, seed=42)

df_nodes = pd.DataFrame({
    "Node": list(G.nodes),
    "Degree": [degree[n] for n in G.nodes],
    "Betweenness": [betweenness[n] for n in G.nodes],
    "Community": [partition[n] for n in G.nodes]
})

# === Normalisation ===
scaler = MinMaxScaler()
df_nodes[["NormDegree", "NormBetweenness"]] = scaler.fit_transform(df_nodes[["Degree", "Betweenness"]])

# === Rôle ===
def get_role(row):
    if row["NormBetweenness"] > 0.6:
        return "Ambassadeur"
    elif row["NormDegree"] > 0.75:
        return "Leader local"
    else:
        return "Satellite"

df_nodes["Role"] = df_nodes.apply(get_role, axis=1)

# === Sous-graphe optimisé ===
key_nodes = df_nodes[df_nodes["Role"].isin(["Leader local", "Ambassadeur"])]["Node"]
selected_nodes = set(key_nodes)

# Pour chaque Leader/Ambassadeur, on ajoute ses meilleurs satellites
for node in key_nodes:
    neighbors = list(G.neighbors(node))
    # On filtre pour ne garder que les satellites
    satellites = [n for n in neighbors if df_nodes.loc[df_nodes["Node"] == n, "Role"].values[0] == "Satellite"]
    # Tri par degré décroissant et on en garde que les 3 plus connectés
    top_satellites = sorted(satellites, key=lambda x: degree[x], reverse=True)[:20]
    selected_nodes.update(top_satellites)

# Sous-graphe final
subG = G.subgraph(selected_nodes)
df_sub = df_nodes[df_nodes["Node"].isin(subG.nodes)].copy()

# === Visualisation ===
pos = nx.spring_layout(subG, seed=42)

# Couleur par rôle
color_map = {
    "Leader local": "#e74c3c",
    "Ambassadeur": "#2980b9",
    "Satellite": "#95a5a6"
}
colors = df_sub["Role"].map(color_map)

# Taille par degré
sizes = 200 + df_sub["NormDegree"] * 10

# Labels que pour les leaders et ambassadeurs
labels = {
    row["Node"]: row["Role"]
    for _, row in df_sub.iterrows()
    if row["Role"] != "Satellite"
}

# Dessin
plt.figure(figsize=(16, 12))
nx.draw_networkx_nodes(subG, pos, node_color=colors, node_size=sizes, alpha=0.9)
nx.draw_networkx_edges(subG, pos, alpha=0.25, width=0.7)

# Légende
from matplotlib.patches import Patch
legend_elements = [
    Patch(color=color_map["Leader local"], label="Leader local"),
    Patch(color=color_map["Ambassadeur"], label="Ambassadeur"),
    Patch(color=color_map["Satellite"], label="Satellite")
]
plt.legend(handles=legend_elements, loc="upper right", fontsize=12)

plt.title("Leadership et satellites filtrés", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.savefig("smart_roles_graph_reduced_satellites.png", dpi=300)
plt.show()
