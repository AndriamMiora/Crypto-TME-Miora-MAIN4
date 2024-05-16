nom = "Miora"


#ajouter du padding pour avoir une taille multiple de 64
while len(nom) % 64 != 0:
    nom += "0"

#enregistrer les noms dans un fichier
with open("prefixe.txt", "w") as f:
    f.write(nom)