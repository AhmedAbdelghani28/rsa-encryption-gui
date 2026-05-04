import pytest
from src.crypto.prime import is_prime, generate_prime


KNOWN_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 97, 1009, 7919]
KNOWN_COMPOSITES = [0, 1, 4, 6, 8, 9, 15, 100, 1001]


def test_known_primes():
    for p in KNOWN_PRIMES:
        assert is_prime(p), f"{p} should be prime"


def test_known_composites():
    for c in KNOWN_COMPOSITES:
        assert not is_prime(c), f"{c} should be composite"


@pytest.mark.parametrize("bits", [16, 32, 64, 128])
def test_generate_prime_is_prime(bits):
    p = generate_prime(bits)
    assert is_prime(p)


@pytest.mark.parametrize("bits", [16, 32, 64, 128])
def test_generate_prime_bit_length(bits):
    p = generate_prime(bits)
    assert p.bit_length() == bits
