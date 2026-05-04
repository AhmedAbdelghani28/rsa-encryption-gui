"""RSA key-pair generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
from .prime import generate_prime


def _extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Returns (gcd, x, y) such that a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    g, x, y = _extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def _mod_inverse(e: int, phi: int) -> int:
    g, x, _ = _extended_gcd(e % phi, phi)
    if g != 1:
        raise ValueError("e and phi(n) are not coprime — no modular inverse exists")
    return x % phi


@dataclass(frozen=True)
class RSAKeyPair:
    p: int
    q: int
    n: int
    phi_n: int
    e: int
    d: int

    @property
    def public_key(self) -> Tuple[int, int]:
        return (self.e, self.n)

    @property
    def private_key(self) -> Tuple[int, int]:
        return (self.d, self.n)

    @property
    def bit_length(self) -> int:
        return self.n.bit_length()

    def summary(self) -> dict[str, str]:
        return {
            "Bit length": str(self.bit_length),
            "p": str(self.p),
            "q": str(self.q),
            "n  (modulus)": str(self.n),
            "φ(n)": str(self.phi_n),
            "e  (public exponent)": str(self.e),
            "d  (private exponent)": str(self.d),
        }


# Standard public exponent — universally used in practice (Fermat prime F4)
_PUBLIC_EXPONENT = 65537


def generate_keypair(bit_length: int = 1024) -> RSAKeyPair:
    """Generate an RSA key pair of the requested modulus bit-length."""
    if bit_length < 16:
        raise ValueError("bit_length must be at least 16")

    half = bit_length // 2
    while True:
        p = generate_prime(half)
        q = generate_prime(half)
        if p == q:
            continue

        n = p * q
        phi_n = (p - 1) * (q - 1)

        e = _PUBLIC_EXPONENT
        if phi_n % e == 0:
            continue  # very rare; just regenerate

        d = _mod_inverse(e, phi_n)
        return RSAKeyPair(p=p, q=q, n=n, phi_n=phi_n, e=e, d=d)
