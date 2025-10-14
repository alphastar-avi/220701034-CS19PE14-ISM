import cv2
import string
import os

# Create dictionaries for character ↔ ASCII mappings
d = {}
c = {}
for i in range(256):
    d[chr(i)] = i
    c[i] = chr(i)

# Load the image
image_path = r"C:\Users\TCS\Desktop\img.jpg"
x = cv2.imread(image_path)

if x is None:
    print("Error: Image not found. Check the path.")
    exit()

rows, cols, _ = x.shape
print(f"Image size: {rows} x {cols}")

# --- ENCRYPTION ---
key = input("Enter key to edit (Security Key): ")
text = input("Enter text to hide: ")

kl = 0  # key index
z = 0   # channel index (0=B,1=G,2=R)
n = 0   # row index
m = 0   # col index

for i in range(len(text)):
    # Encrypt character by XOR with key
    x[n, m, z] = d[text[i]] ^ d[key[kl]]

    # Update indexes
    m += 1
    if m >= cols:
        m = 0
        n += 1
        if n >= rows:
            print("Error: Message too long for the image.")
            exit()

    z = (z + 1) % 3
    kl = (kl + 1) % len(key)

# Save encrypted image
cv2.imwrite("encrypted_img.jpg", x)
os.startfile("encrypted_img.jpg")
print("✅ Data hiding in image completed successfully.")

# --- DECRYPTION ---
choice = int(input("\nEnter 1 to extract data from Image: "))
if choice == 1:
    key1 = input("Re-enter key to extract text: ")
    if key1 != key:
        print("❌ Key doesn't match. Decryption failed.")
    else:
        decrypt = ""
        kl = 0
        z = 0
        n = 0
        m = 0

        for i in range(len(text)):
            decrypted_char = c[x[n, m, z] ^ d[key1[kl]]]
            decrypt += decrypted_char

            m += 1
            if m >= cols:
                m = 0
                n += 1
                if n >= rows:
                    break

            z = (z + 1) % 3
            kl = (kl + 1) % len(key1)

        print("🔓 Extracted text was:", decrypt)
else:
    print("Exiting program.")

