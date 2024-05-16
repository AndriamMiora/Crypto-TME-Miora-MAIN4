import random

# Fonction pour générer une séquence similaire à la fonction range de Python 2
def xrange(k):
    """
    Génère une séquence similaire à la fonction range de Python 2.

    Entrée :
        k : int - Le nombre maximal de la séquence.

    Sortie :
        Un générateur produisant les nombres de 0 à k-1.
    """
    return (i for i in range(k))

# Test de primalité de Miller-Rabin avec k itérations
def miller_rabin(n, k):
    """
    Teste la primalité d'un nombre à l'aide de l'algorithme de Miller-Rabin.

    Entrées :
        n : int - Le nombre à tester.
        k : int - Le nombre d'itérations du test de Miller-Rabin.

    Sortie :
        bool - True si le nombre est probablement premier, False sinon.
    """

    # Vérification des cas de base
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Décomposition de n-1 en (2^r)*s
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    # Test de Miller-Rabin
    for _ in xrange(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in xrange(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Calcul de la taille en octets d'un nombre
def bit_size(a:int) -> int:
    """
    Calcule la taille en octets d'un nombre.

    Entrée :
        a : int - Le nombre dont on souhaite calculer la taille.

    Sortie :
        int - La taille en octets du nombre.
    """
    return int((a.bit_length()+7)//8)

# Conversion d'un entier en tableau d'octets
def int_to_bytes(a):
    """
    Convertit un entier en tableau d'octets.

    Entrée :
        a : int - L'entier à convertir.

    Sortie :
        bytes - Le tableau d'octets représentant l'entier.
    """
    return a.to_bytes(bit_size(a),'big')

# Algorithme d'Euclide étendu pour trouver le PGCD et les coefficients de Bézout
def extended_gcd(a, b):
    """
    Algorithme d'Euclide étendu pour trouver le PGCD et les coefficients de Bézout.

    Entrées :
        a : int - Le premier entier.
        b : int - Le second entier.

    Sortie :
        Tuple[int, int, int] - Le triplet (pgcd, x, y) où pgcd est le PGCD de a et b, et x et y sont les coefficients de Bézout.
    """
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

# Entrée : Nombre premier en hexadécimal
a = "7b54ecaba13bdecee2dd13b19c8e1e1805cbdc532f961d40544799bdac86954b5f880d180c29ae8b71fc9752ed373222fe9549ecaec60d7cc1b922e53358ab314e67218343c627cdc5c1fa67a73d472b000b66b4a0f6b65f011d4fc52296aaf77cb9302817b809cb7055e7edef5c8549f26b3f3efd3fe2e4b8fae46f1a260a82292f6b686a2f4fb68925ca932a1d00a29cada81a1769fcd0001696e004163f7f133bcd0fb27155aa822e24e6be6b05e4dd508f66ccf28ca32464f232013d524cf7a8823dea929f0319e9c43a82d23c12e948295f3344ee376b6fe478ac44b6b868d3b030d9a65dafc872044ba9cec4e4ca67dd41f56566515364f1b9b1a28cd"
# Conversion en entier
a = int(a,16)

# Nombre premier a + 2^1950
b = a + 2**1950

# Nombre premier en hexadécimal
q = "6d7bd751a506215c0646d994136af9be03b7d7e74a6b523ff8fba4cbf861fcb3fcc5b4ba1d7a77655774c65dd1bb0603"
# Conversion en entier
q = int(q,16)

# Constante arbitraire
c = 20000

# Calcul de la taille en bits de b
len_b = bit_size(b)

# Calcul de la borne supérieure de Q'
maxQprim = (b-a)//(c*pow(len_b,2))

# Calcul de la taille en bits de maxQprim
sizeQprim = bit_size(maxQprim)

# Initialisation de Q' avec 2*q
Qprim = 2*q 

# Liste des diviseurs
diviseur = [2]    

# Construction de Q'
while(sizeQprim != bit_size(Qprim)):
    
    # Génération d'un nombre premier pi aléatoire
    pi = random.randrange(2,min(q-1, pow(2,8*(sizeQprim-bit_size(Qprim)))))

    # Vérification de la primalité de pi
    if(miller_rabin(pi,10) == False):
        continue

    # Mise à jour de Qprim
    Qprim *= pi
    diviseur.append(pi)

# Division de a et b par Q'
ak = a // Qprim
bk = b // Qprim

# Recherche d'un nombre premier pk
while(True):
    pk = random.randrange(ak,bk)

    # Vérification de la primalité de pk
    if(miller_rabin(pk,2) == False):
        continue
    
    # Vérification si Q' * pk + 1 est premier
    if(miller_rabin(Qprim*pk + 1,2) == False):
        continue

    # Calcul de Q
    Q = Qprim*pk
    diviseur.append(pk)

    # Calcul de p
    p = Q + 1
    print('p = ',p)
    break

# Nombre d'essais pour trouver g
n_try = 100

# Recherche d'un générateur g
for _ in range(n_try):
    g = random.randrange(2,p-1)
    test = True
    for pi in diviseur:
        if (pow(g,Q//pi,p) == 1):
            test = False
            break

    if test:
        print('g = ',g)
        break

# Affichage de (p-1)//q
print('(p-1)//q = ',str(diviseur)[1:-1])
