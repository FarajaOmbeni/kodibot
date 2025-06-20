#!/usr/bin/env python3
"""
Health check script for KodiBOT deployment debugging
"""

import sys
import os
import requests
import time
from datetime import datetime

def check_health():
    """Check if the KodiBOT API is responding"""
    
    # Configuration
    host = os.getenv("HOST", "localhost")
    port = os.getenv("PORT", "8000")
    base_url = f"http://{host}:{port}"
    
    print(f"🔍 Checking KodiBOT health at {base_url}")
    print(f"⏰ Time: {datetime.now()}")
    print("-" * 50)
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check: PASSED")
            print(f"📊 Status: {data.get('status', 'Unknown')}")
            print(f"💬 Message: {data.get('message', 'No message')}")
            return True
        else:
            print(f"❌ Health check: FAILED")
            print(f"🔢 Status Code: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print("❌ Connection Error: Can't connect to the server")
        print(f"🔗 URL: {base_url}")
        print(f"💡 Check if the server is running and accessible")
        return False
        
    except requests.exceptions.Timeout as e:
        print("⏱️ Timeout Error: Server didn't respond in time")
        print(f"💡 Server might be overloaded or starting up")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    print("\n🔧 Checking dependencies...")
    
    required_modules = [
        "fastapi",
        "uvicorn", 
        "sqlalchemy",
        "openai",
        "pydantic"
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}: Available")
        except ImportError:
            print(f"❌ {module}: Missing")
            return False
    
    return True

def check_environment():
    """Check environment variables"""
    print("\n🌍 Environment variables:")
    
    env_vars = [
        "OPENAI_API_KEY",
        "DATABASE_URL", 
        "HOST",
        "PORT",
        "ENVIRONMENT"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Hide sensitive values
            if "API_KEY" in var or "PASSWORD" in var:
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"⚠️  {var}: Not set")

def main():
    """Main health check function"""
    print("🏥 KodiBOT Health Checker")
    print("=" * 50)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check environment
    check_environment()
    
    # Check health
    health_ok = check_health()
    
    # Summary
    print("\n📋 Summary:")
    print(f"Dependencies: {'✅ OK' if deps_ok else '❌ FAILED'}")
    print(f"Health Check: {'✅ OK' if health_ok else '❌ FAILED'}")
    
    if health_ok:
        print("\n🎉 KodiBOT is healthy and ready!")
        sys.exit(0)
    else:
        print("\n🚨 KodiBOT has issues that need attention")
        sys.exit(1)

if __name__ == "__main__":
    main() 