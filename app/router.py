from fastapi import APIRouter
from schemas import TicketCreate, TicketResponse
from services import TicketService

router = APIRouter(prefix="/api/v1/tickets")

@router.post("", response_model=TicketResponse,
             status_code=201)
def create_ticket(payload: TicketCreate):
    ticket_service = TicketService()
    return ticket_service.create(payload)
