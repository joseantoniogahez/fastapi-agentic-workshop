from app.repositories import InMemoryTicketRepository
from app.schemas import TicketCreate, TicketResponse, TicketStatus, TicketUpdate


class TicketNotFoundError(Exception):
    pass


class TicketStateError(Exception):
    pass


class TicketService:
    def __init__(self, repository: InMemoryTicketRepository | None = None) -> None:
        self.repository = repository or InMemoryTicketRepository()

    def create(self, payload: TicketCreate) -> TicketResponse:
        return self.repository.add({**payload.model_dump(), "status": TicketStatus.OPEN})

    def list(
        self,
        *,
        status: TicketStatus | None,
        priority: str | None,
        limit: int,
        offset: int,
    ) -> list[TicketResponse]:
        return self.repository.list(status=status, priority=priority)[offset : offset + limit]

    def get(self, ticket_id: int) -> TicketResponse:
        ticket = self.repository.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundError
        return ticket

    def update(self, ticket_id: int, payload: TicketUpdate) -> TicketResponse:
        ticket = self.repository.raw(ticket_id)
        if ticket is None or ticket["deleted"]:
            raise TicketNotFoundError
        if ticket["status"] == TicketStatus.CLOSED:
            raise TicketStateError("Closed tickets cannot be edited")
        changes = payload.model_dump(exclude_unset=True)
        if not changes:
            raise TicketStateError("At least one field must be provided")
        if changes.get("status") == TicketStatus.OPEN and ticket["status"] != TicketStatus.OPEN:
            raise TicketStateError("Tickets cannot be reopened")
        ticket.update(changes)
        return self.repository.save(ticket)

    def delete(self, ticket_id: int) -> None:
        ticket = self.repository.raw(ticket_id)
        if ticket is None or ticket["deleted"]:
            raise TicketNotFoundError
        if ticket["status"] == TicketStatus.CLOSED:
            raise TicketStateError("Closed tickets cannot be deleted")
        ticket["deleted"] = True
        self.repository.save(ticket)
