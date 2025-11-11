#!/usr/bin/env python3
"""
AWIES Configuration Wizard
Helps detect and fix LLM API configuration issues
"""

import os
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("🔧 AWIES Configuration Wizard")
    print("=" * 60)
    print()

    # Load current .env
    env_path = Path(__file__).parent / ".env"
    config = {}

    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

    print("📋 Current Configuration:")
    print(f"  Provider: {config.get('LLM_PROVIDER', 'NOT SET')}")
    print(f"  Base URL: {config.get('LLM_BASE_URL', 'NOT SET')}")
    print(f"  Model: {config.get('LLM_MODEL', 'NOT SET')}")
    print(f"  API Key: {'***' + config.get('LLM_API_KEY', 'NOT SET')[-8:] if config.get('LLM_API_KEY', 'NOT SET') != 'your-api-key-here' else 'NOT SET'}")
    print()

    # Detect configuration type based on URL and model
    base_url = config.get('LLM_BASE_URL', '')
    model = config.get('LLM_MODEL', '')
    provider = config.get('LLM_PROVIDER', '')

    issues = []

    # Check for mismatches
    if 'gemini' in model.lower() and provider != 'gemini':
        issues.append("⚠️  Model name contains 'gemini' but provider is not 'gemini'")

    if 'generativelanguage.googleapis.com' in base_url and provider != 'gemini':
        issues.append("⚠️  Using Google API URL but provider is not 'gemini'")

    if provider == 'gemini' and ('/chat/completions' in base_url or 'openai' in base_url.lower()):
        issues.append("⚠️  Provider is 'gemini' but URL looks like OpenAI format")

    if issues:
        print("❌ Configuration Issues Detected:")
        for issue in issues:
            print(f"  {issue}")
        print()

    # Provide recommendations
    print("💡 Configuration Recommendations:")
    print()

    if 'gemini' in model.lower() or 'generativelanguage' in base_url:
        print("Based on your model/URL, you should use Gemini configuration:")
        print()
        print("  LLM_PROVIDER=gemini")
        if 'generativelanguage.googleapis.com' in base_url:
            print(f"  LLM_BASE_URL={base_url}")
        else:
            print("  LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta")
        print(f"  LLM_MODEL={model if 'gemini' in model.lower() else 'gemini-pro'}")
        print("  LLM_API_KEY=your-gemini-api-key")
        print()

    elif '/chat/completions' in base_url or 'openai' in base_url.lower():
        print("Based on your URL, you should use OpenAI-compatible configuration:")
        print()
        print("  LLM_PROVIDER=openai")
        print(f"  LLM_BASE_URL={base_url}")
        print(f"  LLM_MODEL={model if model else 'gpt-3.5-turbo'}")
        print("  LLM_API_KEY=your-api-key")
        print()

    # Special case: Gemini proxy with OpenAI format endpoint
    if 'gemini' in model.lower() and '/chat/completions' in base_url:
        print("⚠️  SPECIAL CASE DETECTED:")
        print("  Your API endpoint uses '/chat/completions' (OpenAI format)")
        print("  But your model is Gemini.")
        print()
        print("  You have two options:")
        print()
        print("  Option 1: Use OpenAI provider (if your proxy converts the format)")
        print("    LLM_PROVIDER=openai")
        print(f"    LLM_BASE_URL={base_url}")
        print(f"    LLM_MODEL={model}")
        print()
        print("  Option 2: Use native Gemini API")
        print("    LLM_PROVIDER=gemini")
        print("    LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta")
        print("    LLM_MODEL=gemini-pro")
        print()

    print("=" * 60)
    print("📝 To apply changes:")
    print("  1. Edit backend/.env file")
    print("  2. Update the LLM_* variables")
    print("  3. Restart the backend server")
    print("=" * 60)

if __name__ == '__main__':
    main()
