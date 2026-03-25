#!/usr/bin/env python3
"""
Test script to check available Gemini models for your API key
"""

import os
from pathlib import Path

# Load environment
try:
    from dotenv import load_dotenv
    local_env = Path(__file__).parent / ".env.local"
    if local_env.exists():
        load_dotenv(local_env)
except:
    pass

# Import SDK
try:
    from google import genai
    print("✅ google-genai SDK imported successfully\n")
except ImportError as e:
    print(f"❌ Failed to import google-genai: {e}")
    print("Install: pip install google-genai")
    exit(1)

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not set in .env.local")
    exit(1)

print(f"✅ API Key found (length: {len(api_key)})\n")

# Test models one by one
models_to_test = [
    "gemini-2.0-flash",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-pro",
    "gemini-pro-vision",
    "models/gemini-2.0-flash",
    "models/gemini-1.5-pro",
    "models/gemini-1.5-flash",
]

print("Testing models:")
print("-" * 60)

try:
    client = genai.Client(api_key=api_key)
    print("✅ Client initialized\n")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    exit(1)

working_models = []

for model_name in models_to_test:
    try:
        print(f"🔍 Testing {model_name}...", end=" ")
        response = client.models.generate_content(
            model=model_name,
            contents="Hello"
        )
        print("✅ WORKS")
        working_models.append(model_name)
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print("❌ 404 Not Found")
        elif "not supported" in error_msg:
            print("❌ Not Supported")
        elif "permission" in error_msg.lower():
            print("❌ Permission Denied")
        else:
            print(f"❌ {type(e).__name__}")

print("\n" + "=" * 60)
if working_models:
    print(f"✅ Working models ({len(working_models)}):")
    for m in working_models:
        print(f"   - {m}")
else:
    print("❌ No working models found!")
    print("\nTroubleshooting:")
    print("1. Check if API key is valid")
    print("2. Check if API key has quota remaining")
    print("3. Check Google Cloud Console for API restrictions")
print("=" * 60)
