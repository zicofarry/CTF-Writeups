from PIL import Image
import numpy as np

# Buka gambar
img = Image.open("location.png")
pixels = np.array(img)

# Ukuran gambar
height, width, _ = pixels.shape

# Geser tiap baris ke kiri sesuai dengan distorsi
for i in range(height):
    shift = (i * 5) % width
    pixels[i] = np.roll(pixels[i], -shift, axis=0)  # geser ke kiri

# Simpan hasil
fixed_img = Image.fromarray(pixels)
fixed_img.save("fixed_image.png")
fixed_img.show()
