import os
from typing import Annotated

from database import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from repositories import TicketRepository
from schemas import TicketAnalysis, TicketCreate, TicketResponse, TicketUpdate
from services import AIService, GeminiAIService, TicketService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/tickets")


def get_ticket_repository(
    session: Annotated[Session, Depends(get_session)],
) -> TicketRepository:
    return TicketRepository(session)


def get_ticket_service(
    repository: Annotated[TicketRepository, Depends(get_ticket_repository)],
) -> TicketService:
    return TicketService(repository)


def get_ai_service() -> GeminiAIService:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini API key is not configured",
        )
    return GeminiAIService(api_key)


@router.post("", response_model=TicketResponse, status_code=201)
def create_ticket(
    payload: TicketCreate,
    service: Annotated[TicketService, Depends(get_ticket_service)],
):
    return service.create(payload)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    service: Annotated[TicketService, Depends(get_ticket_service)],
):
    return service.get(ticket_id)


@router.get("", response_model=list[TicketResponse])
def list_tickets(
    service: Annotated[TicketService, Depends(get_ticket_service)],
):
    return service.list()


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    service: Annotated[TicketService, Depends(get_ticket_service)],
):
    return service.update(ticket_id, payload)


@router.post("/{ticket_id}/close", response_model=TicketResponse)
def close_ticket(
    ticket_id: int,
    service: Annotated[TicketService, Depends(get_ticket_service)],
):
    return service.close(ticket_id)


@router.post("/{ticket_id}/analyze", response_model=TicketAnalysis)
def analyze_ticket(
    ticket_id: int,
    service: Annotated[TicketService, Depends(get_ticket_service)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
):
    return service.analyze(ticket_id, ai_service)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    service: Annotated[TicketService, Depends(get_ticket_service)],
):
    service.delete(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
