import unittest
from crypto.encryption import AESCipher
from crypto.authentication import Authentication
from utils.rate_limiter import RateLimiter
import time

class TestSecurity(unittest.TestCase):
    def test_encryption(self):
        # Test encryption and decryption
        original_data = b"Test data for encryption"
        password = "test_password"
        
        cipher = AESCipher(password)
        salt, iv, ciphertext, hmac_value = cipher.encrypt(original_data)
        
        # Test decryption
        decrypted_data = AESCipher.verify_and_decrypt(cipher.key, iv, ciphertext, hmac_value)
        self.assertEqual(original_data, decrypted_data)
        
        # Test HMAC verification
        with self.assertRaises(ValueError):
            AESCipher.verify_and_decrypt(cipher.key, iv, ciphertext + b"tampered", hmac_value)
    
    def test_authentication(self):
        auth = Authentication("test_secret_key")
        
        # Test password hashing
        password = "test_password"
        hashed = auth.hash_password(password)
        self.assertTrue(auth.verify_password(password, hashed))
        self.assertFalse(auth.verify_password("wrong_password", hashed))
        
        # Test token generation and verification
        token = auth.generate_token("testuser")
        self.assertTrue(auth.verify_token(token))
    
    def test_rate_limiter(self):
        limiter = RateLimiter(max_requests=2, time_window=1)
        client_id = "test_client"
        
        # Test within limits
        self.assertTrue(limiter.is_allowed(client_id))
        self.assertTrue(limiter.is_allowed(client_id))
        self.assertFalse(limiter.is_allowed(client_id))
        
        # Test reset after time window
        time.sleep(1)
        self.assertTrue(limiter.is_allowed(client_id))
