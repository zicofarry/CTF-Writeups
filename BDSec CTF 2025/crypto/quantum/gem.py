import base64
import hashlib

# --- Setup dari Tantangan ---
# Bagian ini berisi konstanta dan fungsi yang disediakan dalam file asli.

# Array konstanta X
X = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476,
     0xC3D2E1F0, 0x76543210, 0xFEDCBA98, 0x89ABCDEF]

# Fungsi hashing G
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

# --- Logika Dekripsi ---
# Fungsi ini membalikkan operasi dari fungsi H yang asli.

def reverse_H(encrypted_data, key):
    decrypted_bytes = bytearray()
    for i, byte_val in enumerate(encrypted_data):
        # 1. Balikkan XOR terakhir dengan array X
        s = byte_val ^ (X[i % len(X)] & 0xFF)
        
        # 2. Balikkan rotasi bit ke kiri (dengan melakukan rotasi ke kanan)
        s = ((s >> 3) | (s << 5)) & 0xFF
        
        # 3. Balikkan XOR awal dengan kunci
        s = s ^ key[i % len(key)]
        
        decrypted_bytes.append(s)
    return bytes(decrypted_bytes)

# --- Eksekusi ---
# Mendekripsi pesan yang disadap untuk menemukan flag.

# Pesan dari tantangan CTF
intercepted_message = 'FL6gWSgGl71j8RANN2yzz9XckwawQ8MXqE7IAOVygOclZiHgi161L7s='

# Seed yang diketahui yang digunakan untuk menghasilkan kunci
key_seed = b"simple_seed_123"

# 1. Dekode pesan dari Base64
encrypted_data = base64.b64decode(intercepted_message)

# 2. Buat ulang kunci yang sama persis yang digunakan untuk enkripsi
decryption_key = G(key_seed, 5)

# 3. Dekripsi data menggunakan fungsi yang dibalik dan kunci
flag = reverse_H(encrypted_data, decryption_key)

# Cetak flag terakhir
print("Dekripsi berhasil!")
print(f"Flag: {flag.decode()}")
