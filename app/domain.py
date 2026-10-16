from dataclasses import dataclass

from schemas import Priority, TicketCreate, TicketStatus


@dataclass
class TicketData:
    title: str
    description: str
    priority: Priority
    status: TicketStatus = TicketStatus.OPEN

    @classmethod
    def create(cls, payload: TicketCreate) -> "TicketData":
        return cls(**payload.model_dump(), status=TicketStatus.OPEN)
