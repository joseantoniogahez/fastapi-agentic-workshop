from typing import Annotated

from database import get_session
from fastapi import APIRouter, Depends, Response, status
from repositories import TicketRepository
from schemas import TicketCreate, TicketResponse, TicketUpdate
from services import TicketService
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


@router.post("", response_model=TicketResponse,
             status_code=201)
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


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    service: Annotated[TicketService, Depends(get_ticket_service)],
):
    service.delete(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
