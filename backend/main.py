import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import our modules
from config import settings
from api.routes import router as api_router
from utils.logger import get_logger, log_request, log_error
from utils.rate_limiter import rate_limit_middleware
from utils.monitoring import metrics_middleware, get_metrics, get_health_status, start_system_monitoring
from utils.cache import cache

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Wallet Scoring System", version=settings.app_version, environment=settings.environment)
    
    # Start system monitoring
    start_system_monitoring()
    
    # Test cache connection
    try:
        cache.set("startup_test", "ok", 10)
        logger.info("Cache connection established")
    except Exception as e:
        logger.error("Cache connection failed", error=str(e))
    
    yield
    
    # Shutdown
    logger.info("Shutting down Wallet Scoring System")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered wallet scoring system for fraud detection and risk assessment",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://wallet-scoring-system-ui.onrender.com"
    ],  # Or use ["*"] for all origins (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware for request tracking
@app.middleware("http")
async def request_tracking_middleware(request: Request, call_next):
    """Track request details and timing"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Add request ID to request state
    request.state.request_id = request_id
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Log request
        log_request(
            request_id=request_id,
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            duration=duration
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        log_error(e, {
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "duration": duration
        })
        raise

# Add rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware_wrapper(request: Request, call_next):
    """Rate limiting middleware wrapper"""
    return await rate_limit_middleware(request, call_next)

# Add metrics middleware
@app.middleware("http")
async def metrics_middleware_wrapper(request: Request, call_next):
    """Metrics collection middleware wrapper"""
    return await metrics_middleware(request, call_next)

# Include API routes
app.include_router(api_router, prefix="/api")

# Error handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    log_error(exc, {
        "request_id": getattr(request.state, "request_id", "unknown"),
        "path": str(request.url.path),
        "method": request.method
    })
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "request_id": getattr(request.state, "request_id", "unknown"),
            "timestamp": time.time()
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    log_error(exc, {
        "request_id": getattr(request.state, "request_id", "unknown"),
        "path": str(request.url.path),
        "method": request.method
    })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "request_id": getattr(request.state, "request_id", "unknown"),
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    log_error(exc, {
        "request_id": getattr(request.state, "request_id", "unknown"),
        "path": str(request.url.path),
        "method": request.method
    })
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "request_id": getattr(request.state, "request_id", "unknown"),
            "timestamp": time.time()
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    return get_health_status()

# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return get_metrics()

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
        "docs": "/docs" if settings.debug else None,
        "health": "/health",
        "metrics": "/metrics"
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting development server")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers,
        log_level=settings.log_level.lower()
    )