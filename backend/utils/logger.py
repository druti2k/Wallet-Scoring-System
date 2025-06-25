import structlog
import logging
import sys
from typing import Any, Dict
from config import settings

def setup_logging():
    """Setup structured logging for the application"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.log_format == "json" else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)

class LoggerMixin:
    """Mixin to add logging capabilities to classes"""
    
    @property
    def logger(self) -> structlog.BoundLogger:
        """Get logger for this class"""
        return get_logger(self.__class__.__name__)

def log_request(request_id: str, method: str, path: str, status_code: int, duration: float):
    """Log HTTP request details"""
    logger = get_logger("http")
    logger.info(
        "HTTP Request",
        request_id=request_id,
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=round(duration * 1000, 2),
    )

def log_error(error: Exception, context: Dict[str, Any] = None):
    """Log error with context"""
    logger = get_logger("error")
    logger.error(
        "Application Error",
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {},
        exc_info=True,
    )

def log_wallet_analysis(wallet_address: str, network: str, score: int, duration: float):
    """Log wallet analysis results"""
    logger = get_logger("wallet_analysis")
    logger.info(
        "Wallet Analysis Complete",
        wallet_address=wallet_address,
        network=network,
        score=score,
        duration_ms=round(duration * 1000, 2),
    )

def log_api_call(api_name: str, success: bool, duration: float, error: str = None):
    """Log external API calls"""
    logger = get_logger("api_calls")
    log_data = {
        "api_name": api_name,
        "success": success,
        "duration_ms": round(duration * 1000, 2),
    }
    if error:
        log_data["error"] = error
    
    if success:
        logger.info("API Call Success", **log_data)
    else:
        logger.error("API Call Failed", **log_data)

# Initialize logging on module import
setup_logging() 