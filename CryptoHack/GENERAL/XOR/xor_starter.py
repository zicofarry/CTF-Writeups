from pwn import xor

str = b'label'
key = 13

# result = ''.join([chr(ord(c) ^ key) for c in str])
result = xor(str, key)

print(f"crypto{{{result.decode()}}}")
# crypto{aloha}