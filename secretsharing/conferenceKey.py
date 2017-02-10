
from polynomials import random_polynomial, mod_inverse, Polynomial, modular_lagrange_interpolation
from primes import get_modulus
from utilitybelt import secure_randint as randint

def share_generation(k, m, n, pub_inf = None):
    mod = get_modulus()
    A = random_polynomial(k,randint(0, mod-1),mod)
    P = Polynomial(A,mod,n)
    S = []
    if pub_inf == None:
        pub_inf = range(1,n+1)
    for i in range(n):
        c = mod_inverse(P.value(pub_inf[i]), mod)
        S.append(Polynomial(P.get_mul_value(c),mod,n))
    return S

def secret_reconstruct(shareholders, values, n,k, modulus, pub_inf = None):
    if pub_inf == None:
        pub_inf = range(1, n+1)
    if len(shareholders) <= k:
        return "error"#error handling, tbc
    if len(shareholders) != len(values):
        return "error"
    pairs = []
    for i in range(len(shareholders)):
        pair = []
        pair.append(pub_inf[shareholders[i]])
        pair.append(values[i])
        pairs.append(pair)
    secret_key = modular_lagrange_interpolation(0,pairs,modulus)
    return secret_key


Shareholders = share_generation(7,4,8)
v = []
for s in Shareholders:
    v.append(s.secret_value())
r = range(8)
print(secret_reconstruct(r,v,8,7,get_modulus()))
