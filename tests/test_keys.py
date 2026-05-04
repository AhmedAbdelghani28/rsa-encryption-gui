import pytest
from src.crypto.keys import generate_keypair
from src.crypto.prime import is_prime


@pytest.mark.parametrize("bits", [64, 128, 256])
def test_key_components_valid(bits):
    kp = generate_keypair(bits)
    assert is_prime(kp.p)
    assert is_prime(kp.q)
    assert kp.p != kp.q
    assert kp.n == kp.p * kp.q
    assert kp.phi_n == (kp.p - 1) * (kp.q - 1)
    assert kp.e == 65537
    # Verify d is the correct inverse: e*d ≡ 1 (mod phi_n)
    assert (kp.e * kp.d) % kp.phi_n == 1


def test_public_private_key_tuples():
    kp = generate_keypair(64)
    e, n = kp.public_key
    d, n2 = kp.private_key
    assert e == kp.e
    assert d == kp.d
    assert n == n2 == kp.n


def test_bit_length():
    kp = generate_keypair(128)
    assert 127 <= kp.bit_length <= 128
