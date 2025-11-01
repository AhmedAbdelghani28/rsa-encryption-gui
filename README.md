# 🔐 RSA Encryption & Decryption GUI

An educational **RSA Encryption & Decryption** app built using **Python** and **CustomTkinter**.  
This project demonstrates how public-key cryptography works — from prime generation to key creation, encryption, and decryption — all inside a simple, modern GUI.

---

## 🧠 Overview

This app shows the basics of the **RSA algorithm**, one of the most famous encryption methods used to secure digital communication.

You can:
- 🔢 Enter an integer message  
- 🔒 Encrypt it using RSA  
- 🔓 Decrypt it back to the original message  
- 🖥️ Enjoy a modern dark-mode interface powered by CustomTkinter

---

## ⚙️ How It Works

1. **Prime Generation**
   - Randomly generates two prime numbers `p` and `q`.
2. **Key Computation**
   - Calculates:
     - `n = p * q`
     - `φ(n) = (p - 1) * (q - 1)`
     - Public key exponent `e`
     - Private key exponent `d`
3. **Encryption**
   - Formula: `C = M^e mod n`
4. **Decryption**
   - Formula: `M = C^d mod n`

---

## 🖼️ GUI Features

| Feature | Description |
|----------|--------------|
| 🧩 Input Fields | Enter a plaintext message or an encrypted number |
| 🔐 Encrypt Button | Encrypts your input using RSA |
| 🔓 Decrypt Button | Decrypts the encrypted value |
| 🌙 Dark Theme | Clean and modern CustomTkinter interface |

---


---

## 🛠️ Technologies Used

- 🐍 **Python 3**
- 🎨 **CustomTkinter**
- 📚 **Random** & **Math-based RSA logic**

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/AhmedAbdelghani28/rsa-encryption-gui.git
   cd rsa-encryption-gui

