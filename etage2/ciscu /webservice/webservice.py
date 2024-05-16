import yaml
import subprocess
import json

def check_certificates(transaction):
    output = []
    print("transaction: ", transaction)
    
    # 1 : Même nom de banque dans la transaction et dans le certificat de la banque
    #Récupère le nom de la banque dans la transaction
    data_string = transaction.get("data", "")
    data_json = json.loads(data_string)
    bank_name = data_json.get("bank-name", "")
    
    # Récupère le nom de la banque dans le certificat de la banque
    card_string = transaction.get("card", "").get("bank", "").get("name", "")

    print(" Result 1 : bank_name: ", bank_name, "bank_cert_name: ", card_string)

    if bank_name != card_string:
        output.append(0)  # Le nom dans le certificat de la banque ne correspond pas au nom de la banque dans la transaction
    else:
        output.append(1)
        
    print("output: ", output)
    
    
    # 2 : Vérifier la validité du certificat de la carte 
    card_cert = transaction.get("card", {}).get("certificate", "")
    bank_cert = transaction.get("card", "").get("bank", "").get("certificate", "")
    
    with open("transaction_card_certificate.pem", "w") as f:
        f.write(card_cert.rstrip('\n'))
        
    with open("transaction_bank_certificate.pem", "w") as f:
        f.write(bank_cert.rstrip('\n'))

    result = subprocess.run(['openssl', 'verify', '-trusted', 'autorite_cert.pem', '-untrusted' ,'transaction_bank_certificate.pem', 'transaction_card_certificate.pem'], capture_output=True, text=True)

    print("Result 2: ", result)
   
    if "OK" in result.stdout:
        output.append(1)  # Le certificat de la carte est valide
    else:
        output.append(0)  # Le certificat de la carte n'est pas valide

    print("output: ", output)

   
    # 3 : Vérifier si le certificat de la banque est auto-signé
    result = subprocess.run(["openssl", "x509", "-noout", "-issuer"], input=bank_cert, capture_output=True, text=True)
    #print("result 3: ", result)
    # Extraire le sujet et l'émetteur du résultat
    issuer = result.stdout.strip().split("issuer=")[1].split("\n")[0] 
      
    print("Résult 3  issuer: ", issuer)
    if issuer == "CN=__fake__" :
        output.append(0)
    else:
        output.append(1)
        
    print("output: ", output)
    

    # 4 : Vérifier si le certificat de la banque a le bit CA
    result = subprocess.run(["openssl", "x509", "-noout", "-text"], input=bank_cert, capture_output=True, text=True)
    print("Result 4: ", result)
    # Vérifier le résultat
    if "CA:TRUE" in result.stdout:
        output.append(1)
    else:
        output.append(0)
        
    print("output: ", output)
    
    
    # 5 : Vérifier si la signature du challenge par la carte est valide
    challenge = transaction.get("data", "")
    with open("challenge.txt", "w") as f:
        f.write(challenge.rstrip('\n'))
        
    signature = transaction.get("signature", "")
    
    binary_signature = bytes.fromhex(signature)
    
    with open("signature.der", "wb") as f:
        f.write(binary_signature)

    # Récupérer la clé publique de la carte 
    result = subprocess.run(["openssl", "x509", "-noout", "-pubkey", "-in", "transaction_card_certificate.pem", "-out", "card_pubkey.pem"], capture_output=True, text=True)

    # Vérifier la signature du challenge par la carte
    result = subprocess.run(["openssl", "dgst", "-sha256", "-verify", "card_pubkey.pem", "-signature", "signature.der", "challenge.txt"], capture_output=True, text=True)
    print("Result 5: ", result)

    if "Verified OK" in result.stdout:
        output.append(1)
    else:
        output.append(0)

    print("output: ", output)

    # 6 : Vérifier si le certificat de la carte est signé par celui de la banque
    result = subprocess.run(["openssl", "x509", "-noout", "-issuer"], input=card_cert, capture_output=True, text=True)
    issuer_card = result.stdout.strip().split("issuer=")[1].split("\n")[0]

    if  bank_name in issuer_card:
        output.append(1)
    else:
        output.append(0)
    
    print("output: ", output)

    # 7 : Vérifier si le certificat de la banque est signé par celui de l'autorité de certification("autorite_cert.pem")
    result = subprocess.run(["openssl", "x509", "-noout", "-issuer"], input=bank_cert, capture_output=True, text=True)
    issuer_bank = result.stdout.strip().split("issuer=")[1].split("\n")[0]
    with open("autorite_cert.pem", "r") as f:
        autorite_cert = f.read()
        
    result = subprocess.run(["openssl", "x509", "-noout", "-issuer"], input=autorite_cert, capture_output=True, text=True)
    issuer_autorite = result.stdout.strip().split("issuer=")[1].split("\n")[0]
    
    print("Result 7: issuer_autorite: ", issuer_autorite, "issuer_bank: ", issuer_bank)
    
    if issuer_autorite in issuer_bank:
        output.append(1)
    else:
        output.append(0)
    
    print("output: ", output)


    # 8 Vérifier si subject de la carte est égal à celui au numéro de carte
    card_number = transaction.get("card", "").get("number", "")
    result = subprocess.run(["openssl", "x509", "-noout", "-subject"], input=card_cert, capture_output=True, text=True)
    subject_card = result.stdout.strip().split("subject=")[1].split("\n")[0]
    
    print("Result 8: subject_card: ", subject_card, "card_number: ", card_number)
    
    if card_number in subject_card:
        output.append(1)
    else:
        output.append(0)
    # Vérifier si toutes les conditions sont vraies, sinon renvoyer 1
    if 0 in output:
        return 0
    else:
        return 1


# Charger le fichier batch.yml
with open("batch.yaml", "r") as f:
    data = yaml.safe_load(f)

output_list = []

# Boucle à travers chaque transaction 
#for transaction, i in zip(data.get("batch", {}).get("transactions", []), range(3) ):
for transaction in data.get("batch", {}).get("transactions", []):
    output = check_certificates(transaction)
    output_list.append(output)


print("output_list: ", output_list)
