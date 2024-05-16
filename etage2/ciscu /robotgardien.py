TEXTE_A_SIGNER = "I, the lab director, hereby grant Miora permission to take the BiblioDrone-NG."

import cryptography.hazmat.primitives.serialization
from hashlib import sha256
import random
import sympy

# Function names respect those in https://www.ietf.org/rfc/rfc3447.txt
# SHA-256
HASH_ID = b'010\r\x06\t`\x86H\x01e\x03\x04\x02\x01\x05\x00\x04 '

def i2osp(x : int, k : int) -> bytes:
    """
    Convert the integer x to a sequence of k bytes
    """
    return x.to_bytes(k, byteorder='big')

def os2ip(x : bytes) -> int:
    """
    Convert the sequence of bytes to an integer
    """
    return int.from_bytes(x, byteorder='big')

def emsa_pkcs1_encode(M : bytes, k : int) -> bytes:
    """
    Encode a message into k bytes for RSA signature
    """
    h = sha256(M)
    T = HASH_ID + h.digest()
    if len(T) + 11 > k:
        raise ValueError("Message Too Long")
    PS = bytes([0xff] * (k - len(T) - 3))
    EM = bytes([0x00, 0x01]) + PS + bytes([0x00]) + T
    return EM

def emsa_pkcs1_decode(EM : bytes, k : int) -> bytes:
    """
    Given an EMSA_PKCS1-encoded message, returns the Hash

    >>> x = emsa_pkcs1_encode("toto", 128)
    >>> emsa_pkcs1_decode(x, 128) == sha256("toto".encode()).digest()
    True
    """
    if len(EM) != k:
        raise ValueError("Incorrect Size")
    if EM[:2] != bytes([0x00, 0x01]):
        raise ValueError("Incorrect Header")
    i = 2
    while EM[i] != 0:
        if EM[i] != 0xff:
            raise ValueError("Incorrect Filler")
        i += 1
        if i == k:
            raise ValueError("Only Filler")
    if i < 10:
        raise ValueError("Not enough filler")
    T = EM[i+1:]
    if T[:len(HASH_ID)] != HASH_ID:
        raise ValueError("Bad Hash ID")
    H = T[len(HASH_ID):]
    return H

def key_length(n : int) -> int:
    """
    key length in bytes
    """
    return (n.bit_length() + 7) // 8

def rsa_pkcs_sign(n : int, d : int, M : bytes):
    """
    RSA Signature using PKCS#1 v1.5 encoding
    """
    k = key_length(n)
    EM = emsa_pkcs1_encode(M, k)
    m = os2ip(EM)
    s = pow(m, d, n)
    S = i2osp(s, k)
    return S

def rsa_pkcs_verify(n : int, e : int, M : bytes, S : bytes) -> bool:
    """
    Verify RSA PKCS#1 v1.5 signatures
    """
    k = key_length(n)
    if len(S) != k:
        raise ValueError("Bad length")
    s = os2ip(S)
    m = pow(s, e, n)
    EM = i2osp(m, k)
    H = emsa_pkcs1_decode(EM, k)
    return (H == sha256(M).digest())


# 1. Etape 1 : Charger la clé publique  et obtenir les valeurs de N et e
chemin_fichier = "director_pk.pem"

# Lire le contenu du fichier
with open(chemin_fichier, "rb") as fichier:
    contenu = fichier.read()

# Charger la clé publique
public_key = cryptography.hazmat.primitives.serialization.load_pem_public_key(contenu)

# Extraire les valeurs de N et e
n = public_key.public_numbers().n
e = public_key.public_numbers().e

# On affiche les valeurs de N et e
print("N (Module) :", n)
print("e (Exposant) :", e)

#2. Etape 2 : Choisir un entier aléatoire X tel que 1 < X < N

# On utilise la fonction randprime de la bibliothèque sympy pour générer un nombre premier aléatoire
# X = sympy.randprime(1, n-1)
X = 21154291739385060415134221989305468105230049649098823050634998242648553117819123264870515840055816216338837772161592112112713598355930144537550492845139745835208668388479348920401920522900874841893880357495720810230370077954236851257582155893913603417888658280245750208991279559711763346980917677167474054291515986844235583316028183917856613734783622320304198805023329484587159707240620576734527180384841271893384518565463848519399450871537937062223787547003760058566006569175574430457258036727120688436347191584101628044342524263068060260167753440303517984168646952061222432040964029310139614004723315106080784676673
print("X :", X)

#3. Etape 3 : Calculer l'inverse de X modulo N
X_inverse = pow(X, -1, n)
print("X inverse :", X_inverse)

#4. Etape 4 : Masquage du message 
M = TEXTE_A_SIGNER.encode()
k = key_length(n)
Message_encode= emsa_pkcs1_encode(M, k)

#On masque le message en réalisant : M * X^e mod n
m = (os2ip(Message_encode)*pow(X,e,n)%n)
m_hex = hex(m)[2:]

print("Message masqué : ", m_hex)

# Etape 5 : On donne le message masqué à signer à l'oracle (le robot) et on récupère la signature S
S = "26810cd2ba99db3b65380981c8c48240ddf45f14540f2b5a0487e74c555354f3dd49a0feeb706d381650d73fb665e216063dc5a66d49730d7eb6880dd4f1224686bbb1e99a802084f0281d9b3b767cbaf9cd2cc6fde5f89af0e1d18e2b39936fa355400d567be5b2948e556be30aafe068c718b29ccb028d6f197b545454396083acf58d3b94002c59ae211c115254cebc905d19c40d3525a326189f8fd64c66d7a6f919ce4b3bad4e14d94196a64aac56e1f75f284b695431f6a0ccb0e692ce026a2697ca86bdbe32fc11bdd25b641900a8c7e10b1ab78a8620eeefea670930b9c703b875aaecfcf6240880e5d6491acd699a0ee98150e2f2df436109defc48"
signature = (int(S, 16) * X_inverse) % n

resultat = i2osp(signature, key_length(n))
print("Signature démasquée : ", resultat)

# Etape 6 : Vérification de la signature, on vérifie que la signature est bien vérifiée par la clé publique
if(rsa_pkcs_verify(n,e, TEXTE_A_SIGNER.encode(),resultat)) :
    print("La signature est valide , car elle a été vérifiée par la clé publique.")
    print("Signature en hex : ", hex(signature)[2:])

    