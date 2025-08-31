#!/usr/bin/env python3
import subprocess
import sys
import time

BINARY = "./Packs.exe"
WINE = False
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}-!@#$%^&*()[]:;<>?,./\\|+ "
L = 48  # panjang flag (didapatkan dari jumlah Nope. nya yaitu 48)

# prefix yang sudah diketahui (format flag)
prefix_known = list("GEMASTIK18{") 

def run_input(s):
    cmd = [BINARY]
    if WINE:
        cmd = ["wine", BINARY]
    try:
        p = subprocess.run(cmd, input=(s+"\n").encode(),
                           capture_output=True, timeout=4)
    except subprocess.TimeoutExpired:
        return None
    return p.stdout.decode(errors="ignore")

def count_nope(out):
    return out.count("Nope.")

filler = "#"
# flag = list(filler * L) # kalo mau bruteforce dari awal
flag = prefix_known + [filler] * (L - len(prefix_known))  # untuk mempercepat proses bruteforce, jadi pake prefix yang udah diketahui

# for i in range(L): # kalo mau bruteforce dari awal
for i in range(len(prefix_known), L):  # mulai bruteforce setelah prefix_known
    candidate_base = "".join(flag[:i]) + filler*(L-i)
    out_base = run_input(candidate_base)
    if out_base is None:
        print("Program timeout saat baseline.")
        sys.exit(1)
    base_nope = count_nope(out_base)

    found = False
    for c in CHARS:
        candidate = "".join(flag[:i]) + c + filler*(L-i-1)
        out = run_input(candidate)
        if out is None:
            continue
        n = count_nope(out)

        # update flag sementara
        flag[i] = c

        # persentase progress
        progress_percent = (i + 1) / L * 100

        # print progress bar + Nope count
        bar_length = 40
        filled_length = int(bar_length * (i + 1) / L)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        sys.stdout.write(f"\r[{bar}] {progress_percent:.1f}% | Nope: {n}")
        sys.stdout.flush()

        # print flag sementara di baris bawah
        sys.stdout.write(f"\n{''.join(flag)}")
        sys.stdout.flush()
        sys.stdout.write("\033[F")  # pindah cursor satu baris ke atas
        sys.stdout.flush()

        if n < base_nope:
            found = True
            break

    if not found:
        flag[i] = filler

# pindah baris setelah selesai
sys.stdout.write("\n\nRecovered flag: " + "".join(flag) + "\n")

# GEMASTIK18{S1mpl3_P4ck3r_f0r_4_S1mpl3_Ch4ll3nge}