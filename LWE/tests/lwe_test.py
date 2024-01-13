import unittest

from LWE.LWE_GSW import LWEGSW
from tests_utils import multiple_generic_tests, lwe_sample

n = 5
q = 4096
error_distribution = lambda: lwe_sample(n, q)
nb_tests = 100


def test_encrypt_decrypt(scheme, pk, sk, bit) -> bool:
    ct = scheme.encrypt(pk, bit)
    return scheme.decrypt(sk, ct)


def test_single_binary_gate(scheme, pk, sk, bit1, bit2, gate) -> bool:
    ct1 = scheme.encrypt(pk, bit1)
    ct2 = scheme.encrypt(pk, bit2)
    ct_gate = scheme.evaluate([[gate]], [ct1, ct2])[0]
    return scheme.decrypt(sk, ct_gate)


def test_not_gate(scheme, pk, sk, bit) -> bool:
    ct = scheme.encrypt(pk, bit)
    ct_gate = scheme.evaluate([["not"]], [ct])[0]
    return scheme.decrypt(sk, ct_gate)


class TestLWE(unittest.TestCase):

    def test_encrypt_decrypt_0(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_encrypt_decrypt, (scheme, pk, sk, False), False, nb_tests,
                               f"GSW-LWE Encrypt and decrypt 0 (n: {n}, q: {q})")

    def test_encrypt_decrypt_1(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_encrypt_decrypt, (scheme, pk, sk, True), True, nb_tests,
                               f"GSW-LWE Encrypt and decrypt 1 (n: {n}, q: {q})")

    def test_nand_true(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_single_binary_gate, (scheme, pk, sk, True, False, "nand"), True, nb_tests,
                               f"GSW-LWE Test: NAND 1 0 (n: {n}, q: {q})")

    def test_nand_false(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_single_binary_gate, (scheme, pk, sk, True, True, "nand"), False, nb_tests,
                               f"GSW-LWE Test: NAND 1 1 (n: {n}, q: {q})")

    def test_and_true(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_single_binary_gate, (scheme, pk, sk, True, False, "and"), False, nb_tests,
                               f"GSW-LWE Test: AND 1 0 (n: {n}, q: {q})")

    def test_and_false(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_single_binary_gate, (scheme, pk, sk, True, True, "and"), True, nb_tests,
                               f"GSW-LWE Test: AND 1 1 (n: {n}, q: {q})")

    def test_or_true(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_single_binary_gate, (scheme, pk, sk, True, False, "or"), True, nb_tests,
                               f"GSW-LWE Test: OR 1 0 (n: {n}, q: {q})")

    def test_or_false(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_single_binary_gate, (scheme, pk, sk, False, False, "or"), False, nb_tests,
                               f"GSW-LWE Test: OR 0 0 (n: {n}, q: {q})")

    def test_xor_true(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_single_binary_gate, (scheme, pk, sk, True, False, "xor"), True, nb_tests,
                               f"GSW-LWE Test: XOR 1 0 (n: {n}, q: {q})")

    def test_xor_false(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_single_binary_gate, (scheme, pk, sk, True, True, "xor"), False, nb_tests,
                               f"GSW-LWE Test: XOR 1 1 (n: {n}, q: {q})")

    def test_not_gate_true(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_not_gate, (scheme, pk, sk, False), True, nb_tests, f"GSW-LWE Test: NOT 0 (n: {n}, q: {q})")

    def test_not_gate_false(self):
        scheme = LWEGSW()
        pk, sk = scheme.keygen((q, n, error_distribution))
        multiple_generic_tests(test_not_gate, (scheme, pk, sk, False), True, nb_tests, f"GSW-LWE Test: NOT 1 (n: {n}, q: {q})")
