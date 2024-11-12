import argparse
import secrets
from pathlib import Path
from crypto.authentication import Authentication
import json

def setup_server():
    """Initialize server configuration and create necessary directories"""
    # Create directories
    Path("logs").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("users").mkdir(exist_ok=True)
    
    # Generate secret key
    secret_key = secrets.token_hex(32)
    
    # Create config file
    config = {
        "secret_key": secret_key,
        "host": Config.HOST,
        "port": Config.PORT,
        "max_file_size": Config.MAX_FILE_SIZE,
        "rate_limit_requests": Config.RATE_LIMIT_REQUESTS,
        "rate_limit_period": Config.RATE_LIMIT_PERIOD
    }
    
    with open("config/server_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("Server configuration created successfully!")