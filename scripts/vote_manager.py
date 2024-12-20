import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

#gen key
AES_KEY = os.urandom(32)  # 32 bytes = 256 bits
AES_IV = os.urandom(16)   # IV pour AES-CBC

def encrypt_data(data: str) -> bytes:
    """Chiffre les données en AES-CBC."""
    backend = default_backend()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=backend)
    encryptor = cipher.encryptor()


    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

def save_vote(username: str, email: str, composer: str):
    """Enregistre un vote dans un fichier JSON après chiffrement du compositeur."""

    encrypted_composer = encrypt_data(composer)

    
    vote_data = {
        "username": username,
        "email": email,
        "composer": encrypted_composer.hex()  # Convertit les bytes en chaîne hexadécimale
    }

    with open("votes.json", "a") as file:
        file.write(json.dumps(vote_data) + "\n")
        