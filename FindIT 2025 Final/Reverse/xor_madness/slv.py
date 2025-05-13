cipher = b"Uz}wZGPGUhzj'Lq } aL\"}\"Lu\x7f'tL}j'Lq'}tn"

for key in range(256):
    plain = ''.join(chr(c ^ key) for c in cipher)
    if all(32 <= ord(c) <= 126 for c in plain):
        print(f"Key {key:02x}: {plain}")
