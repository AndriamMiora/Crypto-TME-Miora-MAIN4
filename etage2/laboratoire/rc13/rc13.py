import secrets
import subprocess
import binascii
import json

class OpensslError(Exception):
    pass

def encrypter_texte(plaintext, mot_de_passe, cipher='aes-128-cbc'):
    """Utilise la bibliothèque OpenSSL (via l'exécutable openssl présent sur votre système)
       pour chiffrer le contenu en utilisant un chiffrement symétrique.

       Le mot_de_passe est une chaîne de caractères str (une chaîne unicode)
       Le texte_en_clair est str() ou bytes()
       La sortie est de type bytes()

       # Utilisation du chiffrement
       >>> message = "texte avec caractères accentués"
       >>> c = encrypter_texte(message, 'motdepasse')       
    """
    # Prépare les arguments à envoyer à OpenSSL
    pass_arg = 'pass:{}'.format(mot_de_passe)
    args = ['openssl', 'enc', '-' + cipher, '-base64', '-pass', pass_arg, '-pbkdf2']
    
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    result = subprocess.run(args, input=plaintext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    message_erreur = result.stderr.decode()
    if message_erreur != '':
        raise OpensslError(message_erreur)

    return result.stdout.decode()

def chiffrer_avec_cle_publique(cle_publique, texte_en_clair):
    args = ['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', cle_publique]

    if isinstance(texte_en_clair, str):
        texte_en_clair = texte_en_clair.encode('utf-8')

    result = subprocess.run(args, input=texte_en_clair, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    message_erreur = result.stderr.decode()
    if message_erreur != '':
        raise OpensslError(message_erreur)

    hex_encodé = binascii.hexlify(result.stdout).decode()
    return hex_encodé

# Étape 1: Générer une clé de session aléatoire
entier_aléatoire = secrets.randbits(16 * 8)
clé_session = format(entier_aléatoire, 'x')

# Étape 2: Écrire la clé de session dans un fichier
with open("clé_session.txt", "w") as fichier:
    fichier.write(clé_session)

# Étape 3: Message à chiffrer
message = "Message"

# Chiffrement du message
texte_chiffré = encrypter_texte(message, clé_session)

# Clé publique du secrétaire
cle_publique_secretaire = "secretaire_pk.pem"

# Chiffrement avec la clé publique
clé_session_chiffrée = chiffrer_avec_cle_publique(cle_publique_secretaire, clé_session)

# Création d'un dictionnaire pour JSON
données_chiffrées = {
    "session-key": clé_session_chiffrée,
    "ciphertext": texte_chiffré
}

# Écrire le JSON dans un fichier
with open("final.json", "w") as fichier_json:
    json.dump(données_chiffrées, fichier_json, indent=2)

# Afficher le JSON final
print("Résultat :\n", json.dumps(données_chiffrées, indent=2))
