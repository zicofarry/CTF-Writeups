cipher = [0xe8, 0xee, 0xf9, 0xef, 0xe9]  # ganti dari hasil gdb
key = 0xaa                               # dari 0x402019

flag = ''.join([chr(c ^ key) for c in cipher])
print(flag)
