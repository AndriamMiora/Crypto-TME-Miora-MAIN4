import cryptography.hazmat.primitives.serialization
from sympy import mod_inverse

# Étape 1 : Récupérer les messages chiffrés de chaque individus
message_bbowman = "bab146807d030f0f6b6beea3e76811fda6c6e321b4e60e9168da8780a8bcadee34e6d091311883320d0be14c3b2d4a72f1d3448ed8fde8c723e25bc7836869e296e0bd734e6a27e133b181b7c1b8a2d71d1e692895d6e3d84a7c70505a28d80d42ca083a3eff326fd9be5308092ef7d10de98ecf53cbc5895d8b777f4007ad040d1036e4d251f601bef9007f9a2cd28f986470e6bace1f8d3088fa32befa6ab7f0e4ffd4bf9f94bbf28dea33ad20cee6488d83bcc5decc4abf205af238ebe0b8e7a00f2fba69f25459c78ea9d889508383fea6a9973e34af4f4befaa96adb85f1b2751b8afbce0784eaf93f313b7235503c58adf26aced32c4800520846a4cb5"
message_john71 = "0194cd488a6ef8ac54a6479ce8831968cb112b0ec7163205957b6ba92ca33db0d7774af682e0d5a6d0c9cd1da31451074d54a4dd7cdfb94917a059c3b4801e556cf18d1be6f332d0c3da99764869d23ce73f33be70b50003b8ad2b99190ac5fd54e9a323311560f33fb2d0e6937e3cd9f9fbc1c9591246fbeb3d8d5383bbfb0c03add2d56f6a2866ccd4fe610f948af00d5991d7f179ed5f77f970d79eda9d938ab3cb456e5d160e39c3a50b6d52a11018f0239b9a4e34b689c13ca6aed704041072d64c86c4801ef1a79690c0d116c1858b979e7733a73e8828e151554bb6d9495548fa6a81b1e0b615d35bdcb23e09cdad759e15d2f5531f1709deff59dde3"
message_lporter = "2c61b448c0296fe1f49f344d52d457d3fd664cc50456a904b029dfeaa19b3d53ff7090c742ed2f09c81d4bf76d70e31e5fdcc48634727e7e4387909d38866d2082ba1695cfd226adf98b9c953fb37c78549d3ee855bd9b170634dc2577d09aa5816e75b06d85c3381f400733d2b7e39db1d58d7f3986ff44de62aa1e326c47ae1a5c402a5bad7dba7c70843dd9512ad2f4c18f6e670e3b58b690d8db23728ece0aeb17da77a0851f3a3af13ab0f7549b2366efb3ac1e74349be6a6d141f3ba41cb106a432c9fec62c6820615ffaaa8dfb56aa650cf7491cdd67042a59a971b8752f2f5ab21b0f65d65e51a398f2a744720c7fa8ed315fa692bd91e6efe85fb07"

# Convertir les nombres hexadécimaux en entiers
c1 = int(message_bbowman, 16)
c2 = int(message_john71, 16)
c3 = int(message_lporter, 16)

# Étape 2 : Examiner les trois clefs publiques pour en extraire les exposants et les modules.
# On récupère les clefs publiques en extrayant l'exposant et le module de chaque clé.
def extraire_exposant_module_de_fichier_pem(chemin_fichier):
    """
    Extrait l'exposant et le module de la clé publique RSA à partir du fichier PEM.
    """
    # Charger le contenu du fichier
    with open(chemin_fichier, "rb") as fichier:
        contenu = fichier.read()
    
    # Charger la clé publique
    cle_publique = cryptography.hazmat.primitives.serialization.load_pem_public_key(contenu)
    
    # Obtenir l'exposant public 'e' et le module 'n'
    exposant = cle_publique.public_numbers().e
    module = cle_publique.public_numbers().n
    
    return exposant, module

# Récupérer les exposants et les modules des clefs publiques
exposant1, module1 = extraire_exposant_module_de_fichier_pem("bbowman.pem")
exposant2, module2 = extraire_exposant_module_de_fichier_pem("john71.pem")
exposant3, module3 = extraire_exposant_module_de_fichier_pem("lporter.pem")

# Comparer les modules et les exposants des clefs publiques
print("Les modulos sont tous égaux :", module1 == module2 == module3)
print("Les exposants sont tous égaux : ", exposant1 == exposant2 == exposant3)

# Étape 3 : Appliquer le théorème des restes chinois pour résoudre le système d'équations
# On utilise le théorème des restes chinois pour résoudre le système posé.
def theoreme_des_restes_chinois(module, texte_chiffre):
    """
    Résoudre le système en utilisant le théorème des restes chinois.
    """
    total = 0
    produit = 1
    for i in range(len(module)):
        produit *= module[i]
    for i in range(len(module)):
        produit_partiel = produit // module[i]
        inverse = mod_inverse(produit_partiel, module[i])
        total += texte_chiffre[i] * inverse * produit_partiel
    return total % produit

# Appliquer le théorème des restes chinois pour obtenir le message
message_recupere = theoreme_des_restes_chinois([module1, module2, module3], [c1, c2, c3])

print("Après application du théorème des restes chinois, le message récupéré est :\n", message_recupere)

# Étape 4 : Calculer la racine cubique du message obtenu
# On réalise la racine cubique sur le message obtenu
def calculer_racine_cubique_entiere(n):
    """
    Calculer la racine cubique entière.
    """
    x = n // 3
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            break
        x = y
    return x

# Calculer la racine cubique sur le message obtenu
racine = calculer_racine_cubique_entiere(message_recupere)
message_dechiffre = racine.to_bytes((racine.bit_length() + 7) // 8, 'big')

# Étape 5 : Convertir le message en hexadécimal
message_hexadecimal = hex(racine)[2:]
print("Le message récupéré est : ", racine)
print("Le mot de passe est : ", message_hexadecimal)
print("Le message déchiffré est : ", message_dechiffre)

#On a comme mot de passe : 7ccceb1cf0601e96341f5a5fee2c5699