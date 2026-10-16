from fastapi import APIRouter
from repositories.tickets import InMemoryTicketRepository
from schemas import TicketCreate, TicketResponse
from services.tickets import TicketService

router = APIRouter()
repository = InMemoryTicketRepository()
service = TicketService(repository)


@router.post("", response_model=TicketResponse, status_code=201)
def create_ticket(payload: TicketCreate):
    return service.create(payload).to_response()


@router.get("")
def list_tickets():
    return [ticket.to_response() for ticket in service.list()]
