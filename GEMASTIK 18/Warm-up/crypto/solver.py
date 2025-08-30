from Crypto.Util.number import long_to_bytes, isPrime
import string

# --- Helper Functions ---

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def is_printable(data):
    if not data:
        return False
    return all(c in string.printable.encode() for c in data)

# --- Main Solver Function ---

def solve_common_modulus():
    print("--- RSA Common Modulus Attack Solver ---")
    print("Membaca input dari file out.txt...")

    try:
        with open("out.txt", "r") as f:
            content = f.read().strip().split()
            if len(content) < 3:
                print("[!] File out.txt harus berisi setidaknya tiga angka: n ct1 ct2")
                return
            n = int(content[0])
            ct1 = int(content[1])
            ct2 = int(content[2])
    except FileNotFoundError:
        print("[!] File out.txt tidak ditemukan.")
        return
    except ValueError:
        print("[!] Format file out.txt salah. Pastikan hanya berisi angka.")
        return

    # 2. Generate a list of possible exponents (10-bit primes)
    primes = [i for i in range(512, 1024) if isPrime(i)]
    print(f"[*] Memulai pencarian dengan {len(primes)} kandidat eksponen prima...")

    # 3. Brute-force through all pairs of possible exponents
    for e1 in primes:
        for e2 in primes:
            if e1 == e2:
                continue

            g, a, b = egcd(e1, e2)

            try:
                if a < 0:
                    term1 = pow(modinv(ct1, n), -a, n)
                else:
                    term1 = pow(ct1, a, n)

                if b < 0:
                    term2 = pow(modinv(ct2, n), -b, n)
                else:
                    term2 = pow(ct2, b, n)

                pt_num = (term1 * term2) % n
                pt_bytes = long_to_bytes(pt_num)

                if is_printable(pt_bytes) and len(pt_bytes) > 5:
                    print("\n" + "="*40)
                    print("[+] FLAG DITEMUKAN!")
                    print(f"    Eksponen yang digunakan (e1, e2): ({e1}, {e2})")
                    print(f"    Flag: {pt_bytes.decode('utf-8')}")
                    print("="*40)
                    return

            except Exception:
                continue

    print("\n[!] Gagal menemukan flag. Semua kombinasi telah dicoba.")

# --- Run the solver ---
if __name__ == "__main__":
    solve_common_modulus()

# gemastik{warmup_baby_crypto}