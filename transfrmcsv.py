import csv

# Fichier d'entrée (fichier texte)
# input_file = "soc-LiveJournal1.txt"
input_file = "reciprocal_relations.txt"

# Fichier de sortie (fichier CSV)
# output_file = "soc-LiveJournal1.csv"
output_file = "reciprocal_relation.csv"


# Ouvrir les fichiers
with open(input_file, "r") as infile, open(output_file, "w", newline='') as outfile:
    # Créer un écrivain CSV
    csv_writer = csv.writer(outfile)
    
    # Écrire l'en-tête CSV
    csv_writer.writerow(["FromNodeId", "ToNodeId"])
    
    # Lire le fichier d'entrée ligne par ligne
    for line in infile:
        # Ignorer les lignes de commentaires
        if line.startswith("#"):
            continue
        
        # Séparer les valeurs de la ligne
        values = line.strip().split()  # Diviser par espace ou tabulation
        
        # Écrire la ligne dans le fichier CSV
        csv_writer.writerow(values)

print("Conversion terminée. Le fichier CSV a été créé :", output_file)
