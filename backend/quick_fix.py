#!/usr/bin/env python3
"""
Quick fix script for common AWIES issues
"""

import os
import sys
from pathlib import Path

def fix_env_file():
    """Fix .env configuration"""
    env_file = Path(__file__).parent / ".env"

    print("🔧 Checking .env configuration...")

    if not env_file.exists():
        print("❌ .env file not found!")
        print("  Creating from .env.working template...")
        working_template = Path(__file__).parent / ".env.working"
        if working_template.exists():
            import shutil
            shutil.copy(working_template, env_file)
            print("✅ Created .env file")
            print("  📝 Please edit .env and configure your API key!")
        return False

    # Read current config
    with open(env_file) as f:
        content = f.read()

    # Check for common issues
    issues = []

    if "your-api-key-here" in content:
        issues.append("API key not set")

    if "LLM_PROVIDER=openai" in content and "gemini" in content.lower():
        issues.append("Provider/model mismatch (openai provider with gemini model)")

    if issues:
        print("⚠️  Configuration issues found:")
        for issue in issues:
            print(f"  - {issue}")
        print()
        print("💡 Quick fixes:")
        print("  1. If using Gemini API:")
        print("     LLM_PROVIDER=gemini")
        print("     LLM_BASE_URL=https://your-api-endpoint (WITHOUT /chat/completions)")
        print("     LLM_MODEL=gemini-2.5-flash")
        print()
        print("  2. If using OpenAI API:")
        print("     LLM_PROVIDER=openai")
        print("     LLM_BASE_URL=https://api.openai.com/v1")
        print("     LLM_MODEL=gpt-3.5-turbo")
        print()
        return False

    print("✅ .env configuration looks OK")
    return True

def test_jane_api():
    """Test JANE API connectivity"""
    print("\n🔍 Testing JANE API...")

    try:
        import socket
        host = "jane.biosemantics.org"
        port = 8080

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            print(f"✅ JANE API ({host}:{port}) is reachable")
            return True
        else:
            print(f"❌ JANE API ({host}:{port}) is not reachable")
            print("   This is normal - JANE is an external service that may be unavailable")
            print("   The system will work without it (recommendations will be empty)")
            return False
    except Exception as e:
        print(f"⚠️  Could not test JANE API: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n📦 Checking dependencies...")

    required = [
        ('fastapi', 'FastAPI'),
        ('openai', 'OpenAI SDK'),
        ('httpx', 'HTTPX'),
        ('spacy', 'spaCy'),
        ('textstat', 'textstat'),
    ]

    missing = []
    for module, name in required:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} (missing)")
            missing.append(module)

    if missing:
        print()
        print("⚠️  Missing dependencies. Install with:")
        print(f"  pip install {' '.join(missing)}")
        return False

    return True

def main():
    print("=" * 60)
    print("🚀 AWIES Quick Fix Utility")
    print("=" * 60)
    print()

    all_ok = True

    # Check dependencies
    if not check_dependencies():
        all_ok = False

    # Fix .env
    if not fix_env_file():
        all_ok = False

    # Test JANE API
    test_jane_api()  # Don't fail on this

    print()
    print("=" * 60)

    if all_ok:
        print("✅ All checks passed!")
        print()
        print("Next steps:")
        print("  1. Make sure your API key is configured in .env")
        print("  2. Restart the backend server")
        print("  3. Try the enhancement again")
    else:
        print("⚠️  Some issues need attention")
        print()
        print("Please fix the issues above and restart the server")

    print("=" * 60)

if __name__ == '__main__':
    main()
