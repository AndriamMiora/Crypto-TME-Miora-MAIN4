# Importation des modules nécessaires
from Crypto.PublicKey import RSA  # Module pour la génération de clés RSA
import base64  # Module pour le décodage de chaînes base64

# Chaîne encodée en base64
base64_string = "ea+++ATRIUM+++ed"

# Décodage de la chaîne base64 en octets
decoded_bytes = base64.b64decode(base64_string)
print(decoded_bytes)  # Affichage des octets décodés

# Conversion des octets en une valeur décimale
decimal_value = int.from_bytes(decoded_bytes, byteorder='big')
print(decimal_value)  # Affichage de la valeur décimale

# Génération de la paire de clés RSA avec la valeur 'e' spécifiée
key = RSA.generate(bits=2048, randfunc=None, e=decimal_value)

# Enregistrement de la clé publique dans un fichier PEM
with open('public_atriumkey.pem', 'wb') as f:
    f.write(key.publickey().export_key('PEM'))

# Enregistrement de la clé privée dans un fichier PEM
with open('private_atriumkey.pem', 'wb') as f:
    f.write(key.export_key('PEM'))
