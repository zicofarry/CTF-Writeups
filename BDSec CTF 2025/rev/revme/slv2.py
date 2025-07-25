# revMe_flag_extractor.py

def extract_flag(filename, key=0xAA):
    with open(filename, "rb") as f:
        data = f.read()

    possible_flag = b""
    # Berdasarkan offset hasil sebelumnya: 0x2000 (8192) panjang sekitar 20 byte
    start_offset = 0x2000
    flag_length = 20  # estimasi panjang flag

    for i in range(start_offset, start_offset + flag_length):
        decoded_byte = data[i] ^ key
        possible_flag += bytes([decoded_byte])

    return possible_flag.decode(errors="ignore")


if __name__ == "__main__":
    flag = extract_flag("revMe.bdsec")
    print("Extracted Flag:", flag)
