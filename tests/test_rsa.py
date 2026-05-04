import pytest
from src.crypto.keys import generate_keypair
from src.crypto.rsa import encrypt, decrypt, encrypt_text, decrypt_text


@pytest.fixture(scope="module")
def keypair():
    return generate_keypair(256)


def test_integer_roundtrip(keypair):
    e, n = keypair.public_key
    d, _ = keypair.private_key
    for m in [0, 1, 42, 1337, n - 1]:
        assert decrypt(encrypt(m, e, n), d, n) == m


def test_text_roundtrip(keypair):
    e, n = keypair.public_key
    d, _ = keypair.private_key
    for text in ["Hello, World!", "RSA rocks 🔐", "a" * 100, "abc\ndef\n"]:
        blocks = encrypt_text(text, e, n)
        assert decrypt_text(blocks, d, n) == text


def test_encrypt_out_of_range(keypair):
    e, n = keypair.public_key
    with pytest.raises(ValueError):
        encrypt(n, e, n)
    with pytest.raises(ValueError):
        encrypt(-1, e, n)


def test_wrong_key_does_not_recover_plaintext():
    kp1 = generate_keypair(256)
    kp2 = generate_keypair(256)
    e1, n1 = kp1.public_key
    d2, n2 = kp2.private_key
    # Encrypt "hello" with kp1; decrypting with kp2 should NOT give "hello"
    blocks = encrypt_text("hello", e1, n1)
    try:
        # May raise ValueError (block >= n2) or UnicodeDecodeError (bad bytes)
        result = decrypt_text(blocks, d2, n2)
        assert result != "hello", "Wrong private key should not recover the plaintext"
    except (ValueError, UnicodeDecodeError):
        pass  # expected — wrong key produced undecodable garbage
