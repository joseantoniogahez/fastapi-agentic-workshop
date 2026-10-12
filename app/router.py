from database import Session, engine, get_session
from fastapi import APIRouter, Response, status
from repositories import TicketRepository
from schemas import TicketCreate, TicketResponse, TicketUpdate
from services import TicketService

router = APIRouter(prefix="/api/v1/tickets")

@router.post("", response_model=TicketResponse,
             status_code=201)
def create_ticket(payload: TicketCreate):
    with Session(engine) as session:
        ticket_service = TicketService(TicketRepository(session))
        return ticket_service.create(payload)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    with Session(engine) as session:
        ticket_service = TicketService(TicketRepository(session))
        return ticket_service.get(ticket_id)


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, payload: TicketUpdate):
    with Session(engine) as session:
        ticket_service = TicketService(TicketRepository(session))
        return ticket_service.update(ticket_id, payload)


@router.post("/{ticket_id}/close", response_model=TicketResponse)
def close_ticket(ticket_id: int):
    with Session(engine) as session:
        ticket_service = TicketService(TicketRepository(session))
        return ticket_service.close(ticket_id)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int):
    with Session(engine) as session:
        TicketService(TicketRepository(session)).delete(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
