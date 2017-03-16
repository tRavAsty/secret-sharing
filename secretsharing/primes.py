# -*- coding: utf-8 -*-
"""
    Secret Sharing
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""
import gensafeprime

def calculate_mersenne_primes():
    """ Returns all the mersenne primes with less than 500 digits.
        All primes:
        3, 7, 31, 127, 8191, 131071, 524287, 2147483647L, 2305843009213693951L,
        618970019642690137449562111L, 162259276829213363391578010288127L,
        170141183460469231731687303715884105727L,
        68647976601306097149...12574028291115057151L, (157 digits)
        53113799281676709868...70835393219031728127L, (183 digits)
        10407932194664399081...20710555703168729087L, (386 digits)
    """
    mersenne_prime_exponents = [
        2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279
    ]
    primes = []
    for exp in mersenne_prime_exponents:
        prime = 1
        for i in range(exp):
            prime *= 2
        prime -= 1
        primes.append(prime)
    return primes

SMALLEST_257BIT_PRIME = (2**256 + 297)
SMALLEST_321BIT_PRIME = (2**320 + 27)
SMALLEST_385BIT_PRIME = (2**384 + 231)
STANDARD_PRIMES = calculate_mersenne_primes() + [
    SMALLEST_257BIT_PRIME, SMALLEST_321BIT_PRIME, SMALLEST_385BIT_PRIME
]
STANDARD_PRIMES.sort()


def get_large_enough_prime(batch):
    """ Returns a prime number that is greater all the numbers in the batch.
    """
    # build a list of primes
    primes = STANDARD_PRIMES
    # find a prime that is greater than all the numbers in the batch
    for prime in primes:
        numbers_greater_than_prime = [i for i in batch if i > prime]
        if len(numbers_greater_than_prime) == 0:
            return prime
    return None

class safePrime(object):

    def __init__(self,l = 512):
        if l <= 0:
            print "error"
            raise Exception()
        elif l<16:
            self._p = 47
            self._q = 59
            self.n = self._p*self._q
            self._phi = (self._p-1)*(self._q-1)
        else:
            self._p = gensafeprime.generate(l)
            self._q = gensafeprime.generate(l)
            self.n = self._p*self._q
            self._phi = (self._q-1) * (self._p-1)

    def get_modulus(self):
        return self.n# hard code, need to be fixed

    def get_eular(self):
        return self._phi

    def sqaure_and_multiply(self, base, index):
        m = bin(index)
        m = m[2:]
        if m[len(m)-1] == '1':
            B = base
        else:
            B = 1
        A = base
        for i in range(len(m)-2,-1,-1):
            A = A*A % self.n
            if m[i] == '1':
                B = B*A % self.n
        return B

def get_modulus():
    return 2773# hard code, need to be fixed,need to find two safe prime, here is result of 47*59

def eular(x):
    return 2668