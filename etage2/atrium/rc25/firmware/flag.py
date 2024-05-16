# ensemble des flags obtenus jusqu'à présent (MAC)
flags_mac = [
    "cb8e475f8ff09502837a6a906eee377dbaf8251b63289329981a3723023edaed",
    "7218b2eb3692198b346b758cce8333da86427fe160d6670dd4c756d19c65d88f",
    "0de03c11206a98b8436645c8d360900e23e4c25f266d95d72a3721844106473d",
    "fb7eea726a5974188519bf34fa777cfaa49af9e3b00ec976be9e147b7b15ba23",
    "d090287283aa9cc6b8645ac7259e1986c8bdd84d77862de70d11c740b7f01b25",
    "5ccdccc03901f1e321419565e70c2e9a2ffa3aac64a4d023c34c238c712c4705",
    "74c4068893c444395e6131bd41932c69f3613aab06d0e0c0d1d09c08be3979af",
    "aca91b0e77212ffd962044dc5c1e28601674da2aa46715932816165a31f4faf0",
    "3925fb6cd62c435244ccbee3a0dd9f76a54560b98f2a2cb702182c089bdedaa2",
    "80437e29ca7b76f23206009c787ba6684d78d2b98f516c36d626ddff17a9de07",
    "ad3869c90ac2861c55767d478e1903c4362aaf7eef6e099fa3cb9b1e8891b67b",
    "549d9748ff84ab3f1396c99d3cda055ced27c7594085bf6720684d70552a3a94",
    "1b4a94ea36db8023871e706018b31df8f39910448123a28ed004666213019d4d",
    "8316bfa9bed4ef489eaa1466cb790cea2c6b9f7530b8e67d5b6876dd11a3ecbd",
    "ae51ba7c7e2e08d69bb923bde550be50b4d4d1392a2dcddf57f860d806b8b977",
    "54dcca04fe466e00e7b9a9c00769b9aea2371191f774d899fa8f1ea827b6d49c",
    "426d8b8c41d6d391372f914de7adb9b904bb5bcebf525a112c2b9c0b94835393",
    "0944d2e1a748f257280c1783a7f812ab82dfb92bd960a0f0230fa51c9c8520ae",
    "bc1f2cffa3a06ae660d7d1672313a8575dcf9a288d13a994556568a874c8324b",
    "8600f486ac04687861f69d55ab2a23e9841edef3f26e7eb57f094b96e2c31f4e"
]





def hex_to_bin(hex_string):
    # Convertit une chaîne hexadécimale en une chaîne binaire
    bin_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string)*4)
    return bin_string

def extract_X_A_B_C_from_MAC(mac):
    # Convertit le MAC en binaire
    mac_bin = hex_to_bin(mac)
    # Extrait X, A, B et C en utilisant la séquence binaire
    X_bin = mac_bin[0:64]
    A_bin = mac_bin[64:128]
    B_bin = mac_bin[128:192]
    C_bin = mac_bin[192:256]
    # Convertit les binaires en entiers
    X = int(X_bin, 2)
    A = int(A_bin, 2)
    B = int(B_bin, 2)
    C = int(C_bin, 2)
    return X, A, B, C

# Listes pour stocker les valeurs X, A, B, et C extraites
list_X = []
list_A = []
list_B = []
list_C = []

# Boucle sur les MACs pour extraire X, A, B et C
for mac in flags_mac:
    X, A, B, C = extract_X_A_B_C_from_MAC(mac)
    list_X.append(X)
    list_A.append(A)
    list_B.append(B)
    list_C.append(C)

# Affiche les listes X, A, B et C
print("X=", list_X)
print("A=", list_A)
print("B=", list_B)
print("C=", list_C)