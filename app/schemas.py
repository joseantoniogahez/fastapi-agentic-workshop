from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TicketStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class TicketCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(max_length=2000)
    priority: Priority = Priority.MEDIUM


class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority | None = None

    @model_validator(mode="after")
    def require_field(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self

class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: Priority
    status: TicketStatus
