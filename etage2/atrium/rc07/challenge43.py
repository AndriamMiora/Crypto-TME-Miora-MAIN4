import math

def fermat_factorization(N):
    a = math.isqrt(N) + 1
    b2 = a * a - N
    while not math.isqrt(b2) ** 2 == b2:
        a += 1
        b2 = a * a - N
    p = a + math.isqrt(b2)
    q = a - math.isqrt(b2)
    return p, q

N = 0x00aa7ab308b5c0d713b5d6810b22d9564cbfc2b3b75d9f7ae5bb9243b0f5c98d83630e32252ddf7d675d892409ac5e9b8d6d42a17c2d1babb6023037696955c30a96693a327c509f00da37e61817e9af617827f5b8fa378e29aa55648cbac8d1b9d7c36e1426fab85a5140b43f417ddfc0af1d30c83237dd40b4bd608d97d2c6cf107163ef3c2c2d8a26a42b0dc032daaaac9a94f8b68a1ffecd5da81fe7a49fa71101819a6c2a0118ddc84403f646f080785b2baad93d0436652b7bc721f1b641c513b9f6beb83bd2a2ecf96384e7e5e822e5c9e9c99a1637d8d32d57ff18940cf31b530fc8a0476c6aa31a2591aa0c08201cad29fa8da74

p, q = fermat_factorization(N)

d = 0xa71fad2e2755eac0304f9474ba090412d8a6f0f744daaa5b9cba65847144a91eae50938aea7552e3c3e08ce5f440fe9f6118471ece1368e4d9d90db547e5e06d496fe11202c4d5c5a4bc204a7fe9d93e395a01561c13e183008ebddcc6958da981d830328f4f5c160bdb490253caa825b2b95110266a3f56bd63c50c186af67a5a8a3662fa46eb778df225e183775ddd5f986907de5f27fd6e3c419bb9ac05c9649f230267b912096f47a2f114e5af82a510b43f0fbbf0804818df728a919c9876e1ed23768764c534148162e993da0fd749e7c9cff87958031135099632ce64776afdc955e85a36d43cdd1779079e31b9a2664e4cb9b1e4caa4a2d600418d21

phi = (p - 1) * (q - 1)
e = pow(d, -1, phi)

private_key = RSA.construct((N, e, d, p, q))
private_key_pem = private_key.export_key(format='PEM')

with open("private_43key.pem", "wb") as f:
    f.write(private_key_pem)

print("Clé privée générée et enregistrée dans private_43key.pem")
