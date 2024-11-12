from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

class AESCipher:
    def __init__(self, password: str):
        self.salt = os.urandom(16)
        self.key = self._derive_key(password.encode(), self.salt)
        
    def _derive_key(self, password: bytes, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password)
    
    def _create_hmac(self, data: bytes) -> bytes:
        h = hmac.HMAC(self.key, hashes.SHA256(), backend=default_backend())
        h.update(data)
        return h.finalize()
    
    def encrypt(self, data: bytes) -> tuple[bytes, bytes, bytes, bytes]:
        iv = os.urandom(16)
        
        # Pad the data
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        # Encrypt
        cipher = Cipher(
            algorithms.AES256(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Create HMAC
        hmac_value = self._create_hmac(ciphertext)
        
        return self.salt, iv, ciphertext, hmac_value
    
    @staticmethod
    def verify_and_decrypt(key: bytes, iv: bytes, ciphertext: bytes, hmac_value: bytes) -> bytes:
        # Verify HMAC
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(ciphertext)
        try:
            h.verify(hmac_value)
        except Exception:
            raise ValueError("File integrity check failed")
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES256(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()