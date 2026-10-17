from statistics import mode

import httpx

from app.config import Settings


class OllamaClient:
    def __init__(self, host, port, username, password):
        self.base_url = Settings.BASE_URL
        self.model = Settings.MODEL

    async def chat_stream(self, message: list[dict], temperature: float = 0.2):
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "stream": True,
            "message": message,
            "option":{
                "temperature": temperature,
            }
        }

        async with httpx.AsyncClient(timeout= 60) as client:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                async for chunk in response.aiter_lines():
                    if chunk:
                        yield chunk


