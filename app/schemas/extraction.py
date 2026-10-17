from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    ask: str = Field(description="Actionable task item")
    priority: str = Field(description="Priority level: High, Medium, or Low")
    assignee: str | None = Field(default=None, description="Person responsible if mentioned")

class TaskExtractionResponse(BaseModel):
    summary: str = Field(description="Summary of the task")
    action_items: list[ActionItem]