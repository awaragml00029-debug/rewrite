#!/usr/bin/env python3
"""Test script to verify LLM API configuration and response."""

import asyncio
import sys
from openai import AsyncOpenAI
from app.core.config import settings

async def test_api():
    """Test the LLM API with current configuration."""
    print("=" * 60)
    print("LLM API Configuration Test")
    print("=" * 60)
    print(f"Provider: {settings.llm_provider}")
    print(f"Model: {settings.llm_model}")
    print(f"Base URL: {settings.llm_base_url}")
    print(f"API Key: {settings.llm_api_key[:10]}..." if settings.llm_api_key else "Not set")
    print("=" * 60)

    if settings.llm_provider != "openai":
        print("\n⚠️  This test only works with OpenAI-compatible APIs")
        return

    client = AsyncOpenAI(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url if settings.llm_base_url else None
    )

    test_text = "The quick brown fox jumps over the lazy dog. This is a test sentence with some minor grammar issues that needs correcting."

    print("\nTest 1: Simple correction task")
    print(f"Input text: {test_text}")
    print("\nSending request...")

    try:
        # Test without temperature parameter
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "user", "content": f"Correct the grammar in this text:\n\n{test_text}"}
            ],
            max_tokens=4000
        )

        content = response.choices[0].message.content
        print(f"\n✅ Success!")
        print(f"Response length: {len(content) if content else 0} characters")
        print(f"Response preview: {content[:200] if content else '(empty)'}...")

        if not content or len(content) == 0:
            print("\n⚠️  WARNING: API returned empty response!")
            print("This indicates the model may not be suitable for this task.")
            print("\nRecommended models for OhMyGPT:")
            print("  - gpt-4o")
            print("  - gemini-2.0-flash-001")
            return False

        print("\nTest 2: Testing with temperature parameter")
        try:
            response2 = await client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "user", "content": f"Improve this text:\n\n{test_text}"}
                ],
                temperature=0.5,
                max_tokens=4000
            )
            content2 = response2.choices[0].message.content
            print(f"✅ Temperature parameter supported")
            print(f"Response length: {len(content2) if content2 else 0} characters")
        except Exception as e:
            if "temperature" in str(e).lower():
                print(f"⚠️  Model does not support custom temperature parameter")
                print(f"Error: {e}")
            else:
                raise

        print("\n" + "=" * 60)
        print("✅ Configuration appears to be working!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if API key is correct")
        print("2. Verify base URL is accessible")
        print("3. Confirm model name is supported by your API provider")
        print("4. See .env.recommended for suggested configuration")
        return False

if __name__ == "__main__":
    sys.path.insert(0, "/home/user/rewrite/backend")
    result = asyncio.run(test_api())
    sys.exit(0 if result else 1)
