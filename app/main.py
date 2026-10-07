from fastapi import FastAPI
from schemas import TicketCreate, TicketResponse, TicketStatus

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

tickets = []

@app.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(payload: TicketCreate):
    ticket = payload.model_dump()
    ticket["status"] = TicketStatus.OPEN

    tickets.append(ticket)
    return ticket

@app.get("/tickets")
def list_tickets():
    return tickets
