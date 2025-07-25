import base64

def decrypt_xor_string(text, keys):
    return ''.join(chr(ord(c) ^ keys[i]) for i, c in enumerate(text))

def hex_to_string(hexstr):
    return bytes.fromhex(hexstr).decode()

def rot13(text):
    result = ''
    for c in text:
        if 'a' <= c <= 'm' or 'A' <= c <= 'M':
            result += chr(ord(c) + 13)
        elif 'n' <= c <= 'z' or 'N' <= c <= 'Z':
            result += chr(ord(c) - 13)
        else:
            result += c
    return result

def decrypt_rot13_hex(hexstr):
    return rot13(hex_to_string(hexstr))

def xor_hex(hexstr, key):
    decoded = hex_to_string(hexstr)
    return ''.join(chr(ord(c) ^ key) for c in decoded)

def str_reverse(s):
    return s[::-1]

def decrypt_caesar_hex(hexstr, shift):
    decoded = hex_to_string(hexstr)
    if shift == 0:
        return decoded
    result = ''
    for c in decoded:
        if 'a' <= c <= 'z':
            result += chr(((ord(c) - ord('a') - shift + 26) % 26) + ord('a'))
        elif 'A' <= c <= 'Z':
            result += chr(((ord(c) - ord('A') - shift + 26) % 26) + ord('A'))
        else:
            result += c
    return result

def concat_hex(*hex_chars):
    return ''.join(hex_to_string(h) for h in hex_chars)

def decrypt_base64_hex(b64str):
    return base64.b64decode(b64str).decode()

def xor_cipher(text, key):
    return ''.join(chr(ord(c) ^ key) for c in text)

def decrypt_vigenere(text, key):
    result = ''
    key_index = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[key_index].lower()) - ord('a')
            if c.islower():
                result += chr((ord(c) - ord('a') - shift + 26) % 26 + ord('a'))
            else:
                result += chr((ord(c) - ord('A') - shift + 26) % 26 + ord('A'))
            key_index = (key_index + 1) % len(key)
        else:
            result += c
    return result

def decrypt_atbash(text):
    result = ''
    for c in text:
        if 'a' <= c <= 'z':
            result += chr(ord('z') - (ord(c) - ord('a')))
        elif 'A' <= c <= 'Z':
            result += chr(ord('Z') - (ord(c) - ord('A')))
        else:
            result += c
    return result

# === START reconstructing buffer ===

a1 = decrypt_xor_string("EGA", [4, 4, 4])  # XOR each char with 4 → gets 'ACK'
a2 = [91, 34, 56]

b = [104, 105, 100, 100, 101, 110]  # → 'hidden'

c1 = decrypt_rot13_hex("7a6e7976706866")        # hex→str→ROT13
c2 = xor_hex("636f6465", 0)                     # just decode: 'code'
c3 = str_reverse(hex_to_string("6e69"))         # 'in' reversed: 'ni'
c4 = decrypt_caesar_hex("746865", 0)            # 'the'
c5 = concat_hex("77", "6f", "72", "64")         # 'word'
c6 = hex_to_string("66696c65")                  # 'file'
c7 = hex_to_string("6973")                      # 'is'
c8 = decrypt_base64_hex("YmFk")                 # 'bad'

cipher1 = base64.b64decode("aW4=").decode()     # 'in'
cipher2 = xor_cipher("`gclj}lm", 9)             # XOR each char with 9
cipher3 = str_reverse("etalpmet")               # 'template'
cipher4 = decrypt_vigenere("ttmgiirkrg", "ace") # Vigenère decrypt
cipher5 = chr(97) + chr(110)                    # 'an'
cipher6 = decrypt_atbash("zggzxp")              # Atbash

buffer = ''
buffer += a1  # 'ACK'
buffer += chr(a2[0] + 32)  # 91+32 = 123 → '{'
for val in b:
    buffer += chr(val)  # 'hidden'
buffer += "_"
buffer += c1 + "_"
buffer += c2 + "_"
buffer += c3 + "_"
buffer += c4 + "_"
buffer += c5 + "_"
buffer += c6 + "_"
buffer += c7 + "_"
buffer += c8 + "_"
buffer += cipher1 + "_"
buffer += cipher2 + "_"
buffer += cipher3 + "_"
buffer += cipher4 + "_"
buffer += cipher5 + "_"
buffer += cipher6 + "}"

print(buffer)
