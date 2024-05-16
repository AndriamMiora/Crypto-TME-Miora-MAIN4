#Etape 1 : On a 2 messages chiffrés sur le pannonceau

walkernicholas="a7ae6900b604872c445da6fcd219781f8026843ebccb4a1831e9592e5511666ca98b4fa2829789f5b82fe7e638e5ffc870eec286745e122f790aa3a8ed0aa7a44c8dfedb912ba2d22eab1e0eaa07c8c7d4124fc91f63ee163fd8fa59d3b4b4d06c68c0cc7339545590fe87d2ee92a3a64568d2cb26b8a79008c285e3f677f812a140c2ff4b137405e0fe6672dd13e0dea0674bd9f3bf2712928f8d56c1650d9be4f751120c0880f2eeba181189f250ee8897731d03400a2c25b16f18daa40d4f70c21b4fd4ff7712667c549d44b8f20a882ab1c41b471a91b69b61a5bd29e29d3dea33acfd145e61accc900b9e8deaaad01373d9a5b4885af2b05c95b20afbc6"

rowlandjesse="4b83f366141aa7c2f2d153ca4653f3c6bc5ac42b19f801ca0b85eb761bc65a43023e9c226e2027a56895071eea9903dbebce10d26b32ed0bca50eb382c6a24cf3ece961a275e6c43e242ca0b75d4040dab48b560f9fbd1a337a642d2a0bfae0eccef5878dd8db937abda2dbdfac01aaf9fc2c670c717a13f0f0115d5af9e9329a4294c8e6fb0f2d15a736b703f45fe2803253a6581bccf728886dcec49c95d020481d60a59c23dde511d8832453578d2a5c42b4ab833cd75c9c85a76450d2a771e7d7e29fb31a1f2871c591e1521c74d896e9cbe28591b6c9f72956a1b7e14bb9afe711632c25a68e863b7064edce4667bb051aac47536f5c3005d701848eff6"

# Etape 2 : On doit récupérer les clés publiques pour extraire les exposants et les modules pour les 2 individus et on les met dans des fichiers PEM
#Les mettre dans un fichier PEM

#Etape 3 : On utilise les fonctions suivantes pour obtenir les exposants et les modules et le message déchiffré à partir des clés publiques
from sympy import mod_inverse
import cryptography.hazmat.primitives.serialization

# On extrait les exposants et les modules des clés publiques
def euclide_etendu(a, b):
    """
    Calcule le PGCD de a et b ainsi que les coefficients de Bézout u et v tels que u*a + v*b = PGCD(a, b)
    Entrées:
        a (int): Le premier entier
        b (int): Le deuxième entier
    Sortie:
        Tuple[int, int, int]: Le PGCD de a et b ainsi que les coefficients de Bézout u et v
    """
    # Initialisation des variables
    r, u, v, r_, u_, v_ = a, 1, 0, b, 0, 1
    
    # Algorithme d'Euclide étendu
    while r_ != 0:
        q = r // r_
        r, u, v, r_, u_, v_ = r_, u_, v_, r - q * r_, u - q * u_, v - q * v_
    
    # Retourne le PGCD et les coefficients de Bézout u et v
    return r, u, v

def CRT(c1, c2, e1, e2, n):
    """
    Décrypte un message chiffré avec le théorème des restes chinois

    Entrées:
        c1 (int): Le premier message chiffré
        c2 (int): Le deuxième message chiffré
        e1 (int): L'exposant de chiffrement du premier message
        e2 (int): L'exposant de chiffrement du deuxième message
        n (int): Le module de chiffrement

    Sortie:
        int: Le message déchiffré
    """
    # Trouver u et v tels que u*e1 + v*e2 == 1
    _, u, v = euclide_etendu(e1, e2)        
    # Calculer c1^u mod n et c2^v mod n
    c1_u = pow(c1, u, n)
    c2_v = pow(c2, v, n)
    
    # Calculer m = c1^u * c2^v mod n
    m = (c1_u * c2_v) % n
    return m

def extraction_exposant(chemin_pk):
    """
    Extrait l'exposant de la clé publique RSA à partir du fichier PEM
    Entrée:
        chemin_pk (str): Le chemin vers le fichier PEM contenant la clé publique
    Sortie:
        int: L'exposant de la clé publique
    """
    # Charger le contenu du fichier
    with open(chemin_pk, "rb") as fichier:
        contenu = fichier.read()
    
    # Charger la clé publique
    public_key = cryptography.hazmat.primitives.serialization.load_pem_public_key(contenu)
    
    # Obtenir l'exposant public e
    e = public_key.public_numbers().e
    
    return e

def extraction_module(chemin_pk):
    """
    Extrait le module de la clé publique RSA à partir du fichier PEM
    Entrée:
        chemin_pk (str): Le chemin vers le fichier PEM contenant la clé publique
    Sortie:
        int: Le module de la clé publique
    """
    # Charger le contenu du fichier
    with open(chemin_pk, "rb") as fichier:
        contenu = fichier.read()
    
    # Charger la clé publique
    public_key = cryptography.hazmat.primitives.serialization.load_pem_public_key(contenu)
    
    # Obtenir le module N
    n = public_key.public_numbers().n
    
    return n

#Etape 5: On applique les fonctions pour obtenir le message déchiffré

#On récupère les messages chiffrés
c2 = int(rowlandjesse, 16)  # Message chiffré avec la première clef publique
c1 = int(walkernicholas, 16)  # Message chiffré avec la deuxième clef publique

#On extrait les exposants et les modules des clés publiques
e1 = extraction_exposant("walkernicholas.pem")      # Exposant public de la première clef publique
e2 = extraction_exposant("rowlandjesse.pem")      # Exposant public de la deuxième clef publique (il est possible que ce soit différent de e1)
n1 = extraction_module("rowlandjesse.pem")  # Module commun des deux clefs publiques
n2 = extraction_module("walkernicholas.pem")  # Module commun des deux clefs publiques

print("Exposant public de la première clef publique:", e1)
print("Exposant public de la deuxième clef publique:", e2)
print("Module commun des deux clefs publiques:", n1==n2)

# On utilise le théorème des restes chinois pour déchiffrer le message
message_dechiffre = CRT(c1, c2, e1, e2, n1)
#On reconvertit le message en bytes , on utilise 'big' pour dire que l'octet de poids fort est en premier
message_dechiffre = message_dechiffre.to_bytes((message_dechiffre.bit_length() + 7) // 8, 'big')
print("-----------------")
print("Message déchiffré:", message_dechiffre)

#On obtient le message "0c5bea89c7b6f09abfc1196bf666e4bb" à donner au digicode.
