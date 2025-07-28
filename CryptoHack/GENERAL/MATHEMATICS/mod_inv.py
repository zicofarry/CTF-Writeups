# Fermat’s Little Theorem
# if a^(p-1) ≡ 1 mod p
# then a_inv = a^(p-2) mod p
a = 3
p = 13
inverse = pow(a, p - 2, p)
print(inverse)
# 9