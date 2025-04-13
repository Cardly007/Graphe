import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('reciprocal_relation.csv')

# # Compter les connexions de chaque nœud
node_degrees = df['FromNodeId'].value_counts().reset_index()
node_degrees.columns = ['Node', 'Degree']


# Sélectionner les 10 000 nœuds les plus connectés
top_nodes = node_degrees.nlargest(10000, 'Degree')['Node']

# Filtrer les relations pour ne garder que celles entre ces nœuds
df_filtered = df[df['FromNodeId'].isin(top_nodes) & df['ToNodeId'].isin(top_nodes)]

# Sauvegarder le fichier échantillonné
df_filtered.to_csv('reciprocal_relation_sample.csv', index=False)
