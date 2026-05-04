"""
RSA encryption / decryption with text support.

Text is split into fixed-size blocks so that each block integer fits
inside the modulus.  Each block is prefixed with a 0x01 sentinel byte
so that leading-zero blocks round-trip correctly.
"""

from __future__ import annotations


def encrypt(message: int, e: int, n: int) -> int:
    if not (0 <= message < n):
        raise ValueError(f"Message must be in range [0, n).  Got {message}, n={n}")
    return pow(message, e, n)


def decrypt(ciphertext: int, d: int, n: int) -> int:
    if not (0 <= ciphertext < n):
        raise ValueError(f"Ciphertext must be in range [0, n).  Got {ciphertext}, n={n}")
    return pow(ciphertext, d, n)


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _block_size(n: int) -> int:
    """Maximum plaintext bytes per block (one byte margin under the modulus)."""
    return (n.bit_length() // 8) - 1


def encrypt_text(text: str, e: int, n: int) -> list[int]:
    """Encrypt a UTF-8 string, returning a list of ciphertext integers."""
    raw = text.encode("utf-8")
    bs = _block_size(n)
    if bs < 1:
        raise ValueError("Modulus is too small to encrypt text")

    blocks: list[int] = []
    for i in range(0, len(raw), bs):
        chunk = raw[i : i + bs]
        # 0x01 sentinel prefix ensures leading zeros are preserved
        m = int.from_bytes(b"\x01" + chunk, "big")
        blocks.append(encrypt(m, e, n))
    return blocks


def decrypt_text(ciphertext_blocks: list[int], d: int, n: int) -> str:
    """Decrypt a list of ciphertext integers back to a UTF-8 string."""
    chunks: list[bytes] = []
    for c in ciphertext_blocks:
        m = decrypt(c, d, n)
        raw = m.to_bytes((m.bit_length() + 7) // 8, "big")
        # Strip the 0x01 sentinel byte
        if raw and raw[0] == 0x01:
            raw = raw[1:]
        chunks.append(raw)
    return b"".join(chunks).decode("utf-8")
