from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="The role that the message was sent to")
    content: str = Field(..., description="The content of the message")

class ChatMessageRequest(BaseModel):
    message: list[ChatMessage]
    temperature: float = Field(default=0, ge=0.0, le=2.0, description="The temperature that the message was sent to")
