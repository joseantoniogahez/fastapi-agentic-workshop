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


@pytest.mark.parametrize(
    "title, expected", [("ab", 422), ("abc", 201)],
)
def test_title_length(client, title, expected):
    response = client.post("/api/v1/tickets", json={
        "title": title,
        "description": "Login fails",
        "priority": "medium",
    })
    assert response.status_code == expected
