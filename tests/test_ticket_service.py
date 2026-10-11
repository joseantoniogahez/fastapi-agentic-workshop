import pytest

from models import Ticket
from services import TicketNotFound, TicketService


class FakeTicketRepository:
    def __init__(self, ticket=None):
        self.ticket = ticket

    def get(self, ticket_id):
        if self.ticket is not None and self.ticket.id == ticket_id:
            return self.ticket
        return None


def test_get_returns_ticket_from_repository():
    ticket = Ticket(
        id=7,
        title="A ticket",
        description="Details",
        priority="medium",
        status="open",
    )
    service = TicketService(FakeTicketRepository(ticket))

    assert service.get(7) is ticket


def test_get_missing_ticket_raises_domain_error():
    service = TicketService(FakeTicketRepository())

    with pytest.raises(TicketNotFound) as error:
        service.get(7)

    assert error.value.args == (7,)
