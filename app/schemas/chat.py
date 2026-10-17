from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(
        ..., description="Who authored the message"
    )
    content: str = Field(..., description="The content of the message")

class ChatMessageRequest(BaseModel):
    messages: list[ChatMessage]
    temperature: float = Field(default=0, ge=0.0, le=2.0, description="The temperature that the message was sent to")
