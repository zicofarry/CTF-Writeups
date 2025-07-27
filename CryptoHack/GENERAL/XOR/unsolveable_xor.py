from pwn import xor

str = bytes.fromhex("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")
known = b"crypto{"
key = xor(str[:len(known)], known) + b"y"
print(key)
flag = xor(str, key)
print(flag.decode())