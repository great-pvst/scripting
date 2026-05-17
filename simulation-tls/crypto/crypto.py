import base64
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography import x509

def encrypt_rsa(data, public_key):
    """Chiffre des donnees avec RSA (cle publique)"""
    try:
        encrypted = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted
    except Exception as e:
        print(f"[ERREUR] Chiffrement RSA echoue: {e}")
        return None

def decrypt_rsa(encrypted_data, private_key):
    """Dechiffre des donnees avec RSA (cle privee)"""
    try:
        decrypted = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted
    except Exception as e:
        print(f"[ERREUR] Dechiffrement RSA echoue: {e}")
        return None

def encrypt_aes(data, key, iv):
    """Chiffre des donnees avec AES-256-CBC"""
    try:
        # Padding PKCS7
        pad_len = 16 - (len(data) % 16)
        data += bytes([pad_len] * pad_len)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(data) + encryptor.finalize()
        return encrypted
    except Exception as e:
        print(f"[ERREUR] Chiffrement AES echoue: {e}")
        return None

def decrypt_aes(encrypted_data, key, iv):
    """Dechiffre des donnees avec AES-256-CBC"""
    try:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
        # Supprimer le padding
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]
    except Exception as e:
        print(f"[ERREUR] Dechiffrement AES echoue: {e}")
        return None

def compute_sha1(data):
    """Calcule le hash SHA-1"""
    digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
    digest.update(data)
    return digest.finalize()

def load_server_certificate(cert_pem):
    """Charge et verifie le certificat du serveur"""
    try:
        cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
        return cert
    except Exception as e:
        print(f"[ERREUR] Certificat: {e}")
        return None
