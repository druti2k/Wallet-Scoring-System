import time
import hashlib
from typing import Dict, Tuple, Optional
from fastapi import HTTPException, Request
from config import settings
from utils.logger import get_logger
from utils.cache import cache

logger = get_logger(__name__)

class RateLimiter:
    def __init__(self):
        self.minute_limit = settings.rate_limit_per_minute
        self.hour_limit = settings.rate_limit_per_hour
    
    def _get_client_id(self, request: Request) -> str:
        """Get unique client identifier"""
        # Try to get from X-Forwarded-For header first (for proxy setups)
        client_ip = request.headers.get("X-Forwarded-For")
        if not client_ip:
            client_ip = request.client.host
        
        # Add user agent for additional uniqueness
        user_agent = request.headers.get("User-Agent", "")
        
        # Create hash for privacy
        client_id = hashlib.sha256(f"{client_ip}:{user_agent}".encode()).hexdigest()
        return client_id
    
    def _get_rate_limit_keys(self, client_id: str) -> Tuple[str, str]:
        """Get rate limit keys for minute and hour windows"""
        current_minute = int(time.time() // 60)
        current_hour = int(time.time() // 3600)
        
        minute_key = f"rate_limit:minute:{client_id}:{current_minute}"
        hour_key = f"rate_limit:hour:{client_id}:{current_hour}"
        
        return minute_key, hour_key
    
    def check_rate_limit(self, request: Request) -> Dict[str, int]:
        """Check if request is within rate limits"""
        client_id = self._get_client_id(request)
        minute_key, hour_key = self._get_rate_limit_keys(client_id)
        
        # Get current counts
        minute_count = cache.get(minute_key) or 0
        hour_count = cache.get(hour_key) or 0
        
        # Check limits
        if minute_count >= self.minute_limit:
            logger.warning("Rate limit exceeded (minute)", client_id=client_id, count=minute_count)
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": "per minute",
                    "retry_after": 60
                }
            )
        
        if hour_count >= self.hour_limit:
            logger.warning("Rate limit exceeded (hour)", client_id=client_id, count=hour_count)
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": "per hour",
                    "retry_after": 3600
                }
            )
        
        return {
            "minute_count": minute_count,
            "hour_count": hour_count,
            "minute_limit": self.minute_limit,
            "hour_limit": self.hour_limit
        }
    
    def increment_rate_limit(self, request: Request):
        """Increment rate limit counters"""
        client_id = self._get_client_id(request)
        minute_key, hour_key = self._get_rate_limit_keys(client_id)
        
        # Increment counters with appropriate TTL
        current_minute_count = cache.get(minute_key) or 0
        current_hour_count = cache.get(hour_key) or 0
        
        cache.set(minute_key, current_minute_count + 1, 60)  # 1 minute TTL
        cache.set(hour_key, current_hour_count + 1, 3600)   # 1 hour TTL
    
    def get_rate_limit_info(self, request: Request) -> Dict[str, int]:
        """Get current rate limit information for client"""
        client_id = self._get_client_id(request)
        minute_key, hour_key = self._get_rate_limit_keys(client_id)
        
        minute_count = cache.get(minute_key) or 0
        hour_count = cache.get(hour_key) or 0
        
        return {
            "minute_count": minute_count,
            "hour_count": hour_count,
            "minute_limit": self.minute_limit,
            "hour_limit": self.hour_limit,
            "minute_remaining": max(0, self.minute_limit - minute_count),
            "hour_remaining": max(0, self.hour_limit - hour_count)
        }

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit_middleware(request: Request, call_next):
    """FastAPI middleware for rate limiting"""
    try:
        # Check rate limit
        rate_info = rate_limiter.check_rate_limit(request)
        
        # Add rate limit headers to response
        response = call_next(request)
        response.headers["X-RateLimit-Minute-Remaining"] = str(rate_info["minute_limit"] - rate_info["minute_count"])
        response.headers["X-RateLimit-Hour-Remaining"] = str(rate_info["hour_limit"] - rate_info["hour_count"])
        response.headers["X-RateLimit-Minute-Limit"] = str(rate_info["minute_limit"])
        response.headers["X-RateLimit-Hour-Limit"] = str(rate_info["hour_limit"])
        
        # Increment counters after successful request
        rate_limiter.increment_rate_limit(request)
        
        return response
        
    except HTTPException as e:
        # Re-raise HTTP exceptions (like 429)
        raise e
    except Exception as e:
        logger.error("Rate limit middleware error", error=str(e))
        # Continue without rate limiting if there's an error
        return call_next(request) 