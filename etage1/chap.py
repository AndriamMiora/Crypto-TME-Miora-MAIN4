import subprocess

class OpensslError(Exception):
    pass

def decrypt(ciphertext, passphrase, cipher='aes-128-cbc'):
    """
    invoke the OpenSSL library (though the openssl executable which must be
    present on your system) to decrypt content using a symmetric cipher.

    The passphrase is an str object (a unicode string)
    The ciphertext is str() or bytes()
    The output is bytes()

    # decryption use
    > ciphertext = encrypted_message
    > m = decrypt(ciphertext, 'foobar')
    """

    # prépare les arguments à envoyer à openssl
    pass_arg = 'pass:{}'.format(passphrase)
    args = ['openssl', 'enc', '-d', '-' + cipher, '-base64', '-pass', pass_arg, '-pbkdf2']

    # si plaintext est de stype str, on est obligé de l'encoder en bytes pour
    # pouvoir l'envoyer dans le pipeline vers openssl
    if isinstance(ciphertext, str):
        ciphertext = ciphertext.encode('utf-8')

    # ouvre le pipeline vers openssl. envoie plaintext sur le stdin de openssl, récupère stdout et stderr
    result = subprocess.run(args, input=ciphertext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    error_message = result.stderr.decode()
    if "bad decrypt" in error_message:
        return None  # Retourne None si le déchiffrement a échoué
    elif error_message != '':
        raise OpensslError(error_message)

    try:
        # Tente de décoder en UTF-8
        return result.stdout.decode('utf-8')
    except UnicodeDecodeError:
        # Si le décodage UTF-8 échoue, retourne la sortie brute ou une erreur personnalisée
        return result.stdout
    #je veux print le fichier décrypter
    print(result.stdout.decode('utf-8'))


passphrase = "rabetrano"
ciphertext = "U2FsdGVkX1/1UwTjflolfau9TczZEgR4HbBQNWsnJcmNxxsK3ayj0NOm7kRjem0z\n"
print(decrypt(ciphertext, passphrase))