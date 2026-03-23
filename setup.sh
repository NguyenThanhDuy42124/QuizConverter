#!/bin/bash
# Setup script for Quiz Converter

echo "=========================================="
echo "Quiz Converter - Setup Script"
echo "=========================================="
echo ""

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Setup Backend
echo "Setting up Backend..."
cd backend

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "✓ Backend setup complete"
echo ""

cd ..

# Setup Frontend
echo "Setting up Frontend..."
cd frontend

if ! command -v node &> /dev/null; then
    echo "⚠ Node.js is not installed. Please install Node.js 14+"
    echo "Visit: https://nodejs.org/"
else
    NODE_VERSION=$(node --version)
    echo "✓ Node.js $NODE_VERSION found"
    
    echo "Installing npm dependencies..."
    npm install
    
    echo "✓ Frontend setup complete"
fi

cd ..
echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your MySQL credentials"
echo "2. Start Backend: cd backend && python main.py"
echo "3. Start Frontend: cd frontend && npm start"
echo ""
