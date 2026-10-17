from database import SessionLocal
from fastapi import APIRouter, Depends
from repositories.tickets import TicketRepository
from schemas import TicketCreate, TicketResponse
from services.tickets import TicketService
from sqlalchemy.orm import Session

router = APIRouter()


def get_session():
    with SessionLocal() as session:
        yield session


def get_service(session: Session = Depends(get_session)) -> TicketService:
    return TicketService(TicketRepository(session))


@router.post("", response_model=TicketResponse, status_code=201)
def create_ticket(
    payload: TicketCreate,
    service: TicketService = Depends(get_service),
):
    return service.create(payload)


@router.get("", response_model=list[TicketResponse])
def list_tickets(service: TicketService = Depends(get_service)):
    return service.list()


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, service: TicketService = Depends(get_service)):
    return service.get(ticket_id)
