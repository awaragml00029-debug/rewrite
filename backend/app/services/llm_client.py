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
            content = response.choices[0].message.content
            if content is None:
                logger.warning(f"API returned None content. Response: {response}")
                return ""
            result = content.strip()
            logger.info(f"OpenAI API response: {len(result)} characters")
            return result
        except Exception as e:
            error_str = str(e)
            # Check if error is about unsupported temperature parameter
            if "temperature" in error_str.lower() and ("unsupported" in error_str.lower() or "does not support" in error_str.lower()):
                logger.warning(f"Model {self.model} does not support custom temperature, retrying with default value")
                try:
                    # Retry without temperature parameter (will use API default)
                    response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=max_tokens
                    )
                    content = response.choices[0].message.content
                    if content is None:
                        logger.warning(f"API returned None content on retry. Response: {response}")
                        return ""
                    result = content.strip()
                    logger.info(f"OpenAI API retry success: received {len(result)} characters")
                    return result
                except Exception as retry_e:
                    logger.error(f"OpenAI API error on retry: {retry_e}")
                    raise
            else:
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

            # Try to parse response in multiple formats
            return self._parse_response(data)

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

            # Try to parse response in multiple formats
            return self._parse_response(data)

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    def _parse_response(self, data: Dict[str, Any]) -> str:
        """Parse Gemini API response with support for multiple formats."""
        logger.debug(f"Parsing Gemini response. Top-level keys: {list(data.keys())}")

        # Format 1: Standard Gemini API format
        # {"candidates": [{"content": {"parts": [{"text": "..."}]}}]}
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            logger.debug("Parsed using standard Gemini format")
            return text.strip()
        except (KeyError, IndexError, TypeError) as e:
            logger.debug(f"Standard format failed: {e}")

        # Format 2: OpenAI-compatible format (some proxies)
        # {"choices": [{"message": {"content": "..."}}]}
        try:
            text = data["choices"][0]["message"]["content"]
            logger.debug("Parsed using OpenAI-compatible format")
            return text.strip()
        except (KeyError, IndexError, TypeError) as e:
            logger.debug(f"OpenAI format failed: {e}")

        # Format 3: Direct text field
        # {"text": "..."}
        if "text" in data and isinstance(data["text"], str):
            logger.debug("Parsed using direct text format")
            return data["text"].strip()

        # Format 4: Simple content field
        # {"content": "..."}
        if "content" in data:
            if isinstance(data["content"], str):
                logger.debug("Parsed using direct content format")
                return data["content"].strip()
            elif isinstance(data["content"], dict) and "text" in data["content"]:
                logger.debug("Parsed using nested content.text format")
                return data["content"]["text"].strip()

        # Format 5: Response field
        # {"response": "..."}
        if "response" in data and isinstance(data["response"], str):
            logger.debug("Parsed using response format")
            return data["response"].strip()

        # If none of the formats work, log the full response
        logger.error(f"Cannot parse Gemini response. Full response: {data}")
        raise ValueError(f"Unsupported response format. Available keys: {list(data.keys())}")

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
