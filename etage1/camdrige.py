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

def test_passphrase(filename, ciphertext, expected_decrypt):
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            print("Testing passphrase:", line)  # Ajout du print pour la passphrase traitée
            decrypted = decrypt(ciphertext, line)
            if decrypted == expected_decrypt:
                print("Paraphrase found:", line)
                return  # Sort de la fonction si la passphrase correcte est trouvée
    print("Paraphrase not found for any passphrase in the file.")  # Indique que la passphrase correcte n'a pas été trouvée

filename = "cambridge.txt"
ciphertext = "U2FsdGVkX1/HCZSmrOQV5JdLFyr12FS3oQycLlV0/zhIiw5aaOZb+lSk9WfZD6mr\n"
expected_decrypt = "reams furor likes mucho quips"

test_passphrase(filename, ciphertext, expected_decrypt)
