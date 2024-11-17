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

**Installation**

Install required packages:

pip install -r requirements.txt

**Setup**

First, initialize the server configuration:

python3 scripts/setup_server.py

Create a user account:

python3 scripts/create_user.py --username <your-username>

Start the server:

python3 server/server.py

Using the Client
To transfer a file:
python3 client/client.py --username <your-username> <path-to-file>

Additional options:

--host: Server hostname (default: localhost)
--port: Server port (default: 8443)

Configuration
Default settings in config.py:

Max file size: 100MB
Rate limit: 10 requests per minute
Token expiry: 1 hour
Maximum login attempts: 3
Lockout period: 5 minutes


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

## Testing


python -m unittest tests/test_security.py


## Error Handling

- Authentication failures
- File integrity violations
- Size limit exceedance
- Rate limit violations
- Network timeouts
- File handling errors

## Author

Naing Lynn Kyaw
- GitHub: [@Nairinn](https://github.com/Nairinn)
