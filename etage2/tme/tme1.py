import random
from sympy import isprime

def generate_prime(q, a, b):
    """
    Génère un nombre premier p tel que p-1 soit un multiple de q et a <= p < b.
    On tente de trouver un tel nombre premier en augmentant le nombre d'essais.
    """
    lower_bound = (a - 1) // q + 1
    upper_bound = (b - 1) // q

    for _ in range(5000):  # Augmentation du nombre d'essais pour une meilleure chance de succès
        candidate = q * random.randint(lower_bound, upper_bound) + 1
        if isprime(candidate):
            return candidate
    raise ValueError("Impossible de trouver un nombre premier dans l'intervalle donné après 5000 essais.")

def find_generator(p, q):
    """
    Trouve un générateur g d'ordre q modulo p, avec les contraintes que p est premier
    et (p-1) % q == 0. On teste des candidats aléatoires jusqu'à en trouver un valide.
    """
    if not (isprime(p) and (p - 1) % q == 0):
        raise ValueError("Les conditions sur p et q ne sont pas respectées.")
    for _ in range(100):  # Tentatives limitées pour trouver un générateur
        candidate = random.randint(2, p - 2)
        g = pow(candidate, (p - 1) // q, p)
        if g > 1:
            return g
    raise ValueError("Impossible de trouver un générateur après 100 essais.")

# Conversion des paramètres hexadécimaux en entiers
a_hex = "5fe1cff6a6985c9017ed7810cb65ef1d13e86c79dac73e3f388f84f74408f8558fce6136bd58b55d2c358010f445966f58ae153bed16606081abf172663ce2b44409f4e07eaaf6d6e7fa6038eb187003c18b078674524d637a03f29dd7ad0d594df554ce72b2584a5f959cf3eb573369f5007200f3f4d77099a900f2bf47bff1080be802922f484c38e2382e501c19e30c89f34df49cd7043982a69602b5bb06b5d950c5d69e704d40e019037ec6299a46167727a67eeb84aa717f2d9f9e03113e65855468cbe796ccc2bd32db9dbd6b0722923b06787133801f1a44e72a897cbb513fe7174d1fd3559eb36f75e66a00eff21d43fc089b7fc99fbcf21e0ff8f7"
a = int(a_hex, 16)
q_hex = "81712b30190a697df542e3801f265309dd2754d4d67852254706b92f5c954869"
q = int(q_hex, 16)
b = a + 2**1950

try:
    p = generate_prime(q, a, b)
    print(f"Nombre premier p: {p} où p-1 est un multiple de {q}")
    g = find_generator(p, q)
    print(f"Le générateur g est: {g}")
except ValueError as e:
    print(e)
