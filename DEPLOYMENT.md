# Quiz Converter - Deployment Guide

## Container Deployment

This application is designed to run in container environments (Docker, etc.) with the following startup command:

```bash
python /home/container/app.py
```

### Directory Structure for Container

```
/home/container/
├── app.py                    # Entry point (MAIN FILE)
├── main.py                   # FastAPI application logic
├── database.py               # Database configuration
├── models.py                 # SQLAlchemy models
├── schemas.py                # Pydantic schemas
├── converter.py              # HTML parsing and Word generation
├── combinatorics.py          # Quiz shuffling logic
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
└── temp/                     # Temporary file storage (auto-created)
```

## Startup Process

### 1. From Your Host
Your host startup script does:
```bash
git pull                          # Update code from repository
pip install -r requirements.txt   # Install Python dependencies
python /home/container/app.py    # Start the application
```

### 2. What app.py Does
- Loads environment variables from `.env` file
- Imports FastAPI app from `main.py`
- Starts Uvicorn ASGI server with configuration:
  - Host: 0.0.0.0 (listens on all interfaces)
  - Port: 8000 (configurable via `API_PORT` env var)
  - Workers: 1 (for container compatibility)
  - No reload: Production mode (unless DEBUG=True)

## Configuration

### Environment Variables (.env file)

Update `.env` file before deployment:

```bash
# Server
DEBUG=False                    # Set to False for production
API_PORT=8000                  # Port to listen on
API_WORKERS=1                  # Number of workers (1 for containers)

# Database (SQLite by default - no external DB needed)
DATABASE_URL=sqlite+aiosqlite:///./quiz_converter.db

# CORS (Update for your domain)
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]

# Security (Change these!)
SECRET_KEY=your-production-secret-key-here
ALGORITHM=HS256
```

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Update `CORS_ORIGINS` with your domain
- [ ] Change `SECRET_KEY` to a strong random string
- [ ] Ensure `temp/` directory is writable
- [ ] Database file location is persistent (not on ephemeral storage)

## API Endpoints

Once running, access the API:

- **Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc` (Alternative docs)
- **Convert Quiz**: `POST /api/convert/`
- **Download Word**: `GET /api/download/{file_id}`
- **History**: `GET /api/history/`
- **Health Check**: `GET /api/health/`

## Database

The application uses **SQLite** by default, which:
- ✅ Requires no external database server
- ✅ Stores data in a single file (`quiz_converter.db`)
- ✅ Is perfect for containers
- ✅ Auto-creates tables on first run

## Troubleshooting

### Port Already in Use
```bash
# Change PORT in .env:
API_PORT=9000
```

### Database Locked
```bash
# SQLite uses file locking. If you get lock errors:
# 1. Ensure only one Python process is running
# 2. Check that API_WORKERS=1 in .env
```

### Missing Dependencies
```bash
# Reinstall dependencies:
pip install -U --prefix .local -r requirements.txt
```

### CORS Errors from Frontend
```bash
# Update CORS_ORIGINS in .env:
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]
# Restart the application
```

## Performance Notes

- Single worker (API_WORKERS=1) is recommended for container environments
- SQLite performs well for moderate traffic (< 100 concurrent users)
- Temp files are stored on disk - ensure sufficient space
- Word document generation is fast (~100ms per document)

## Monitoring

The application logs to stdout:
```
🚀 Starting Quiz Converter API
   Host: 0.0.0.0
   Port: 8000
   Workers: 1
   Debug: False
```

Access logs will show all API requests for monitoring purposes.
