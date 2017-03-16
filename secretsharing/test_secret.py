import unittest
from secretsharing.conferenceKey import *

class TestPrimes(unittest.TestCase):
    def test_square_and_multiply(self):
        s = safePrime(4)
        self.assertEquals(s.sqaure_and_multiply(3, 2), 9)
        self.assertEquals(s.sqaure_and_multiply(3,s.get_eular()+1), 3)

class TestConferenceKey(unittest.TestCase):
    def test_secret(self):
        A, Shareholders = share_generation(3, 4, 4, 512)
        self.assertEquals(len(Shareholders), 4)

        for s in Shareholders:
            self.assertEquals(len(s.coefficient), 4)
        v = []
        for s in Shareholders:
            v.append(s.secret_value())

        r = range(4)
        for i in range(3):
            self.assertEquals(Shareholders[i].conference_key_construct(r), Shareholders[i+1].conference_key_construct(r))
        mod = Shareholders[0].get_modulus()
        self.assertEquals(secret_reconstruct(r, v, 4, 3, mod), A[0]**4 % mod)

if __name__ == '__main__':
    unittest.main()
