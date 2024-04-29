from ascon import encrypt, decrypt
import random


message = b"This is a secret message!"
key = b"your_secret_key_"
nonce = b'gggggggggggggggg'
associated_data = b""  

ciphertext = encrypt(key, nonce, associated_data, message, variant="Ascon-128")

decrypted_message = decrypt(key, nonce, associated_data, ciphertext, variant="Ascon-128")

print("Original Message:", message.decode())
print("Decrypted Message:", decrypted_message.decode())
