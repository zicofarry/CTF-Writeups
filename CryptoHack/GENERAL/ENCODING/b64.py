import base64
str = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
flag = base64.b64encode(bytes.fromhex(str)).decode()
print(flag)
# crypto/Base+64+Encoding+is+Web+Safe/