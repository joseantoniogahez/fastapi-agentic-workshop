from app.schemas import TicketResponse, TicketStatus


class InMemoryTicketRepository:
    """Small repository adapter; replace with a persistent adapter as the course evolves."""

    def __init__(self) -> None:
        self._tickets: dict[int, dict] = {}
        self._next_id = 1

    def add(self, values: dict) -> TicketResponse:
        ticket = {"id": self._next_id, **values, "deleted": False}
        self._tickets[self._next_id] = ticket
        self._next_id += 1
        return TicketResponse.model_validate(ticket)

    def get(self, ticket_id: int, *, include_deleted: bool = False) -> TicketResponse | None:
        ticket = self._tickets.get(ticket_id)
        if ticket is None or (ticket["deleted"] and not include_deleted):
            return None
        return TicketResponse.model_validate(ticket)

    def raw(self, ticket_id: int) -> dict | None:
        return self._tickets.get(ticket_id)

    def save(self, ticket: dict) -> TicketResponse:
        self._tickets[ticket["id"]] = ticket
        return TicketResponse.model_validate(ticket)

    def list(self, *, status: TicketStatus | None, priority: str | None) -> list[TicketResponse]:
        return [
            TicketResponse.model_validate(ticket)
            for ticket in self._tickets.values()
            if not ticket["deleted"]
            and (status is None or ticket["status"] == status)
            and (priority is None or ticket["priority"] == priority)
        ]
