from contextlib import contextmanager

from fastapi.testclient import TestClient

from domain import TicketConflict, TicketNotFound
from main import app
from routers.tickets import get_service
from schemas import Priority, TicketStatus


class FakeService:
    def __init__(self, ticket=None, error=None):
        self.ticket = ticket
        self.error = error

    def _result(self):
        if self.error:
            raise self.error
        return self.ticket

    def create(self, payload):
        return self._result()

    def list(self):
        return [self._result()]

    def get(self, ticket_id):
        return self._result()

    def update(self, ticket_id, payload):
        return self._result()

    def close(self, ticket_id):
        return self._result()

    def delete(self, ticket_id):
        if self.error:
            raise self.error


def item(status=TicketStatus.OPEN):
    return dict(
        id=1,
        title="Problem",
        description="Details",
        priority=Priority.MEDIUM,
        status=status,
    )


@contextmanager
def client(service):
    app.dependency_overrides[get_service] = lambda: service
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_existing_create_list_get_routes():
    with client(FakeService(item())) as http:
        response = http.post(
            "/api/v1/tickets", json={"title": "Problem", "description": "Details"}
        )
        assert response.status_code == 201
        assert http.get("/api/v1/tickets").status_code == 200
        assert http.get("/api/v1/tickets/1").json()["id"] == 1


def test_patch_close_and_delete_status_codes():
    with client(FakeService(item())) as http:
        response = http.patch("/api/v1/tickets/1", json={"title": "New title"})
        assert response.status_code == 200
        assert http.post("/api/v1/tickets/1/close").status_code == 200
        assert http.delete("/api/v1/tickets/1").status_code == 204


def test_not_found_and_conflict_error_contracts():
    with client(FakeService(error=TicketNotFound(8))) as http:
        response = http.get("/api/v1/tickets/8")
        assert response.status_code == 404
        assert response.json() == {"detail": {"code": "ticket_not_found", "ticket_id": 8}}
    with client(FakeService(error=TicketConflict(1, "delete"))) as http:
        response = http.delete("/api/v1/tickets/1")
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "ticket_conflict"


def test_validation_errors_keep_fastapi_422():
    with client(FakeService(item())) as http:
        response = http.patch("/api/v1/tickets/1", json={"unknown": True})
        assert response.status_code == 422
