import time
import psutil
import threading
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

WALLET_ANALYSIS_COUNT = Counter(
    'wallet_analysis_total',
    'Total wallet analysis requests',
    ['network', 'status']
)

WALLET_ANALYSIS_DURATION = Histogram(
    'wallet_analysis_duration_seconds',
    'Wallet analysis duration in seconds',
    ['network']
)

API_CALL_COUNT = Counter(
    'external_api_calls_total',
    'Total external API calls',
    ['api_name', 'status']
)

API_CALL_DURATION = Histogram(
    'external_api_call_duration_seconds',
    'External API call duration in seconds',
    ['api_name']
)

SYSTEM_MEMORY_USAGE = Gauge(
    'system_memory_usage_bytes',
    'System memory usage in bytes'
)

SYSTEM_CPU_USAGE = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage'
)

CACHE_HIT_RATIO = Gauge(
    'cache_hit_ratio',
    'Cache hit ratio'
)

class SystemMonitor:
    def __init__(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self._lock = threading.Lock()
    
    def record_cache_hit(self):
        """Record a cache hit"""
        with self._lock:
            self.cache_hits += 1
            self._update_cache_metrics()
    
    def record_cache_miss(self):
        """Record a cache miss"""
        with self._lock:
            self.cache_misses += 1
            self._update_cache_metrics()
    
    def _update_cache_metrics(self):
        """Update cache hit ratio metric"""
        total = self.cache_hits + self.cache_misses
        if total > 0:
            hit_ratio = self.cache_hits / total
            CACHE_HIT_RATIO.set(hit_ratio)
    
    def update_system_metrics(self):
        """Update system metrics"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            SYSTEM_MEMORY_USAGE.set(memory.used)
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            SYSTEM_CPU_USAGE.set(cpu_percent)
            
        except Exception as e:
            logger.error("Error updating system metrics", error=str(e))

# Global monitor instance
system_monitor = SystemMonitor()

async def metrics_middleware(request: Request, call_next):
    """FastAPI middleware for metrics collection"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Record metrics
    duration = time.time() - start_time
    endpoint = request.url.path
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=endpoint
    ).observe(duration)
    
    return response

def get_metrics():
    """Get Prometheus metrics"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

def get_health_status() -> Dict[str, Any]:
    """Get comprehensive health status"""
    try:
        # System health
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        disk = psutil.disk_usage('/')
        
        # Cache health
        cache_total = system_monitor.cache_hits + system_monitor.cache_misses
        cache_hit_ratio = system_monitor.cache_hits / cache_total if cache_total > 0 else 0
        
        health_status = {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.app_version,
            "environment": settings.environment,
            "system": {
                "memory_usage_percent": memory.percent,
                "cpu_usage_percent": cpu_percent,
                "disk_usage_percent": (disk.used / disk.total) * 100,
                "memory_available_gb": memory.available / (1024**3),
                "disk_available_gb": disk.free / (1024**3)
            },
            "cache": {
                "hits": system_monitor.cache_hits,
                "misses": system_monitor.cache_misses,
                "hit_ratio": cache_hit_ratio
            },
            "dependencies": {
                "redis": _check_redis_health(),
                "database": _check_database_health(),
                "external_apis": _check_external_apis_health()
            }
        }
        
        # Determine overall health
        if (memory.percent > 90 or cpu_percent > 90 or 
            health_status["dependencies"]["redis"] == "unhealthy" or
            health_status["dependencies"]["database"] == "unhealthy"):
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }

def _check_redis_health() -> str:
    """Check Redis health"""
    try:
        from utils.cache import cache
        # Try a simple operation
        test_key = "health_check_test"
        cache.set(test_key, "test", 10)
        result = cache.get(test_key)
        cache.delete(test_key)
        
        if result == "test":
            return "healthy"
        else:
            return "unhealthy"
    except Exception:
        return "unhealthy"

def _check_database_health() -> str:
    """Check database health"""
    try:
        # TODO: Implement actual database health check
        # For now, return healthy
        return "healthy"
    except Exception:
        return "unhealthy"

def _check_external_apis_health() -> Dict[str, str]:
    """Check external APIs health"""
    api_status = {}
    
    # Check if API keys are configured
    if settings.etherscan_api_key:
        api_status["etherscan"] = "configured"
    else:
        api_status["etherscan"] = "not_configured"
    
    if settings.alchemy_api_key:
        api_status["alchemy"] = "configured"
    else:
        api_status["alchemy"] = "not_configured"
    
    if settings.openai_api_key:
        api_status["openai"] = "configured"
    else:
        api_status["openai"] = "not_configured"
    
    return api_status

def start_system_monitoring():
    """Start background system monitoring"""
    def monitor_loop():
        while True:
            try:
                system_monitor.update_system_metrics()
                time.sleep(60)  # Update every minute
            except Exception as e:
                logger.error("System monitoring error", error=str(e))
                time.sleep(60)
    
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    logger.info("System monitoring started") 