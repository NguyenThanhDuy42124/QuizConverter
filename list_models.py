#!/usr/bin/env python3
"""
List all available Gemini models for your API key
Uses the new google-genai SDK
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

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not set in .env.local")
    exit(1)

print(f"✅ API Key loaded (length: {len(api_key)})\n")

try:
    from google import genai
    print("Using: google-genai (new SDK)\n")
except ImportError:
    print("❌ google-genai not installed!")
    print("Install: pip install google-genai")
    exit(1)

try:
    client = genai.Client(api_key=api_key)
    
    print("=" * 60)
    print("Models available for generateContent:")
    print("=" * 60)
    
    # List all available models
    try:
        models = client.models.list()
        working_models = []
        
        for model in models:
            # Check if model supports generateContent
            if hasattr(model, 'supported_generation_methods'):
                methods = model.supported_generation_methods
                if isinstance(methods, list) and 'generateContent' in methods:
                    model_name = model.name.replace('models/', '')
                    working_models.append(model_name)
                    print(f"✅ {model_name}")
        
        print("=" * 60)
        print(f"\nTotal working models: {len(working_models)}\n")
        
        if working_models:
            print("Recommended (from fastest to most capable):")
            print("1. gemini-2.0-flash (fast + logic)")
            print("2. gemini-1.5-pro (powerful)")
            print("3. gemini-1.5-flash (balanced)")
            
            if working_models:
                print(f"\nYour API actually supports:")
                for m in working_models:
                    print(f"  • {m}")
        else:
            print("❌ No models found! Check your API key.")
    
    except Exception as e:
        print(f"Error listing models: {e}")
        print("\nTrying to test individual models...")
        
        test_models = [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro",
            "gemini-2.0-flash"
        ]
        
        working = []
        for model_name in test_models:
            try:
                print(f"Testing {model_name}...", end=" ", flush=True)
                response = client.models.generate_content(
                    model=model_name,
                    contents="Test"
                )
                print("✅ WORKS")
                working.append(model_name)
            except Exception as err:
                if "404" in str(err):
                    print("❌ 404")
                else:
                    print(f"❌ {type(err).__name__}")
        
        print(f"\n\nWorking models: {working if working else 'None'}")

except Exception as e:
    print(f"❌ Error: {e}")
