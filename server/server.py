import socket
import json
from pathlib import Path
from crypto.encryption import AESCipher
from crypto.authentication import Authentication
from utils.rate_limiter import RateLimiter
from utils.logging_config import setup_logging
import threading
from typing import Dict, Any

class SecureServer:
    def __init__(self, host: str = Config.HOST, port: int = Config.PORT):
        self.host = host
        self.port = port
        self.auth = Authentication(secret_key="your_secret_key")  # Use secure key in production
        self.rate_limiter = RateLimiter(
            Config.RATE_LIMIT_REQUESTS,
            Config.RATE_LIMIT_PERIOD
        )
        self.logger = setup_logging()
        self.active_connections: Dict[str, Any] = {}
    
    def start(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.host, self.port))
                sock.listen(Config.MAX_CONNECTIONS)
                self.logger.info("server_start", host=self.host, port=self.port)
                
                while True:
                    conn, addr = sock.accept()
                    client_id = f"{addr[0]}:{addr[1]}"
                    
                    if not self.rate_limiter.is_allowed(client_id):
                        self.logger.warning("rate_limit_exceeded", client_id=client_id)
                        conn.close()
                        continue
                    
                    thread = threading.Thread(
                        target=self._handle_client,
                        args=(conn, addr)
                    )
                    thread.start()
                    self.active_connections[client_id] = {
                        'thread': thread,
                        'start_time': time.time()
                    }
        
        except Exception as e:
            self.logger.error("server_error", error=str(e))
            raise
    
    def _handle_client(self, conn: socket.socket, addr: tuple):
        client_id = f"{addr[0]}:{addr[1]}"
        
        try:
            # Authenticate client
            auth_data = json.loads(conn.recv(1024).decode())
            if not self.auth.verify_token(auth_data.get('token')):
                self.logger.warning("authentication_failed", client_id=client_id)
                conn.send(json.dumps({"error": "Authentication failed"}).encode())
                return
            
            # Receive metadata
            metadata = json.loads(conn.recv(1024).decode())
            filename = metadata['filename']
            filesize = metadata['filesize']
            
            # Check file size limit
            if filesize > Config.MAX_FILE_SIZE:
                self.logger.warning("file_size_exceeded", 
                                  client_id=client_id, 
                                  size=filesize)
                conn.send(json.dumps({"error": "File too large"}).encode())
                return
            
            # Receive encryption parameters
            salt = conn.recv(16)
            iv = conn.recv(16)
            hmac_value = conn.recv(32)  # HMAC-SHA256 is 32 bytes
            
            # Receive and process file
            encrypted_data = b''
            bytes_received = 0
            
            while bytes_received < filesize:
                try:
                    data = conn.recv(min(4096, filesize - bytes_received))
                    if not data:
                        break
                    encrypted_data += data
                    bytes_received += len(data)
                except socket.timeout:
                    self.logger.error("transfer_timeout", 
                                    client_id=client_id,
                                    filename=filename)
                    raise
            
            # Verify and decrypt file
            try:
                decrypted_data = AESCipher.verify_and_decrypt(
                    key,
                    iv,
                    encrypted_data,
                    hmac_value
                )
            except ValueError as e:
                self.logger.error("integrity_check_failed",
                                client_id=client_id,
                                filename=filename)
                conn.send(json.dumps({"error": "Integrity check failed"}).encode())
                return
            
            # Save file
            with open(f"received_{filename}", 'wb') as f:
                f.write(decrypted_data)
            
            self.logger.info("file_received",
                           client_id=client_id,
                           filename=filename,
                           size=filesize)
            
            conn.send(json.dumps({"status": "success"}).encode())
            
        except Exception as e:
            self.logger.error("transfer_error",
                            client_id=client_id,
                            error=str(e))
            try:
                conn.send(json.dumps({"error": str(e)}).encode())
            except:
                pass
        
        finally:
            conn.close()
            if client_id in self.active_connections:
                del self.active_connections[client_id]