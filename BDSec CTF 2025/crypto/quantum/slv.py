from Crypto.Util.number import *
import hashlib
import base64
import zlib

X = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476,
     0xC3D2E1F0, 0x76543210, 0xFEDCBA98, 0x89ABCDEF]

# hashing generator seperti di fungsi G
def G(a, b):
    d = a
    for i in range(b):
        if i % 4 == 0:
            d = hashlib.sha256(d).digest()
        elif i % 4 == 1:
            d = hashlib.blake2b(d, digest_size=32).digest()
        elif i % 4 == 2:
            d = hashlib.md5(d).digest() * 2
        else:
            d = hashlib.sha1(d).digest() + d[:12]
    return d

# inverse of H (custom xor-rot decryption)
def H_inv(m, k):
    q = bytearray()
    for i, t in enumerate(m):
        s = t ^ (X[i % len(X)] & 0xFF)
        s = ((s >> 3) | (s << 5)) & 0xFF  # reverse of (<<3 | >>5)
        s ^= k[i % len(k)]
        q.append(s)
    return bytes(q)

# ------------- main decrypt routine ----------------

cipher_b64 = "FL6gWSgGl71j8RANN2yzz9XckwawQ8MXqE7IAOVygOclZiHgi161L7s="
cipher = base64.b64decode(cipher_b64)

# step 1: reverse 3 layers of XOR
layers = [
    b"binary_singularity",
    b"entropic_veil_layer",
    b"qbit_spectrum_field"
]

for i in range(3)[::-1]:  # reverse order
    key = G(layers[i], i+1)
    cipher = bytes([b ^ key[j % len(key)] for j, b in enumerate(cipher)])

# step 2: reverse H
seed = b"simple_seed_123"
k = G(seed, 5)
plaintext = H_inv(cipher, k)

print("Decrypted message:", plaintext.decode(errors="ignore"))
