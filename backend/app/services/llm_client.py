"""LLM Client - Universal adapter for OpenAI and Gemini APIs."""

import logging
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import httpx
from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate text completion."""
        pass

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate chat completion."""
        pass


class OpenAIClient(LLMClient):
    """OpenAI-compatible API client (works with OpenAI, Azure, local models, etc.)."""

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url if settings.llm_base_url else None
        )
        self.model = settings.llm_model
        logger.info(f"Initialized OpenAI client with model: {self.model}")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate text completion using chat endpoint."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        return await self.chat(messages, temperature, max_tokens)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate chat completion."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise


class GeminiClient(LLMClient):
    """Google Gemini API client."""

    def __init__(self):
        self.api_key = settings.llm_api_key
        self.base_url = settings.llm_base_url
        self.model = settings.llm_model
        self.client = httpx.AsyncClient(timeout=60.0)
        logger.info(f"Initialized Gemini client with model: {self.model}")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate text completion."""
        # Gemini uses a different format
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        try:
            url = f"{self.base_url}/models/{self.model}:generateContent"

            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                }
            }

            response = await self.client.post(
                url,
                json=payload,
                params={"key": self.api_key}
            )
            response.raise_for_status()

            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate chat completion (converted to Gemini format)."""
        # Convert OpenAI-style messages to Gemini format
        gemini_contents = []
        system_prompt = None

        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            elif msg["role"] == "user":
                gemini_contents.append({
                    "role": "user",
                    "parts": [{"text": msg["content"]}]
                })
            elif msg["role"] == "assistant":
                gemini_contents.append({
                    "role": "model",
                    "parts": [{"text": msg["content"]}]
                })

        try:
            url = f"{self.base_url}/models/{self.model}:generateContent"

            # If there's a system prompt, prepend it to the first user message
            if system_prompt and gemini_contents:
                first_user_msg = gemini_contents[0]
                if first_user_msg["role"] == "user":
                    first_user_msg["parts"][0]["text"] = (
                        f"{system_prompt}\n\n{first_user_msg['parts'][0]['text']}"
                    )

            payload = {
                "contents": gemini_contents,
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                }
            }

            response = await self.client.post(
                url,
                json=payload,
                params={"key": self.api_key}
            )
            response.raise_for_status()

            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()


def get_llm_client() -> LLMClient:
    """Factory function to get the appropriate LLM client."""
    if settings.llm_provider == "openai":
        return OpenAIClient()
    elif settings.llm_provider == "gemini":
        return GeminiClient()
    else:
        raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
