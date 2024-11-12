import time
from collections import defaultdict
import threading

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
        
    def is_allowed(self, client_id: str) -> bool:
        with self.lock:
            now = time.time()
            client_requests = self.requests[client_id]
            
            # Remove old requests
            while client_requests and client_requests[0] < now - self.time_window:
                client_requests.pop(0)
            
            # Check if limit exceeded
            if len(client_requests) >= self.max_requests:
                return False
            
            # Add new request
            client_requests.append(now)
            return True
