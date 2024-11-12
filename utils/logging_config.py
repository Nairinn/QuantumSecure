import structlog
import logging
import sys
from pathlib import Path

def setup_logging(log_file: str = "secure_transfer.log"):
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
    
    # Set up file handler
    log_path = Path(log_file)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    
    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    return structlog.get_logger()
