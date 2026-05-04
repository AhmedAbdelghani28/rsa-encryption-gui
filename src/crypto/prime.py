"""
Prime number utilities for RSA key generation.

Uses the Miller-Rabin probabilistic primality test, which is the
industry-standard approach used in cryptographic libraries.
"""

from __future__ import annotations

import secrets
from typing import Optional

# Witness counts recommended by FIPS 186-5 for each bit-length range
_MILLER_RABIN_ROUNDS: dict = {
    (0, 512): 40,
    (512, 1024): 20,
    (1024, 2048): 10,
    (2048, 4096): 5,
}


def _miller_rabin_rounds(bit_length: int) -> int:
    for (lo, hi), rounds in _MILLER_RABIN_ROUNDS.items():
        if lo <= bit_length < hi:
            return rounds
    return 4


def is_prime(n: int, rounds: Optional[int] = None) -> bool:
    """Miller-Rabin probabilistic primality test.

    Returns False if n is definitely composite, True if probably prime.
    Error probability is at most 4^(-rounds).
    """
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False

    # Write n-1 as 2^r * d with d odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    k = rounds if rounds is not None else _miller_rabin_rounds(n.bit_length())
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # random in [2, n-2]
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bit_length: int) -> int:
    """Generate a random prime of exactly *bit_length* bits."""
    if bit_length < 2:
        raise ValueError("bit_length must be >= 2")
    while True:
        # Force the top two bits to 1 so the product p*q is exactly 2*bit_length bits
        candidate = secrets.randbits(bit_length) | (1 << (bit_length - 1)) | 1
        if is_prime(candidate):
            return candidate
