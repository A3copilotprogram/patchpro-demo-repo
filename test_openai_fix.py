"""
Test script to verify OpenAI client initialization works correctly
Usage: Set OPENAI_API_KEY environment variable before running
"""
import os

# Get API key from environment variable
test_api_key = os.environ.get('OPENAI_API_KEY', 'sk-test-placeholder')

try:
    from openai import OpenAI
    
    print("✅ OpenAI library imported successfully")
    
    # Test initialization with explicit parameters
    client = OpenAI(
        api_key=test_api_key,
        max_retries=2,
        timeout=30.0
    )
    
    print("✅ OpenAI client initialized successfully")
    print(f"✅ Client type: {type(client)}")
    
    # Try a simple API call
    print("\n🔍 Testing API call...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'test successful' in 2 words"}],
        max_tokens=10
    )
    
    print(f"✅ API call successful!")
    print(f"✅ Response: {response.choices[0].message.content}")
    
except ImportError as e:
    print(f"❌ OpenAI library not installed: {e}")
    print("💡 This is expected in development - will install on Render")
    
except Exception as e:
    print(f"❌ Error: {e}")
    if 'proxies' in str(e).lower():
        print("\n⚠️  PROXIES ERROR DETECTED!")
        print("Solution: Update openai library to latest version")
        print("Command: pip install --upgrade 'openai>=1.50.0'")
