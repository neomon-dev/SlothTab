import abc
import json
import asyncio
import aiohttp
from typing import Optional, Dict, Any, List
from .models import AnalysisBase


class AIProvider(abc.ABC):
    """Abstract base class for AI providers."""

    @abc.abstractmethod
    async def chat_complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Send a chat completion request and return the response."""
        pass

    @abc.abstractmethod
    async def get_available_models(self) -> List[str]:
        """Get list of available models from the provider."""
        pass

    @abc.abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to the AI provider."""
        pass


class LMStudioProvider(AIProvider):
    """Provider for LM Studio (default: http://localhost:1234/v1)."""

    def __init__(self, base_url: str = "http://localhost:1234/v1", api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "sk-lmstudio"
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def chat_complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self.base_url}/chat/completions"

        payload = {
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        payload["stream"] = False

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(
                    f"LM Studio API error {resp.status}: {text}"
                )
            return await resp.json()

    async def get_available_models(self) -> List[str]:
        session = await self._get_session()
        url = f"{self.base_url}/models"

        async with session.get(url) as resp:
            if resp.status != 200:
                return ["gemma-2b", "llama-3b", "mistral-7b"]
            data = await resp.json()
            model_ids = [m.get("id", m.get("name", "")) for m in data.get("data", [])]
            if model_ids:
                return model_ids
            return ["gemma-2b", "llama-3b", "mistral-7b"]

    async def test_connection(self) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self.base_url}/models"

        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    return {"connected": True, "message": "LM Studio reachable"}
                return {
                    "connected": False,
                    "message": f"LM Studio returned status {resp.status}",
                }
        except asyncio.TimeoutError:
            return {
                "connected": False,
                "message": "LM Studio connection timed out",
            }
        except Exception as e:
            return {"connected": False, "message": str(e)}


class OllamaProvider(AIProvider):
    """Provider for Ollama (default: http://localhost:11434/v1)."""

    def __init__(self, base_url: str = "http://localhost:11434/v1", api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "ollama"
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def chat_complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self.base_url}/api/chat"

        payload = {
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        if max_tokens is not None:
            payload["num_predict"] = max_tokens

        async with session.post(url, json=payload) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Ollama API error {resp.status}: {text}")
            return await resp.json()

    async def get_available_models(self) -> List[str]:
        session = await self._get_session()
        url = f"{self.base_url}/api/tags"

        async with session.get(url) as resp:
            if resp.status != 200:
                return ["gemma:2b", "llama3:8b", "mistral:7b"]
            data = await resp.json()
            models = data.get("models", [])
            return [m.get("name", "") for m in models]

    async def test_connection(self) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self.base_url}/api/tags"

        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    return {"connected": True, "message": "Ollama reachable"}
                return {
                    "connected": False,
                    "message": f"Ollama returned status {resp.status}",
                }
        except asyncio.TimeoutError:
            return {
                "connected": False,
                "message": "Ollama connection timed out",
            }
        except Exception as e:
            return {"connected": False, "message": str(e)}


class OpenAICompatibleProvider(AIProvider):
    """Provider for generic OpenAI-compatible endpoints."""

    def __init__(
        self,
        base_url: str = "https://api.openai.com/v1",
        api_key: str = "",
        model: str = "gpt-4",
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "sk-test"
        self.model = model
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def chat_complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(
                    f"OpenAI-compatible API error {resp.status}: {text}"
                )
            return await resp.json()

    async def get_available_models(self) -> List[str]:
        session = await self._get_session()
        url = f"{self.base_url}/models"

        async with session.get(url) as resp:
            if resp.status != 200:
                return [self.model]
            data = await resp.json()
            model_ids = [m.get("id", "") for m in data.get("data", [])]
            if model_ids:
                return model_ids
            return [self.model]

    async def test_connection(self) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self.base_url}/models"

        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    return {"connected": True, "message": "OpenAI-compatible reachable"}
                return {
                    "connected": False,
                    "message": f"OpenAI-compatible returned status {resp.status}",
                }
        except asyncio.TimeoutError:
            return {
                "connected": False,
                "message": "OpenAI-compatible connection timed out",
            }
        except Exception as e:
            return {"connected": False, "message": str(e)}


# Provider factory

def create_provider(
    provider_type: str,
    base_url: str = "",
    api_key: str = "",
    model: str = "",
) -> AIProvider:
    """Factory function to create the appropriate AI provider."""
    if provider_type.lower() == "lmstudio":
        return LMStudioProvider(
            base_url=base_url or "http://localhost:1234/v1",
            api_key=api_key,
        )
    elif provider_type.lower() == "ollama":
        return OllamaProvider(
            base_url=base_url or "http://localhost:11434/v1", api_key=api_key
        )
    else:
        # Generic OpenAI-compatible
        return OpenAICompatibleProvider(
            base_url=base_url or "https://api.openai.com/v1",
            api_key=api_key,
            model=model or "gpt-4",
        )