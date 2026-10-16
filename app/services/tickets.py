from domain import Ticket
from repositories.tickets import InMemoryTicketRepository
from schemas import TicketCreate


class TicketService:
    def __init__(self, repository: InMemoryTicketRepository) -> None:
        self._repository = repository

    def create(self, payload: TicketCreate) -> Ticket:
        ticket = Ticket.create(payload)
        return self._repository.save(ticket)

    def list(self) -> list[Ticket]:
        return self._repository.list()
