import customtkinter as ctk
from tkinter import messagebox
import random

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def is_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(k):
        a = 2 + random.randint(0, n - 4)
        x = mod_exp(a, d, n)
        if x == 1 or x == n - 1:
            continue
        prime = False
        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                prime = True
                break
        if not prime:
            return False
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    m0, x0, x1 = phi, 0, 1
    while e > 1:
        q = e // phi
        phi, e = e % phi, phi
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_prime(bit_length):
    while True:
        prime = random.getrandbits(bit_length)
        if is_prime(prime):
            return prime

def encrypt(message, e, n):
    return mod_exp(message, e, n)

def decrypt(encrypted_message, d, n):
    return mod_exp(encrypted_message, d, n)

def encrypt_message():
    try:
        message = int(entry_message.get())
        encrypted_message = encrypt(message, e, n)
        label_encrypted.configure(text=f"Encrypted message: {encrypted_message}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer message")

def decrypt_message():
    try:
        encrypted_message = int(entry_encrypted.get())
        decrypted_message = decrypt(encrypted_message, d, n)
        label_decrypted.configure(text=f"Decrypted message: {decrypted_message}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer encrypted message")

random.seed()
p = generate_prime(10)
q = generate_prime(10)
n = p * q
phi = (p - 1) * (q - 1)
e = 2
while gcd(e, phi) != 1:
    e += 1
d = mod_inverse(e, phi)

# Initialize the application
app = ctk.CTk()

# Set the theme (optional)
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

app.title("RSA Encryption and Decryption")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label_message = ctk.CTkLabel(master=frame, text="Enter message:")
label_message.grid(row=0, column=0, pady=10, padx=10)
entry_message = ctk.CTkEntry(master=frame)
entry_message.grid(row=0, column=1, pady=10, padx=10)
button_encrypt = ctk.CTkButton(master=frame, text="Encrypt", command=encrypt_message)
button_encrypt.grid(row=0, column=2, pady=10, padx=10)
label_encrypted = ctk.CTkLabel(master=frame, text="")
label_encrypted.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

label_encrypted_entry = ctk.CTkLabel(master=frame, text="Enter encrypted message:")
label_encrypted_entry.grid(row=2, column=0, pady=10, padx=10)
entry_encrypted = ctk.CTkEntry(master=frame)
entry_encrypted.grid(row=2, column=1, pady=10, padx=10)
button_decrypt = ctk.CTkButton(master=frame, text="Decrypt", command=decrypt_message)
button_decrypt.grid(row=2, column=2, pady=10, padx=10)
label_decrypted = ctk.CTkLabel(master=frame, text="")
label_decrypted.grid(row=3, column=0, columnspan=3, pady=10, padx=10)

app.mainloop()
