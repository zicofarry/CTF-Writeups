from PIL import Image as ig

img1 = ig.open("flag.png").convert("RGB")
img2 = ig.open("lemur.png").convert("RGB")

result = ig.new("RGB", img1.size)

for x in range(img1.width):
    for y in range(img1.height):
        r1, g1, b1 = img1.getpixel((x,y))
        r2, g2, b2 = img2.getpixel((x,y))
        result.putpixel((x, y), (r1 ^ r2, g1 ^ g2, b1 ^ b2))

result.save("output.png")
# crypto{X0Rly_n0t!}