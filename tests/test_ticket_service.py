from types import SimpleNamespace

import pytest

from domain import TicketConflict, TicketNotFound
from schemas import Priority, TicketCreate, TicketStatus, TicketUpdate
from services.tickets import TicketService


class FakeRepository:
    def __init__(self, ticket=None):
        self.ticket = ticket
        self.deleted = False

    def get(self, ticket_id):
        return self.ticket

    def create(self, data):
        return data

    def list(self):
        return []

    def update(self, ticket, changes):
        for field, value in changes.items():
            setattr(ticket, field, value)
        return ticket

    def close(self, ticket):
        ticket.status = TicketStatus.CLOSED
        return ticket

    def delete(self, ticket):
        self.deleted = True


def ticket(status=TicketStatus.OPEN):
    return SimpleNamespace(
        id=1,
        title="Problem",
        description="Details",
        priority=Priority.MEDIUM,
        status=status,
        deleted_at=None,
    )


def test_update_changes_only_provided_fields():
    item = ticket()
    service = TicketService(FakeRepository(item))
    updated = service.update(1, TicketUpdate(title="New title"))
    assert updated.title == "New title"
    assert updated.description == "Details"


def test_close_sets_closed_status():
    item = ticket()
    assert TicketService(FakeRepository(item)).close(1).status == TicketStatus.CLOSED


def test_closed_ticket_cannot_be_updated_or_deleted():
    for operation in ("update", "delete"):
        repository = FakeRepository(ticket(TicketStatus.CLOSED))
        service = TicketService(repository)
        with pytest.raises(TicketConflict):
            if operation == "update":
                service.update(1, TicketUpdate(title="New title"))
            else:
                service.delete(1)
        assert not repository.deleted


def test_missing_ticket_raises_domain_error():
    with pytest.raises(TicketNotFound):
        TicketService(FakeRepository()).update(10, TicketUpdate(title="New title"))


def test_delete_delegates_for_open_ticket():
    repository = FakeRepository(ticket())
    TicketService(repository).delete(1)
    assert repository.deleted
