# TME #4 : somme de carrés
# ========================
                                                    
def mods(a, n):
    """ Normalise a pour être entre -n/2 et n/2. """
    a = a % n
    if 2 * a > n:
        a -= n
    return a


def powmods(a, r, n):
    """ Réalise l'exponentiation modulaire avec normalisation. """
    out = 1
    while r > 0:
        if (r % 2) == 1:
            r -= 1
            out = mods(out * a, n)
        r //= 2
        a = mods(a * a, n)
    return out


def quos(a, n):
    """ Calcule le quotient de la division de a par n, ajusté par mods. """
    return (a - mods(a, n)) // n


def grem(w, z):
    """ Calcul du reste dans les entiers gaussiens lors de la division de w par z. """
    (w0, w1) = w
    (z0, z1) = z
    n = z0**2 + z1**2
    if n == 0:
        raise ValueError("Division par zéro")
    u0 = quos(w0 * z0 + w1 * z1, n)
    u1 = quos(w1 * z0 - w0 * z1, n)
    return (w0 - z0 * u0 + z1 * u1, w1 - z0 * u1 - z1 * u0)


def ggcd(w, z):
    """ Calcule le plus grand diviseur commun utilisant les entiers gaussiens. """
    while z != (0, 0):
        w, z = z, grem(w, z)
    return w


def root4(p):
    """ Calcule la racine 4-ième de 1 modulo p."""
    if p <= 1:
        return "trop petit"
    if (p % 4) != 1:
        return "pas congruent à 1"
    k = p//4
    j = 2
    while True:
        a = powmods(j, k, p)
        b = mods(a * a, p)
        if b == -1:
            return a
        if b != 1:
            return "pas premier"
        j += 1


def sq2(p):
    """ Décompose un nombre premier p en une somme de deux carrés. """
    a = root4(p)
    return ggcd((p, 0), (a, 1))


def main():
    p_hex = "c1a1a26a2b3c10905d7fa2a026dcbd4bf782ff37b16d530db9e3970361fe43763217448bf53c5808286c1f9f3955f0719b68473b6bdc1b0aa3cdf3bb5ba651fb4e97b1331e9a2c053a8a9974667b24678d6a84f445a80069eac60a39ec599a278ef8b6adf747623e93e13675ed6f27bfe6991f24d1812463f473a1647d0fe631"
    p_int = int(p_hex, 16)
    a, b = sq2(p_int)
    print(f"a = \n{a} \nb = \n{b}\n")


if __name__ == "__main__":
    main()