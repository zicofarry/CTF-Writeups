def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x, y = extended_gcd(b, a % b)
        return (g, y, x - (a // b) * y)

p=26513; q=32321
gcd_val, u, v = extended_gcd(p, q)
# gcd = 1
# u = 10245
# v = -8404
print(min(u, v))
# -8404