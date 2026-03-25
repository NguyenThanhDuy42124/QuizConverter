#!/usr/bin/env python3
"""
Setup script to create .env.local file with API keys
Allows user to configure sensitive data locally without pushing to Git
"""

import os
import sys
from pathlib import Path


def setup_env_local():
    """Create .env.local file with user input"""
    
    env_local_path = Path(__file__).parent / ".env.local"
    
    print("=" * 60)
    print("🔧 Quiz Converter - Environment Setup")
    print("=" * 60)
    print()
    
    # Check if .env.local already exists
    if env_local_path.exists():
        print(f"📁 Found existing .env.local at {env_local_path}")
        response = input("Overwrite it? (y/n): ").strip().lower()
        if response != 'y':
            print("❌ Setup cancelled.")
            return False
    
    print()
    print("Please provide the following configuration:")
    print()
    
    # Get Gemini API Key
    print("🔑 Google Gemini API Key")
    print("   Get it from: https://aistudio.google.com/app/apikey")
    gemini_key = input("   Enter Gemini API Key (or press Enter to skip): ").strip()
    
    # Get other optional configs
    print()
    print("📊 Optional Configuration (press Enter to skip):")
    api_host = input("   API Host [0.0.0.0]: ").strip() or "0.0.0.0"
    api_port = input("   API Port [8000]: ").strip() or "8000"
    debug = input("   Debug Mode [False]: ").strip() or "False"
    
    # Create .env.local content
    env_content = f"""# Local Environment Configuration
# This file is NOT tracked by Git - store sensitive data here only

# Google Gemini API
GEMINI_API_KEY={gemini_key if gemini_key else "your-gemini-api-key-here"}

# FastAPI Server
DEBUG={debug}
API_HOST={api_host}
API_PORT={api_port}

# Database (SQLite)
DATABASE_URL=sqlite+aiosqlite:///./quiz_converter.db

# File Upload
TEMP_DIR=./temp
MAX_FILE_SIZE=52428800

# Logging
LOG_LEVEL=INFO
"""
    
    # Write file
    try:
        with open(env_local_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print()
        print("=" * 60)
        print(f"✅ Success! Created .env.local")
        print(f"📍 Location: {env_local_path}")
        print("=" * 60)
        print()
        
        if not gemini_key:
            print("⚠️  WARNING: Gemini API Key is not set!")
            print("   Please open .env.local and add your API key:")
            print(f"   GEMINI_API_KEY=your-actual-key")
            print()
        else:
            print("✅ Gemini API Key is configured!")
        
        print("🚀 You can now run the application:")
        print("   python main.py")
        print()
        
        return True
        
    except Exception as e:
        print()
        print(f"❌ Error creating .env.local: {e}")
        return False


if __name__ == "__main__":
    success = setup_env_local()
    sys.exit(0 if success else 1)
