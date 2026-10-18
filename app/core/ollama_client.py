from collections.abc import AsyncIterator

import httpx

from app.config import Settings, get_settings


class OllamaClient:
    def __init__(self, settings: Settings | None = None):
        settings = settings or get_settings()
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.model = settings.OLLAMA_MODEL
        self.think = settings.OLLAMA_THINK
        self.num_ctx = settings.OLLAMA_NUM_CTX
        self.num_predict = settings.OLLAMA_NUM_PREDICT

        self.timeout = httpx.Timeout(settings.OLLAMA_TIMEOUT, connect=10.0)

    async def stream_chat(self, messages: list[dict], temperature: float = 0.2) -> AsyncIterator[str] :
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "stream": True,
            "think": self.think,
            "messages": messages,
            "options": {
                "temperature": temperature,
                "num_ctx": self.num_ctx,
                "num_predict": self.num_predict,
            },
        }

        async with httpx.AsyncClient(timeout= 60) as client:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        yield line


