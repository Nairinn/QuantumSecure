class Config:
    # Server settings
    HOST = 'localhost'
    PORT = 8443
    MAX_CONNECTIONS = 5
    
    # Security settings
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    RATE_LIMIT_REQUESTS = 10
    RATE_LIMIT_PERIOD = 60  # seconds
    
    # Authentication settings
    TOKEN_EXPIRY = 3600  # 1 hour
    MAX_LOGIN_ATTEMPTS = 3
    LOCKOUT_PERIOD = 300  # 5 minutes
