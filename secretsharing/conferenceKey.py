
from polynomials import random_polynomial, mod_inverse, Polynomial, modular_lagrange_interpolation
from primes import get_modulus, eular
from utilitybelt import secure_randint as randint

def share_generation(k, m, n, pub_inf = None):
    mod = get_modulus()
    A = random_polynomial(k,randint(0, mod-1),mod)
    A = [985, 254, 1957, 312]
    print "f_i" + str(A)
    P = Polynomial(A,mod,n)
    for i in range(1,n+1):
        print P.value(i)
    S = []
    if pub_inf == None:
        pub_inf = range(1,n+1)
    inverseOfnminus1 = mod_inverse(n-1,eular(mod))
    for i in range(n):
        c = (P.value(pub_inf[i]) ** inverseOfnminus1) % mod
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


Shareholders = share_generation(3,4,4)
print Shareholders
v = []
for s in Shareholders:
    v.append(s.secret_value())
print "secret values",
print v
r = range(4)
for i in r:
    print "conference key of shareohlder "+ str(i) + " is " + str(Shareholders[0].conference_key_construct(r))
print(secret_reconstruct(r, v, 4, 3,get_modulus()))
