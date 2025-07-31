p = 29
ints = [14, 6, 11]
flag = 999999
for a in range(1, p):
    square = (a * a) % p
    for x in ints:
        if square == x:
            print(f"{x} is a quadratic residue modulo {p}, one square root is {a}")
            flag = min(flag, a)

print(flag)
# 8