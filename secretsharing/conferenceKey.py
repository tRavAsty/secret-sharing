
from polynomials import random_polynomial, mod_inverse, Polynomial, modular_lagrange_interpolation, share_Polynomial
from primes import get_modulus, eular, safePrime
from utilitybelt import secure_randint as randint

def share_generation(k, m, n, l = None,pub_inf = None):
    #k degree, m members, n identities, n >=m, modulus is 2l bits long
    if l == None:
        s = safePrime()
    else:
        s = safePrime(l)

    mod = s.get_modulus()
    A = random_polynomial(k, randint(0, mod-1), mod) #the second parameter means secret
    #A = [985, 254, 1957, 312]
    #print "f_i" + str(A)
    P = Polynomial(A, mod, n)
    '''
    for i in range(1,n+1):
        print P.value(i)
    '''
    S = []
    if pub_inf == None:
        pub_inf = range(1,n+1)
    inverseOfnminus1 = mod_inverse(n-1, s.get_eular())
    for i in range(n):
        c = s.sqaure_and_multiply(P.value(pub_inf[i]), inverseOfnminus1)
        S.append(share_Polynomial(P.get_mul_value(c),mod,n, i))
    return A, S

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



