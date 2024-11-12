import bcrypt
import jwt
import time
from datetime import datetime, timedelta
import json

class Authentication:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.failed_attempts = {}
        
    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def verify_password(self, password: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed)
    
    def generate_token(self, username: str) -> str:
        expiry = datetime.utcnow() + timedelta(seconds=Config.TOKEN_EXPIRY)
        payload = {
            'username': username,
            'exp': expiry
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> bool:
        try:
            jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return True
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")