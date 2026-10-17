from domain import TicketConflict, TicketData, TicketNotFound
from models import Ticket
from repositories.tickets import TicketRepository
from schemas import TicketCreate, TicketStatus, TicketUpdate


class TicketService:
    def __init__(self, repository: TicketRepository) -> None:
        self._repository = repository

    def create(self, payload: TicketCreate) -> Ticket:
        return self._repository.create(TicketData.create(payload))

    def list(self) -> list[Ticket]:
        return self._repository.list()

    def get(self, ticket_id: int) -> Ticket:
        ticket = self._repository.get(ticket_id)
        if ticket is None:
            raise TicketNotFound(ticket_id)
        return ticket

    def update(self, ticket_id: int, payload: TicketUpdate) -> Ticket:
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketConflict(ticket_id, "update")
        return self._repository.update(ticket, payload.model_dump(exclude_unset=True))

    def close(self, ticket_id: int) -> Ticket:
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketConflict(ticket_id, "close")
        return self._repository.close(ticket)

    def delete(self, ticket_id: int) -> None:
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketConflict(ticket_id, "delete")
        self._repository.delete(ticket)
