#!/bin/bash
# Quick test script to check which Gemini model works
# Run: bash test_models.sh

cd /home/container

echo "Testing Gemini models with your API key..."
echo "==========================================="

# Load .env
export $(cat .env.local | grep GEMINI_API_KEY)

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY not found in .env.local"
    exit 1
fi

echo "✅ API Key loaded"
echo ""

# Test mỗi model với Python one-liner
echo "Testing models:"
python3 << 'EOF'
import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

models = ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash"]

for model in models:
    try:
        print(f"🔍 {model}...", end=" ", flush=True)
        response = client.models.generate_content(
            model=model,
            contents="Test"
        )
        print("✅ WORKS")
    except Exception as e:
        if "404" in str(e):
            print("❌ 404")
        else:
            print(f"❌ Error: {type(e).__name__}")

EOF

echo ""
echo "==========================================="
