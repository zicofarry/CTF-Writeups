# Soal Laporan Eldas #
<img width="454" height="676" alt="Image" src="https://github.com/user-attachments/assets/0a64b43d-4962-4942-aa41-a5612bd20ff9" />

# Deskripsi #

Diberikan file attachment berupa file docx yang bernama LAPORAN_AKHIR_ELDAS24_KELOMPOK_50.docx dan disebutkan terdapat file berbahaya dibalik file docx tersebut dan kita perlu mencarinya (flag) sebelum dikirim ke dosen.

# Solusi #

Setelah melakukan analisis, dari awal kita sudah punya feeling bahwa ini merupakan file zip yang nantinya kita bisa dapatkan xml nya.

danyapp benar saja ketika kita ubah ekstensi filenya menjadi zip dan diekstrak, terdapat banyak file seperti ini.

<img width="719" height="227" alt="Image" src="https://github.com/user-attachments/assets/25c058aa-ddcb-4af9-86d0-c6286c08bdb7" />

Tanpa berlama-lama, kita langsung mencari string yang mencurigakan dengan command

```
grep -ao '[A-Za-z0-9+/=]\{20,\}' ./* -R
```

dan ditemukanlah string base64 yang cukup mencurigakan.

<img width="926" height="500" alt="Image" src="https://github.com/user-attachments/assets/bdcdefab-b617-4a88-a8af-a678f7f011e2" />

Namun, setelah kita konversikan dan coba submit, oh noo ternyata itu adalah fake flag.

<img width="870" height="299" alt="Image" src="https://github.com/user-attachments/assets/8ad75cd8-3056-4e4d-bc2c-c641e73ba3c7" />

Okee, tapi itu clue yang lumayan bermanfaaat ACE{kalem_dikit_lagi_nemu_bang} kita berasumsi bahwa hal yang kita kerjakan sudah lumayan benar dan tinggal melanjutkan saja.

Karena fake flag itu disimpan di file settings.xml.rels, maka saya pun mengecek isian filenya.

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate" Target="https://github.com/KurniaRadhit/Stockmate/blob/main/Stockmate/Modul/__pycache__/open_download.cpython-310.pyc" TargetMode="External" Data="QUNFe2thbGVtX2Rpa2l0X2xhZ2lfbmVtdV9iYW5nfQ=="/>
</Relationships>
```

di sana terdapat link github yang cukup mencurigakan. Maka dari itu, saya klik linknya dan link itu mengarahkan kita untuk mendownload file open_download.cpython-310.pyc

setelah itu, untuk membaca isi code dari file tersebut daya menggunakan tool pycdc dan setelah dieksekusi, muncul code seperti ini.

<img width="1919" height="910" alt="Image" src="https://github.com/user-attachments/assets/0ab710fa-c267-4043-b413-ff5f4bf045d8" />

Terdapat lagi link yang mencurigakan, setelah saya klik link itu, link itu mulai mendownload file bernama LAPORAN_AKHIR_ELDAS24_KELOMPOK_50.dotm lalu saya membuka filenya menggunakan tools olevba dan muncul output seperti yang saya simpan di file output.txt

Sebenarnya ketika saya lempar file output.txt itu ke AI dia langsung memberikan flag jadinya, tapi biar di write-upnya rapih, saya minta dia untuk ubah dalam versi python dan begini jadinya.

```
# solve.py
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
```

<img width="1160" height="107" alt="Image" src="https://github.com/user-attachments/assets/623979aa-985d-45b6-bcdf-2e2f0fcdfca3" />

# Flag #
```
ACE{hidden_malicus_code_in_the_word_file_is_bad_in_injected_template_triggering_an_attack}
````
