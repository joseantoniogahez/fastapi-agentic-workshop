from database import Session, engine, get_session
from fastapi import APIRouter
from repositories import TicketRepository
from schemas import TicketCreate, TicketResponse
from services import TicketService

router = APIRouter(prefix="/api/v1/tickets")

@router.post("", response_model=TicketResponse,
             status_code=201)
def create_ticket(payload: TicketCreate):
    with Session(engine) as session:
        ticket_service = TicketService(TicketRepository(session))
        return ticket_service.create(payload)
