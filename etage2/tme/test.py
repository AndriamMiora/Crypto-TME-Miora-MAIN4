import random

# Test de primalité de Miller-Rabin
def miller_rabin(n, k):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Calcul de la taille en octets d'un nombre
def bit_size(a:int) -> int:
    return int((a.bit_length()+7)//8)

# Conversion d'un entier en tableau d'octets
def int_to_bytes(a):
    return a.to_bytes(bit_size(a),'big')

# Algorithme d'Euclide étendu
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

# Entrée : Nombre premier en hexadécimal
a = int("7b54ecaba13bdecee2dd13b19c8e1e1805cbdc532f961d40544799bdac86954b5f880d180c29ae8b71fc9752ed373222fe9549ecaec60d7cc1b922e53358ab314e67218343c627cdc5c1fa67a73d472b000b66b4a0f6b65f011d4fc52296aaf77cb9302817b809cb7055e7edef5c8549f26b3f3efd3fe2e4b8fae46f1a260a82292f6b686a2f4fb68925ca932a1d00a29cada81a1769fcd0001696e004163f7f133bcd0fb27155aa822e24e6be6b05e4dd508f66ccf28ca32464f232013d524cf7a8823dea929f0319e9c43a82d23c12e948295f3344ee376b6fe478ac44b6b868d3b030d9a65dafc872044ba9cec4e4ca67dd41f56566515364f1b9b1a28cd", 16)

# Nombre premier a + 2^1950
b = a + 2**1950

# Nombre premier en hexadécimal
q = int("6d7bd751a506215c0646d994136af9be03b7d7e74a6b523ff8fba4cbf861fcb3fcc5b4ba1d7a77655774c65dd1bb0603", 16)

# Constante arbitraire
c = 20000

# Calcul de la taille en bits de b
len_b = bit_size(b)

# Calcul de la borne supérieure de Q'
maxQprim = (b-a)//(c*pow(len_b,2))

# Initialisation de Q' avec 2*q
Qprim = 2*q 

# Liste des diviseurs
diviseur = [2]    

# Construction de Q'
while bit_size(Qprim) != bit_size(maxQprim):
    pi = random.choice([i for i in range(2, min(q-1, pow(2,8*(bit_size(maxQprim)-bit_size(Qprim)))) + 1) if miller_rabin(i, 10)])
    Qprim *= pi
    diviseur.append(pi)

# Division de a et b par Q'
ak = a // Qprim
bk = b // Qprim

# Recherche d'un nombre premier pk
while True:
    pk = random.randint(ak, bk)
    if miller_rabin(pk, 2) and miller_rabin(Qprim*pk + 1, 2):
        Q = Qprim*pk
        diviseur.append(pk)
        p = Q + 1
        print('p = ', p)
        break

# Nombre d'essais pour trouver g
n_try = 100

# Recherche d'un générateur g
for _ in range(n_try):
    g = random.randint(2, p - 1)
    if all(pow(g, Q//pi, p) != 1 for pi in diviseur):
        print('g = ', g)
        break

# Affichage de (p-1)//q
print('(p-1)//q = ', str(diviseur)[1:-1])
