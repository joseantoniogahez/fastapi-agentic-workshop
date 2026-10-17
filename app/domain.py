from dataclasses import dataclass

from schemas import Priority, TicketCreate, TicketStatus


class TicketNotFound(Exception):
    def __init__(self, ticket_id: int) -> None:
        self.ticket_id = ticket_id
        super().__init__(f"Ticket {ticket_id} was not found")


@dataclass
class TicketData:
    title: str
    description: str
    priority: Priority
    status: TicketStatus = TicketStatus.OPEN

    @classmethod
    def create(cls, payload: TicketCreate) -> "TicketData":
        return cls(**payload.model_dump(), status=TicketStatus.OPEN)
