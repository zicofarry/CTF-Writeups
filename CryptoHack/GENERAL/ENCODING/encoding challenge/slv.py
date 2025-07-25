from pwn import *
import json
import base64
import codecs
from Crypto.Util.number import long_to_bytes # type: ignore

r = remote('socket.cryptohack.org', 13377, level='debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

while True:
    received = json_recv()
    if "flag" in received:
        print(received['flag'])
        break

    encoding_type = received["type"]
    encoded = received["encoded"]

    if encoding_type == "base64":
        decoded = base64.b64decode(encoded).decode()
    elif encoding_type == "hex":
        decoded = bytes.fromhex(encoded).decode()
    elif encoding_type == "rot13":
        decoded = codecs.decode(encoded, 'rot_13')
    elif encoding_type == "bigint":
        decoded = long_to_bytes(int(encoded, 16)).decode()
    elif encoding_type == "utf-8":
        decoded = ''.join([chr(c) for c in encoded])
    else:
        print("Unkonwn encoding type")
        break

    to_send = {
        "decoded" : decoded
    }
    json_send(to_send)

# crypto{3nc0d3_d3c0d3_3nc0d3}