from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_ticket(title: str = "Printer issue") -> dict:
    response = client.post(
        "/api/v1/tickets",
        json={"title": title, "description": "The printer is offline"},
    )
    assert response.status_code == 201
    return response.json()


def test_create_list_filter_and_get_ticket() -> None:
    ticket = create_ticket()

    assert ticket["id"] > 0
    assert ticket["status"] == "open"
    assert client.get("/api/v1/tickets", params={"status": "open"}).json()[-1]["id"] == ticket["id"]
    assert client.get(f"/api/v1/tickets/{ticket['id']}").json() == ticket


def test_update_close_and_closed_ticket_rules() -> None:
    ticket = create_ticket("Account access")
    updated = client.patch(
        f"/api/v1/tickets/{ticket['id']}",
        json={"status": "closed"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "closed"
    assert client.patch(f"/api/v1/tickets/{ticket['id']}", json={"title": "Changed"}).status_code == 409
    assert client.delete(f"/api/v1/tickets/{ticket['id']}").status_code == 409


def test_soft_delete_hides_ticket() -> None:
    ticket = create_ticket("Laptop setup")
    assert client.delete(f"/api/v1/tickets/{ticket['id']}").status_code == 204
    assert client.get(f"/api/v1/tickets/{ticket['id']}").status_code == 404
    assert all(item["id"] != ticket["id"] for item in client.get("/api/v1/tickets").json())


def test_validation_and_missing_ticket() -> None:
    assert client.post("/api/v1/tickets", json={"title": "x", "description": ""}).status_code == 422
    assert client.post(
        "/api/v1/tickets", json={"title": "Valid title", "description": "", "other": 1}
    ).status_code == 422
    assert client.get("/api/v1/tickets/999999").status_code == 404


def test_pagination_and_health() -> None:
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/v1/tickets", params={"limit": 0}).status_code == 422
