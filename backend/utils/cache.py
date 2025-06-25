import redis
import json
import pickle
from typing import Any, Optional, Union
from datetime import timedelta
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class RedisCache:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)
        self.default_ttl = settings.cache_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            logger.error("Cache get error", key=key, error=str(e))
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL"""
        try:
            serialized_value = pickle.dumps(value)
            ttl = ttl or self.default_ttl
            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error("Cache set error", key=key, error=str(e))
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error("Cache delete error", key=key, error=str(e))
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error("Cache exists error", key=key, error=str(e))
            return False
    
    def get_ttl(self, key: str) -> int:
        """Get remaining TTL for key"""
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            logger.error("Cache TTL error", key=key, error=str(e))
            return -1
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error("Cache clear pattern error", pattern=pattern, error=str(e))
            return 0

# Global cache instance
cache = RedisCache()

def cache_wallet_analysis(wallet_address: str, network: str, data: dict, ttl: int = 3600):
    """Cache wallet analysis results"""
    key = f"wallet_analysis:{network}:{wallet_address}"
    return cache.set(key, data, ttl)

def get_cached_wallet_analysis(wallet_address: str, network: str) -> Optional[dict]:
    """Get cached wallet analysis results"""
    key = f"wallet_analysis:{network}:{wallet_address}"
    return cache.get(key)

def cache_transaction_data(wallet_address: str, network: str, data: dict, ttl: int = 1800):
    """Cache transaction data"""
    key = f"transactions:{network}:{wallet_address}"
    return cache.set(key, data, ttl)

def get_cached_transaction_data(wallet_address: str, network: str) -> Optional[dict]:
    """Get cached transaction data"""
    key = f"transactions:{network}:{wallet_address}"
    return cache.get(key)

def cache_defi_data(wallet_address: str, data: dict, ttl: int = 1800):
    """Cache DeFi activity data"""
    key = f"defi_activity:{wallet_address}"
    return cache.set(key, data, ttl)

def get_cached_defi_data(wallet_address: str) -> Optional[dict]:
    """Get cached DeFi activity data"""
    key = f"defi_activity:{wallet_address}"
    return cache.get(key)

def invalidate_wallet_cache(wallet_address: str, network: str):
    """Invalidate all cache entries for a wallet"""
    patterns = [
        f"wallet_analysis:{network}:{wallet_address}",
        f"transactions:{network}:{wallet_address}",
        f"defi_activity:{wallet_address}"
    ]
    
    for pattern in patterns:
        cache.clear_pattern(pattern) 