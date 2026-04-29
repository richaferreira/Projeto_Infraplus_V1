import time
from collections import defaultdict


class RateLimiter:
    """Simple in-memory rate limiter for login attempts."""

    def __init__(self, max_attempts=5, window_seconds=300):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts = defaultdict(list)

    def _cleanup(self, key):
        now = time.time()
        cutoff = now - self.window_seconds
        self._attempts[key] = [t for t in self._attempts[key] if t > cutoff]

    def is_rate_limited(self, key):
        self._cleanup(key)
        return len(self._attempts[key]) >= self.max_attempts

    def record_attempt(self, key):
        self._attempts[key].append(time.time())

    def remaining_attempts(self, key):
        self._cleanup(key)
        return max(0, self.max_attempts - len(self._attempts[key]))

    def reset(self, key):
        self._attempts.pop(key, None)


login_limiter = RateLimiter(max_attempts=5, window_seconds=300)
