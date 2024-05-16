from hashlib import sha256
from Crypto.Cipher import AES
import base64

# IV initial fourni
target_iv = "7e6049198579fb631a81265e0976cd63"

# Fonction pour générer toutes les combinaisons de 16 bits
def generate_seeds():
    seeds = []
    for a in range(256):
        for b in range(256):
            seeds.append(bytes([a, b]))
    return seeds

# Fonction pour étendre la clé à partir de la seed
def key_expansion(seed : bytes) -> bytes:
    state = seed
    output = b''
    for i in range(8):
        state = sha256(state).digest()
        output += state[:4]
    return output

# Lecture du message chiffré depuis un fichier
with open("message.txt", "r") as file:
    encrypted_message = base64.b64decode(file.read())

# Génération de toutes les seeds possibles
seeds = generate_seeds()

# Essayer chaque seed
for seed in seeds:
    # Calculer la clé et l'IV correspondants
    key_material = key_expansion(seed)
    key = key_material[0:16]
    iv = key_material[16:32]

    # Vérifier si l'IV calculé correspond à l'IV cible
    if iv.hex() == target_iv:
        # Déchiffrer le message avec la clé et l'IV trouvés
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = cipher.decrypt(encrypted_message)

        # Supprimer le padding
        padding_length = decrypted_message[-1]
        decrypted_message = decrypted_message[:-padding_length]

        # Afficher les données décryptées
        print("Clé trouvée:", key.hex())
        print("IV trouvé:", iv.hex())
        print("Message décrypté:\n", decrypted_message.decode())
        break
