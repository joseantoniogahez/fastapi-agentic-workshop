from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient
from main import create_app
from router import get_ticket_repository


class FakeTicketRepository:
    def __init__(self):
        self.tickets = {}
        self.next_id = 1

    def create(self, ticket):
        ticket.id = self.next_id
        self.next_id += 1
        self.tickets[ticket.id] = ticket
        return ticket

    def get(self, ticket_id):
        ticket = self.tickets.get(ticket_id)
        if ticket is None or ticket.is_deleted:
            return None
        return ticket

    def list(self):
        return [ticket for ticket in self.tickets.values() if not ticket.is_deleted]

    def save(self, ticket):
        self.tickets[ticket.id] = ticket
        return ticket

    def delete(self, ticket):
        ticket.is_deleted = True


@pytest.fixture
def client_factory() -> Iterator[Callable[[], TestClient]]:
    clients = []

    def make_client():
        fake_repo = FakeTicketRepository()
        app = create_app(manage_database=False)
        app.dependency_overrides[get_ticket_repository] = lambda: fake_repo
        client = TestClient(app)
        client.__enter__()
        clients.append(client)
        return client

    yield make_client

    for test_client in clients:
        app = test_client.app
        test_client.__exit__(None, None, None)
        app.dependency_overrides.pop(get_ticket_repository, None)


@pytest.fixture
def client(client_factory):
    yield client_factory()
