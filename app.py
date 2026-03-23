"""
Quiz Converter – Entry point for PikaMC / Pterodactyl Python Egg hosting.

This script:
1. Syncs code from GitHub (git fetch + reset --hard)
2. Installs Python dependencies from requirements.txt
3. Starts the FastAPI server via uvicorn

Pterodactyl auto-installs requirements.txt, then runs this file.
"""
import subprocess
import sys
import os

# ── Force sync with GitHub (fixes Pterodactyl git pull conflicts) ──
project_root = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(os.path.join(project_root, ".git")):
    print("==> Syncing code from GitHub...")
    try:
        subprocess.run(["git", "fetch", "origin"], cwd=project_root, timeout=30)
        subprocess.run(["git", "reset", "--hard", "origin/main"], cwd=project_root, timeout=30)
        print("==> Code synced successfully!")
    except Exception as e:
        print(f"==> Git sync skipped: {e}")

# Get port from environment variable (Pterodactyl sets SERVER_PORT or PORT)
port = os.environ.get("SERVER_PORT") or os.environ.get("PORT") or "8000"

# Start FastAPI server from the project root
print(f"==> Starting Quiz Converter API on port {port}...")
subprocess.call([
    sys.executable, "-m", "uvicorn",
    "main:app",
    "--host", "0.0.0.0",
    "--port", str(port),
])
