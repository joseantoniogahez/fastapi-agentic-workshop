from domain import Ticket


class InMemoryTicketRepository:
    def __init__(self) -> None:
        self._tickets: list[Ticket] = []

    def save(self, ticket: Ticket) -> Ticket:
        self._tickets.append(ticket)
        return ticket

    def list(self) -> list[Ticket]:
        return self._tickets
