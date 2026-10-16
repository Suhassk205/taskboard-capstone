from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Status = Literal["open", "in_progress", "resolved"]
Priority = Literal["low", "medium", "high", "urgent"]
Category = Literal["IT", "Facilities", "Academics", "Other"]

class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    category: Category = "IT"
    requester: str = Field(default="Student", min_length=1, max_length=120)
    owner: str = Field(default="Unassigned", min_length=1, max_length=120)
    priority: Priority = "medium"
    status: Status = "open"

class TicketUpdate(TicketCreate):
    pass

class TicketOut(TicketCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
