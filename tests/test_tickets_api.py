import pytest


def test_create_ticket(client):
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Unable to log in",
            "description": "Login fails",
            "priority": "high",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "open"
    assert body["priority"] == "high"
    assert isinstance(body["id"], int)


def test_get_created_ticket(client):
    created = client.post(
        "/api/v1/tickets",
        json={
            "title": "Unable to log in",
            "description": "Login fails",
            "priority": "high",
        },
    ).json()

    response = client.get(f"/api/v1/tickets/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_new_client_starts_with_empty_repository(client_factory):
    first_client = client_factory()
    created = first_client.post(
        "/api/v1/tickets",
        json={
            "title": "Isolated ticket",
            "description": "Only in the first fake repository",
        },
    ).json()

    second_client = client_factory()
    response = second_client.get(f"/api/v1/tickets/{created['id']}")

    assert response.status_code == 404


def test_get_missing_ticket_returns_404(client):
    response = client.get("/api/v1/tickets/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket 999 not found"}


def test_edit_closed_ticket_returns_409_and_preserves_data(client):
    created = client.post(
        "/api/v1/tickets",
        json={
            "title": "Keep this title",
            "description": "Original details",
            "priority": "medium",
        },
    ).json()
    client.post(f"/api/v1/tickets/{created['id']}/close")

    response = client.patch(
        f"/api/v1/tickets/{created['id']}",
        json={"title": "Changed title", "priority": "high"},
    )

    assert response.status_code == 409
    fetched = client.get(f"/api/v1/tickets/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Keep this title"
    assert fetched.json()["priority"] == "medium"
    assert fetched.json()["status"] == "closed"


def test_delete_ticket_returns_204_and_hides_it(client):
    created = client.post(
        "/api/v1/tickets",
        json={
            "title": "Delete me",
            "description": "Temporary ticket",
        },
    ).json()

    response = client.delete(f"/api/v1/tickets/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/api/v1/tickets/{created['id']}").status_code == 404


@pytest.mark.parametrize(
    ("title", "expected_status"),
    [
        ("ab", 422),
        ("abc", 201),
    ],
)
def test_title_length(client, title, expected_status):
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": title,
            "description": "Login fails",
            "priority": "medium",
        },
    )

    assert response.status_code == expected_status


def test_unknown_priority_returns_422(client):
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Unable to log in",
            "description": "Login fails",
            "priority": "urgent",
        },
    )

    assert response.status_code == 422
