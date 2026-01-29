# WiFi ISP Backend API

A production-ready FastAPI backend for the WiFi ISP platform with complete configuration.

## Features

- ✅ **App Identity & Metadata** - Title, version, contact, license info
- ✅ **OpenAPI Documentation** - Swagger UI and ReDoc
- ✅ **Versioning** - Semantic versioning (v1.0.0)
- ✅ **Global Middleware** - CORS, logging, request tracking
- ✅ **Router Registration** - Modular endpoint structure
- ✅ **Lifecycle Events** - Startup/shutdown handlers
- ✅ **Exception Handlers** - Custom error responses
- ✅ **Request Logging** - All requests/responses logged with timing

## Quick Start

### 1. Install Dependencies

```powershell
cd "WiFi ISP\Back_End"
pip install -r requirements.txt
```

### 2. Configure Environment

```powershell
copy .env.example .env
# Edit .env with your settings if needed
```

### 3. Run the Server

```powershell
python main.py
```

Or with uvicorn directly:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Documentation
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

### Health & Info
- **GET** `/` - API root with links
- **GET** `/api/health` - Health check
- **GET** `/api/packages` - All available packages
- **GET** `/api/contact` - Contact information

## Architecture

```
main.py
├── Configuration & Metadata
├── Logging Setup
├── Lifespan Events (startup/shutdown)
├── FastAPI App Instantiation
├── Global Middleware Registration
│   ├── CORS
│   └── Request Logging
├── Exception Handlers
│   ├── Custom APIException
│   ├── Validation Errors
│   └── General Exceptions
└── Routers & Endpoints
    ├── Health Check
    ├── Packages
    ├── Contact
    └── Root
```

## Environment Variables

See `.env.example` for all available configuration options.

## Error Handling

The API provides consistent error responses:

```json
{
  "error": true,
  "message": "Error description",
  "timestamp": "2026-01-29T12:34:56.789Z",
  "details": {}
}
```

## Middleware

### CORS
Configured to allow requests from:
- `http://localhost:5173` (React frontend)
- `http://localhost:3000` (Alternative frontend)

### Request Logging
All requests are logged with:
- Method and path
- Client IP
- Response status
- Processing time
- Custom headers

## Extending the App

### Adding New Routers

Create a new router file:

```python
# routers/packages.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/packages", tags=["Packages"])

@router.get("/")
async def list_packages():
    return {"packages": []}

# In main.py:
# from routers import packages
# app.include_router(packages.router)
```

## Development

- Python 3.9+
- FastAPI 0.109+
- Uvicorn for ASGI server

## License

MIT License - See LICENSE file for details
