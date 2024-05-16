from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

# Charger la clé publique depuis le fichier PEM
#rb = read binary
with open('public_andrea43.pem', 'rb') as f:
    public_key_pem = f.read()

# Importer la clé publique RSA
public_key = RSA.import_key(public_key_pem)

# Vérifier si la clé est une clé publique RSA
if isinstance(public_key, RsaKey) and not public_key.has_private():
    # Récupérer les composantes n et e
    n = public_key.n
    e = public_key.e
    print("--Andrea43--")
    print("Composante n :", n)
    print("Composante e :", e)
else:
    print("La clé n'est pas une clé publique RSA valide.")


with open('public_scottmccall.pem', 'rb') as f:
    public_key_pem = f.read()

# Importer la clé publique RSA
public_key = RSA.import_key(public_key_pem)

# Vérifier si la clé est une clé publique RSA
if isinstance(public_key, RsaKey) and not public_key.has_private():
    # Récupérer les composantes n et e
    n = public_key.n
    e = public_key.e
    print("--Scott--")
    print("Composante n :", n)
    print("Composante e :", e)
else:
    print("La clé n'est pas une clé publique RSA valide.")

