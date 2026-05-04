# RSA Encryption & Decryption — Desktop GUI

A fully-featured RSA cryptography tool built in Python. Implements the complete RSA algorithm from scratch — prime generation, key derivation, and block-based text encryption — with a modern PyQt6 GUI.

---

## Features

- **RSA from scratch** — no `cryptography` or `rsa` library; every mathematical operation is implemented directly
- **Miller-Rabin primality test** using `secrets` (CSPRNG) for cryptographic-quality randomness
- **Extended Euclidean Algorithm** for modular inverse computation
- **Configurable key sizes** — 512, 1024, or 2048-bit moduli
- **Text encryption** — encrypts arbitrary UTF-8 strings via block encoding (not just integers)
- **Non-blocking UI** — key generation runs on a background thread; the interface stays responsive
- **19 unit tests** covering primes, key generation, integer round-trips, and text round-trips

---

## Project Structure

```
rsa-encryption-gui/
├── src/
│   ├── crypto/
│   │   ├── prime.py      # Miller-Rabin primality test + prime generation
│   │   ├── keys.py       # RSA key-pair generation (Extended GCD, dataclass)
│   │   └── rsa.py        # Encrypt / decrypt (integers and UTF-8 text)
│   └── gui/
│       ├── app.py                     # Main PyQt6 window, toolbar, tabs
│       └── components/
│           ├── crypto_panel.py        # Encrypt / Decrypt tab
│           └── key_panel.py          # Key Details tab
├── tests/
│   ├── test_prime.py
│   ├── test_keys.py
│   └── test_rsa.py
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## How RSA Works

| Step | Operation |
|------|-----------|
| 1 | Generate two large primes **p** and **q** |
| 2 | Compute **n = p·q** (the modulus) |
| 3 | Compute **φ(n) = (p−1)(q−1)** (Euler's totient) |
| 4 | Choose **e = 65537** (Fermat prime — standard public exponent) |
| 5 | Compute **d = e⁻¹ mod φ(n)** via Extended Euclidean Algorithm |
| 6 | **Encrypt:** C = Mᵉ mod n &nbsp; (public key) |
| 7 | **Decrypt:** M = Cᵈ mod n &nbsp; (private key) |

---

## Quick Start (Local)

```bash
# Clone
git clone https://github.com/AhmedAbdelghani28/rsa-encryption-gui.git
cd rsa-encryption-gui

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py

# Run tests
pytest tests/ -v
```

---

## Docker

The app ships with a `Dockerfile` and `docker-compose.yml` so you can run it without installing any Python dependencies locally. Because it is a desktop GUI, the container forwards its display to your host screen via X11.

### Linux

```bash
# Allow the container to connect to your X server
xhost +local:docker

# Build and run
docker compose up --build

# Revoke access when done
xhost -local:docker
```

### macOS

1. Install [XQuartz](https://www.xquartz.org/) and open it.
2. In XQuartz → Preferences → Security, enable **"Allow connections from network clients"**.
3. Restart XQuartz, then run:

```bash
xhost +localhost

DISPLAY=host.docker.internal:0 docker compose up --build
```

### Windows

1. Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) and launch it with **"Disable access control"** checked.
2. Find your host IP (e.g. `ipconfig` → IPv4 address).
3. Run:

```powershell
$env:DISPLAY="<your-host-ip>:0"
docker compose up --build
```

### Run tests inside Docker

```bash
docker compose run --rm rsa-gui pytest tests/ -v
```

---

## Technologies

| | |
|--|--|
| **Language** | Python 3.11 |
| **GUI** | PyQt6 |
| **Cryptography** | Pure Python (no third-party crypto library) |
| **Randomness** | `secrets` module (CSPRNG) |
| **Tests** | pytest |
| **Container** | Docker / Docker Compose |
