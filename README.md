# QuantumSecure

A robust and secure file transfer system featuring military-grade encryption, token-based authentication, rate limiting, and comprehensive security logging.

## Key Features

- **Advanced Encryption**
  - AES-256 encryption in CBC mode
  - PBKDF2 key derivation (100,000 iterations)
  - Random IV generation per session
  - PKCS7 padding implementation
  - HMAC integrity verification

- **Authentication & Security**
  - JWT-based token authentication
  - bcrypt password hashing
  - Rate limiting (10 requests/60 seconds)
  - 3-attempt login with 5-minute lockout
  - 1-hour token expiry

- **File Transfer**
  - Chunked transfer (4KB blocks)
  - Support for files up to 100MB
  - Real-time progress monitoring
  - Integrity verification
  - Automatic cleanup

## Quick Start


# Install dependencies
pip install -r requirements.txt

# Start the server
python server.py

# Run the client
python client.py --username <username> filepath


## Configuration

Default settings in `Config`:

HOST = 'localhost'
PORT = 8443
MAX_CONNECTIONS = 5
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_PERIOD = 60  # seconds
TOKEN_EXPIRY = 3600    # 1 hour
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_PERIOD = 300   # 5 minutes


## Project Structure


quantumsecure/
├── client.py           # Client implementation
├── server.py           # Server implementation
├── config.py           # Configuration settings
├── crypto/
│   ├── encryption.py   # AES encryption implementation
│   └── authentication.py # JWT authentication
├── utils/
│   ├── rate_limiter.py # Rate limiting implementation
│   └── logging_config.py # Structured logging setup
└── tests/
    └── test_security.py # Security feature tests


## Security Features

### Encryption
- AES-256 in CBC mode with PBKDF2
- Random IV generation
- HMAC integrity verification
- Secure key derivation

### Authentication
- JWT token-based system
- bcrypt password hashing
- Rate limiting protection
- Login attempt monitoring

### Logging & Monitoring
- Structured logging with JSON format
- Security event tracking
- Transfer monitoring
- Error logging

## Requirements


cryptography>=3.4
bcrypt>=3.2
PyJWT>=2.0
structlog>=21.0
tqdm>=4.65.0


## Testing


python -m unittest tests/test_security.py


## Error Handling

- Authentication failures
- File integrity violations
- Size limit exceedance
- Rate limit violations
- Network timeouts
- File handling errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Author

Naing Lynn Kyaw
- GitHub: [@Nairinn](https://github.com/Nairinn)
