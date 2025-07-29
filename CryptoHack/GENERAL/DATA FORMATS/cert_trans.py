# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.asymmetric import rsa
# import binascii
# -----------------
from Crypto.PublicKey import RSA
from sympy import factorint

with open("transparency.pem", "r") as f:
    key = RSA.import_key(f.read())

n = key.n
e = key.e

print(f"n = {n}")
print(f"e = {e}")
ciphertext = 123456789  # contoh, harus kamu ganti dengan ciphertext asli

for i in range(2**8, 2**64):
    if pow(i, e, n) == ciphertext:
        print(f"Flag = {i.to_bytes((i.bit_length() + 7) // 8, 'big')}")
        break

factors = factorint(n)
print(factors)


# ------------------

# with open('transparency.pem', 'rb') as f:
#     pubkey = serialization.load_pem_public_key(f.read(), backend= default_backend())

# numbers = pubkey.public_numbers()
# n = numbers.n
# e = numbers.e

# print(f"modulus (n): {n}")
# print(f"exponent (e): {e}")

# plaintext = b"crypto{"
# plaintext_int = int.from_bytes(plaintext, byteorder='big')

# # enkripsi: c = m^e mod n
# ciphertext = pow(plaintext_int, e, n)

# print("plainttext int:", plaintext_int)
# print("ciphertext (decimal):", ciphertext)
# print("ciphertext (hex)", hex(ciphertext))