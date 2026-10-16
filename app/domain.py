from dataclasses import dataclass

from schemas import Priority, TicketCreate, TicketStatus


@dataclass
class Ticket:
    title: str
    description: str
    priority: Priority
    status: TicketStatus = TicketStatus.OPEN

    @classmethod
    def create(cls, payload: TicketCreate) -> "Ticket":
        return cls(**payload.model_dump(), status=TicketStatus.OPEN)

    def to_response(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
        }
