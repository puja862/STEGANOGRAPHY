import cv2
import os
import hashlib

# Specify the path to the encrypted image
encrypted_image_path = r'C:\Users\LAVANYA\Downloads\encryptedImage.jpg'

# Read the encrypted image
encrypted_img = cv2.imread(encrypted_image_path)

# Check if the image is successfully loaded
if encrypted_img is None:
    print("Encrypted image not found. Check the file path and make sure the image exists.")
    exit()

# Get the dimensions of the image
height, width, channels = encrypted_img.shape

# Prompt the user to input the password
password = input("Enter the passcode: ")

# Hash the password using SHA-256
hash_object = hashlib.sha256(password.encode())
hashed_password = hash_object.digest()

# Initialize dictionaries for mapping characters to their ASCII values and vice versa
d = {}
c = {}

# Fill the dictionaries with ASCII values (0-255)
for i in range(256):
    d[chr(i)] = i  # Character to ASCII
    c[i] = chr(i)  # ASCII to character

# Initialize variables for image coordinates and color channel
n = 0  # Row index
m = 0  # Column index
z = 0  # Color channel index

# Initialize an empty string to store the decoded message
decoded_msg = ""

# Decode the hidden message from the image using the hashed password
try:
    while True:
        # Get the original value by reversing the encoding operation
        original_value = (int(encrypted_img[n, m, z]) - hashed_password[len(decoded_msg) % len(hashed_password)]) % 256
        char = c[original_value]

        # Check for the termination condition (assuming the message ends with a null character '\0')
        if char == '\0':
            break

        decoded_msg += char

        # Move to the next pixel
        m += 1

        # If the column index exceeds the image width, reset it and move to the next row
        if m >= width:
            m = 0
            n += 1

        # If the row index exceeds the image height, stop decoding (no more message to decode)
        if n >= height:
            break

        # Cycle through the color channels (0, 1, 2) for RGB
        z = (z + 1) % 3
except KeyError:
    print("Decryption failed. The image might be corrupted or the password is incorrect.")

print(f"Decoded message: {decoded_msg}")
