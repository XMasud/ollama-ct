import json
from collections.abc import AsyncIterator

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.core.ollama_client import OllamaClient
from app.schemas.chat import ChatMessageRequest

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_ollama_client() -> OllamaClient:
    return OllamaClient()


@router.post("/stream")
async def stream_chat(
        request: ChatMessageRequest,
        client: OllamaClient = Depends(get_ollama_client),
):
    messages = [msg.model_dump() for msg in request.messages]
    stream = client.stream_chat(messages, request.temperature)

    try:
        first = await anext(stream)
    except StopAsyncIteration:
        first = None
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot reach Ollama. Is it running?")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ollama returned {e.response.status_code}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timed out waiting for Ollama")

    async def event_generator() -> AsyncIterator[str]:
        lines = [first] if first is not None else []
        for line in lines:
            if stream_token := _extract_token(line):
                yield stream_token
            async for stream_token in stream:
                if stream_token := _extract_token(line):
                    yield stream_token


def _extract_token(raw_line: str) -> str:
    try:
        data = json.loads(raw_line)
    except json.JSONDecodeError:
        return ""
    return data.get("message", {}).get("content", "")
