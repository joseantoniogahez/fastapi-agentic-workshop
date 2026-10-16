from domain import TicketData
from models import Ticket
from repositories.tickets import TicketRepository
from schemas import TicketCreate


class TicketService:
    def __init__(self, repository: TicketRepository) -> None:
        self._repository = repository

    def create(self, payload: TicketCreate) -> Ticket:
        return self._repository.create(TicketData.create(payload))

    def list(self) -> list[Ticket]:
        return self._repository.list()
