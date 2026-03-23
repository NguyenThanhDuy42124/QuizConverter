"""
Quiz Converter API - Production Entry Point
Compatible with container deployment
Startup command: python /home/container/app.py
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import FastAPI app from main module
from main import app

if __name__ == "__main__":
    import uvicorn
    
    # Configuration from environment variables or defaults
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    workers = int(os.getenv("API_WORKERS", 1))  # Default 1 for container
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"🚀 Starting Quiz Converter API")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Workers: {workers}")
    print(f"   Debug: {debug}")
    
    # Run with Uvicorn
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers if not debug else 1,
        reload=debug,  # Reload only in debug mode
        log_level="debug" if debug else "info"
    )
