from models import Ticket
from schemas import TicketCreate, TicketStatus, TicketUpdate


class TicketNotFound(Exception):
    pass


class TicketAlreadyClosed(Exception):
    pass


class TicketService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, payload: TicketCreate):
        ticket = Ticket(
            **payload.model_dump(),
            status=TicketStatus.OPEN,
        )
        return self.repository.create(ticket)

    def get(self, ticket_id: int):
        ticket = self.repository.get(ticket_id)
        if ticket is None:
            raise TicketNotFound(ticket_id)
        return ticket

    def update(self, ticket_id: int, payload: TicketUpdate):
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketAlreadyClosed(ticket_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(ticket, field, value)
        return self.repository.save(ticket)

    def close(self, ticket_id: int):
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketAlreadyClosed(ticket_id)
        ticket.status = TicketStatus.CLOSED
        return self.repository.save(ticket)

    def delete(self, ticket_id: int):
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketAlreadyClosed(ticket_id)
        self.repository.delete(ticket)
