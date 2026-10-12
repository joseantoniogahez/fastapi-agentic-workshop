from typing import Protocol

from google import genai
from google.genai import types
from models import Ticket
from pydantic import ValidationError
from schemas import (
    TicketAnalysis,
    TicketCreate,
    TicketResponse,
    TicketStatus,
    TicketUpdate,
)


class AIService(Protocol):
    def analyze_ticket(self, ticket: TicketResponse) -> TicketAnalysis:
        ...


class AIProviderUnavailable(Exception):
    pass


class AIResponseInvalid(Exception):
    pass


class GeminiAIService(AIService):
    def __init__(self, api_key: str, model: str = "gemini-3.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def analyze_ticket(self, ticket: TicketResponse) -> TicketAnalysis:
        prompt = (
            "Analyze this support ticket. Choose a concise category and suggest "
            "a priority based on its impact. Summarize the user's issue.\n\n"
            f"Title: {ticket.title}\n"
            f"Description: {ticket.description}\n"
            f"Current priority: {ticket.priority.value}\n"
            f"Status: {ticket.status.value}"
        )
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=TicketAnalysis,
                ),
            )
        except Exception as exc:
            raise AIProviderUnavailable from exc

        try:
            if response.parsed is not None:
                return TicketAnalysis.model_validate(response.parsed)
            if response.text:
                return TicketAnalysis.model_validate_json(response.text)
        except (ValidationError, ValueError, TypeError) as exc:
            raise AIResponseInvalid from exc
        raise AIResponseInvalid("Gemini returned no structured content")


class TicketNotFound(Exception):
    pass


class TicketAlreadyClosed(Exception):
    pass


class TicketService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, payload: TicketCreate):
        ticket = Ticket(
            **payload.model_dump(),
            status=TicketStatus.OPEN,
        )
        return self.repository.create(ticket)

    def get(self, ticket_id: int):
        ticket = self.repository.get(ticket_id)
        if ticket is None:
            raise TicketNotFound(ticket_id)
        return ticket

    def update(self, ticket_id: int, payload: TicketUpdate):
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketAlreadyClosed(ticket_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(ticket, field, value)
        return self.repository.save(ticket)

    def close(self, ticket_id: int):
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketAlreadyClosed(ticket_id)
        ticket.status = TicketStatus.CLOSED
        return self.repository.save(ticket)

    def delete(self, ticket_id: int):
        ticket = self.get(ticket_id)
        if ticket.status == TicketStatus.CLOSED:
            raise TicketAlreadyClosed(ticket_id)
        self.repository.delete(ticket)

    def analyze(self, ticket_id: int, ai_service: AIService) -> TicketAnalysis:
        ticket = self.get(ticket_id)
        return ai_service.analyze_ticket(TicketResponse.model_validate(ticket))
