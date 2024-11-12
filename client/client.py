import socket
import json
from pathlib import Path
from tqdm import tqdm
from crypto.encryption import AESCipher
from utils.logging_config import setup_logging

class SecureClient:
    def __init__(self, host: str = Config.HOST, port: int = Config.PORT):
        self.host = host
        self.port = port
        self.logger = setup_logging("client.log")
        self.token = None
    
    def login(self, username: str, password: str):
        # Authenticate and get token
        auth_data = {
            "username": username,
            "password": password
        }
        
        with socket.create_connection((self.host, self.port)) as sock:
            sock.send(json.dumps(auth_data).encode())
            response = json.loads(sock.recv(1024).decode())
            if "error" in response:
                raise ValueError(response["error"])
            self.token = response["token"]
    
    def send_file(self, filepath: str, password: str):
        filepath = Path(filepath)
        if not filepath.exists():
            self.logger.error("file_not_found", filepath=str(filepath))
            raise FileNotFoundError(f"File {filepath} not found")
        
        try:
            # Read and encrypt file
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            if len(file_data) > Config.MAX_FILE_SIZE:
                self.logger.error("file_too_large", 
                                filepath=str(filepath),
                                size=len(file_data))
                raise ValueError("File too large")
            
            cipher = AESCipher(password)
            salt, iv, encrypted_data, hmac_value = cipher.encrypt(file_data)
            
            # Send file
            with socket.create_connection((self.host, self.port)) as sock:
                # Send authentication
                sock.send(json.dumps({"token": self.token}).encode())
                response = json.loads(sock.recv(1024).decode())
                if "error" in response:
                    raise ValueError(response["error"])
                
                # Send metadata
                metadata = {
                    "filename": filepath.name,
                    "filesize": len(encrypted_data)
                }
                sock.send(json.dumps(metadata).encode())
                
                # Send encryption parameters
                sock.send(salt)
                sock.send(iv)
                sock.send(hmac_value)
                
                # Send encrypted file with progress bar
                with tqdm(total=len(encrypted_data),
                         unit='B',
                         unit_scale=True,
                         desc="Sending") as pbar:
                    remaining_data = encrypted_data
                    while remaining_data:
                        chunk = remaining_data[:4096]
                        remaining_data = remaining_data[4096:]
                        sock.send(chunk)
                        pbar.update(len(chunk))
                
                # Get response
                response = json.loads(sock.recv(1024).decode())
                if "error" in response:
                    raise ValueError(response["error"])
                
                self.logger.info("file_sent",
                 filepath=str(filepath),
                 size=len(encrypted_data))
                
                return response["status"] == "success"
                
        except Exception as e:
            self.logger.error("transfer_error",
                            filepath=str(filepath),
                            error=str(e))
            raise

# Example usage
if __name__ == "__main__":
    import argparse
    import getpass
    
    parser = argparse.ArgumentParser(description='Secure File Transfer Client')
    parser.add_argument('--host', default=Config.HOST, help='Server host')
    parser.add_argument('--port', type=int, default=Config.PORT, help='Server port')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('filepath', help='File to transfer')
    
    args = parser.parse_args()
    
    try:
        # Get passwords securely
        login_password = getpass.getpass('Login password: ')
        encryption_password = getpass.getpass('File encryption password: ')
        
        # Initialize client
        client = SecureClient(args.host, args.port)
        
        # Login
        print("Logging in...")
        client.login(args.username, login_password)
        
        # Send file
        print(f"Sending file: {args.filepath}")
        success = client.send_file(args.filepath, encryption_password)
        
        if success:
            print("File transferred successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)