from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import binascii

with open('transparency.pem', 'rb') as f:
    pubkey = serialization.load_pem_public_key(f.read(), backend= default_backend())

numbers = pubkey.public_numbers()
n = numbers.n
e = numbers.e

print(f"modulus (n): {n}")
print(f"exponent (e): {e}")

plaintext = b"crypto{"
plaintext_int = int.from_bytes(plaintext, byteorder='big')

# enkripsi: c = m^e mod n
ciphertext = pow(plaintext_int, e, n)

print("plainttext int:", plaintext_int)
print("ciphertext (decimal):", ciphertext)
print("ciphertext (hex)", hex(ciphertext))