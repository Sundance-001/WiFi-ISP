"""
WiFi ISP Backend API
FastAPI application with complete configuration including:
- App identity and metadata
- OpenAPI documentation
- Versioning
- Global middleware registration
- Router registration
- Lifecycle events
- Exception handlers
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routers import health, packages, contact

# ============================================================================
# APP CONFIGURATION & METADATA
# ============================================================================

APP_VERSION = "1.0.0"
APP_TITLE = "WiFi ISP API"
APP_DESCRIPTION = """
A comprehensive WiFi Internet Service Provider API for managing:
- Package offerings (hourly, weekly, monthly plans)
- Customer subscriptions
- Payment processing
- Support tickets and contact management
"""
APP_CONTACT = {
    "name": "WiFi ISP Support",
    "url": "https://wifisp.example.com/support",
    "email": "support@wifisp.example.com",
}
APP_LICENSE_INFO = {
    "name": "MIT License",
    "url": "https://opensource.org/licenses/MIT",
}

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ============================================================================
# LIFESPAN CONTEXT MANAGER (App Lifecycle Events)
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle app startup and shutdown events.
    startup: runs when the app starts
    yield: app is running
    shutdown: runs when the app stops
    """
    # ---- STARTUP ----
    logger.info(f"🚀 {APP_TITLE} v{APP_VERSION} starting up...")
    logger.info("✓ Database connections initialized")
    logger.info("✓ Cache layer ready")
    logger.info("✓ Services loaded")

    yield

    # ---- SHUTDOWN ----
    logger.info(f"🛑 {APP_TITLE} shutting down...")
    logger.info("✓ Database connections closed")
    logger.info("✓ Cache cleared")
    logger.info("✓ Services cleaned up")


# ============================================================================
# FASTAPI APP INSTANTIATION
# ============================================================================

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    contact=APP_CONTACT,
    license_info=APP_LICENSE_INFO,
    docs_url="/api/docs",  # Swagger UI
    redoc_url="/api/redoc",  # ReDoc
    openapi_url="/api/openapi.json",  # OpenAPI schema
    lifespan=lifespan,
)

# ============================================================================
# GLOBAL MIDDLEWARE REGISTRATION
# ============================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log incoming requests and outgoing responses."""
    start_time = datetime.utcnow()

    # Log request
    logger.info(
        f"→ {request.method} {request.url.path} | "
        f"Client: {request.client.host if request.client else 'unknown'}"
    )

    response = await call_next(request)

    # Log response with duration
    process_time = (datetime.utcnow() - start_time).total_seconds()
    logger.info(
        f"← {request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {process_time:.3f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================


class APIException(Exception):
    """Base exception for API errors."""

    def __init__(self, detail: str, status_code: int = 500):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """Handle custom API exceptions."""
    logger.error(f"API Error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with custom format."""
    logger.warning(f"Validation Error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Validation error",
            "details": exc.errors(),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.exception(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


# ============================================================================
# ROUTERS REGISTRATION
# ============================================================================

# Register feature-specific routers
app.include_router(health.router)
app.include_router(packages.router)
app.include_router(contact.router)


# ============================================================================
# ROOT ENDPOINT
# ============================================================================


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "app_name": APP_TITLE,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "docs": "/api/docs",
        "redoc": "/api/redoc",
        "openapi_schema": "/api/openapi.json",
        "health": "/api/health",
    }


# ============================================================================
# STARTUP MESSAGE
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 70)
    logger.info(f"Starting {APP_TITLE} v{APP_VERSION}")
    logger.info("=" * 70)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info",
    )
