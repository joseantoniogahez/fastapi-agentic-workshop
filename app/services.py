from models import Ticket
from schemas import TicketCreate, TicketStatus


class TicketService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, payload: TicketCreate):
        ticket = Ticket(
            **payload.model_dump(),
            status=TicketStatus.OPEN,
        )
        return self.repository.create(ticket)
