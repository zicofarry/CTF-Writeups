from pwn import xor
# 1 byte = 8 bit = 256 desimal

str = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")
for key in range(256):
    flag = xor(str, key)
    if b"crypto{" in flag:
        print(f"[+] found key: {key}")
        print(flag.decode())
        break
# crypto{0x10_15_my_f4v0ur173_by7e}