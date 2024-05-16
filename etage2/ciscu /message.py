M = "I, the lab director, hereby grant Miora permission to take the BiblioDrone-NG."




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


#chemin fichier

key_path = "director_pk.pem"

#lecture de la clé publique

with open(key_path, 'r') as file:
    key = file.read()

public_key = cryptography.hazmat.primitives.serialization.load_pem_public_key(key.encode())

n = public_key.public_numbers().n
e = public_key.public_numbers().e

print("n : ", n)
print("e : ", e)


k = key_length(n)
print("k : ", k)
M = M.encode()
M_PKCS_encoded = emsa_pkcs1_encode(M,k)
print("M_PKCS_encoded : ", M_PKCS_encoded)
# print("M_PKCS_int : ", os2ip(M_PKCS_encoded))

# x = sympy.randprime(1, n-1)

# print("x : ", x)
# print("x_inv", x_inv)

x = 19152870488268069675986209239318862638998494354844254820330375352597756481751737673464113811148190970485408680156190640958499971933634152896824097374275770548520559502527323978589825137661765824508684600595718445998880400892040671370055042754786504029655959341756860910750286921228351267085777237346805523618228360097219654205410618409868839441648143894409451545416847710883639506673114486722377094236169993165992366105615239908362758265973262819394323578737734178285137442446129522407397873374344565135067288697924478838241950241534047399515916974733694555012324055555748912152715972370041571842060139339519974176377
x_inv = pow(x, -1, n)
# print(x*x_inv % n == 1) TRUE

# Calculer (M * x**e) mod N
M_int = os2ip(M_PKCS_encoded)
new_M = ( M_int * pow(x, e,n)) % n
print("new_M (int) : ", new_M)

hex_encoded_new_M = hex(new_M)[2:]
print("new_M (hex) : ", hex_encoded_new_M)


# - le serveur renvoie (M * x*e)d == (Md) * (xed) == x * M*d mod N.
signature_machine = "65716484860859090e23a47f1050f6b6e48a6bd620907e141128ac375612adc7d63c7fe141f9a1effe0c8aaef5ab6ede79a920e1739735e6853723aa9d7251edd4a7950cf85ee117454f035de33a1693a4f6194d7f333b28f6e87eda430bad359e694ae7a144370ad30e10cc11e5fc3481dbea2b7c7bd3ab0cb5786878084f94b6b1f65add80967b3e786f052b6b3e5689bb3860efdb1eb146b02570deae25e73211b1471780e2593b1e30f0ae3b0f145e1e21c785746a3280e51cfdc396982e4d497982867427ea5376de45257b9d15024de3ddab0feb54119e79306403e74b0e11ce96f2b66fd33868be02784cfee543d154f6f23e159b8627c459147af6cd"
signature_machine_int = int(signature_machine,16)

# - il suffit d'éliminer le ``masque'' x (en multipliant par l'inverse de x
#   modulo N) et on obtient M**d mod N, c'est-à-dire la signature voulue.
signature = (signature_machine_int * x_inv) %n
print("signature en int : ", signature)
signature_bytes = i2osp(signature,k)
print("signature en bytes", signature_bytes)


# Vérification
if(rsa_pkcs_verify(n,e,M,signature_bytes)) :
    print("la signature est bien verrifiée par la clef publique")
    print("signature en hex : ", hex(signature)[2:])