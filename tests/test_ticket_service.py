import pytest
from models import Ticket
from schemas import Priority, TicketAnalysis, TicketResponse
from services import (
    AIProviderUnavailable,
    AIResponseInvalid,
    GeminiAIService,
    TicketNotFound,
    TicketService,
)


class FakeTicketRepository:
    def __init__(self, ticket=None):
        self.ticket = ticket

    def get(self, ticket_id):
        if self.ticket is not None and self.ticket.id == ticket_id:
            return self.ticket
        return None

    def list(self):
        return [self.ticket] if self.ticket is not None else []


class FakeAIService:
    def __init__(self, result):
        self.result = result
        self.ticket = None

    def analyze_ticket(self, ticket):
        self.ticket = ticket
        return self.result


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


def test_list_returns_repository_tickets():
    ticket = Ticket(
        id=7,
        title="A ticket",
        description="Details",
        priority="medium",
        status="open",
    )
    service = TicketService(FakeTicketRepository(ticket))

    assert service.list() == [ticket]


def test_get_missing_ticket_raises_domain_error():
    service = TicketService(FakeTicketRepository())

    with pytest.raises(TicketNotFound) as error:
        service.get(7)

    assert error.value.args == (7,)


def test_analyze_passes_response_schema_to_ai_service():
    ticket = Ticket(
        id=7,
        title="Cannot log in",
        description="The password is rejected",
        priority="medium",
        status="open",
    )
    analysis = TicketAnalysis(
        category="authentication",
        suggested_priority=Priority.HIGH,
        summary="The user cannot authenticate.",
    )
    ai_service = FakeAIService(analysis)
    service = TicketService(FakeTicketRepository(ticket))

    result = service.analyze(7, ai_service)

    assert result is analysis
    assert ai_service.ticket.model_dump() == {
        "id": 7,
        "title": "Cannot log in",
        "description": "The password is rejected",
        "priority": Priority.MEDIUM,
        "status": "open",
    }


def test_analyze_missing_ticket_does_not_call_ai_service():
    ai_service = FakeAIService(None)
    service = TicketService(FakeTicketRepository())

    with pytest.raises(TicketNotFound):
        service.analyze(7, ai_service)

    assert ai_service.ticket is None


def test_gemini_service_validates_structured_response(monkeypatch):
    class FakeModels:
        def generate_content(self, **kwargs):
            return type(
                "Response",
                (),
                {
                    "parsed": {
                        "category": "authentication",
                        "suggested_priority": "high",
                        "summary": "The user cannot authenticate.",
                    },
                    "text": None,
                },
            )()

    service = GeminiAIService.__new__(GeminiAIService)
    service.client = type("Client", (), {"models": FakeModels()})()
    service.model = "test-model"
    ticket = TicketResponse.model_validate(
        {
            "id": 1,
            "title": "Cannot log in",
            "description": "Password rejected",
            "priority": "medium",
            "status": "open",
        }
    )

    result = service.analyze_ticket(ticket)

    assert result.category == "authentication"
    assert result.suggested_priority == Priority.HIGH


def test_gemini_service_maps_provider_errors():
    class FakeModels:
        def generate_content(self, **kwargs):
            raise RuntimeError("network error")

    service = GeminiAIService.__new__(GeminiAIService)
    service.client = type("Client", (), {"models": FakeModels()})()
    service.model = "test-model"
    ticket = TicketResponse.model_validate(
        {
            "id": 1,
            "title": "Cannot log in",
            "description": "Password rejected",
            "priority": "medium",
            "status": "open",
        }
    )

    with pytest.raises(AIProviderUnavailable):
        service.analyze_ticket(ticket)


def test_gemini_service_rejects_invalid_response():
    class FakeModels:
        def generate_content(self, **kwargs):
            return type(
                "Response", (), {"parsed": {"category": "auth"}, "text": None}
            )()

    service = GeminiAIService.__new__(GeminiAIService)
    service.client = type("Client", (), {"models": FakeModels()})()
    service.model = "test-model"
    ticket = TicketResponse.model_validate(
        {
            "id": 1,
            "title": "Cannot log in",
            "description": "Password rejected",
            "priority": "medium",
            "status": "open",
        }
    )

    with pytest.raises(AIResponseInvalid):
        service.analyze_ticket(ticket)
