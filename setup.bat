@echo off
REM Setup script for Quiz Converter on Windows

echo ==========================================
echo Quiz Converter - Setup Script (Windows)
echo ==========================================
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.10+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo ✓ Backend setup complete
echo.

cd ..

REM Setup Frontend
echo Setting up Frontend...
cd frontend

where node >nul 2>&1
if errorlevel 1 (
    echo ⚠ Node.js is not installed. Please install Node.js 14+
    echo Visit: https://nodejs.org/
) else (
    for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✓ Node.js !NODE_VERSION! found
    
    echo Installing npm dependencies...
    call npm install
    
    echo ✓ Frontend setup complete
)

cd ..
echo.
echo ==========================================
echo ✓ Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Update backend\.env with your MySQL credentials
echo 2. Start Backend: cd backend ^& python main.py
echo 3. Start Frontend: cd frontend ^& npm start
echo.
pause
