from fastapi import FastAPI, HTTPException, Response, status

from app.schemas import (
    TicketAnalysis,
    TicketCreate,
    TicketResponse,
    TicketStatus,
    TicketUpdate,
)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


tickets: dict[int, dict] = {}
next_ticket_id = 1


def get_ticket(ticket_id: int, *, include_deleted: bool = False) -> dict:
    ticket = tickets.get(ticket_id)
    if ticket is None or (ticket["deleted"] and not include_deleted):
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate):
    global next_ticket_id
    ticket = {
        "id": next_ticket_id,
        **payload.model_dump(),
        "status": TicketStatus.OPEN,
        "deleted": False,
    }
    tickets[next_ticket_id] = ticket
    next_ticket_id += 1
    return ticket


@app.get("/tickets", response_model=list[TicketResponse])
def list_tickets():
    return [ticket for ticket in tickets.values() if not ticket["deleted"]]


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def read_ticket(ticket_id: int):
    return get_ticket(ticket_id)


@app.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, payload: TicketUpdate):
    ticket = get_ticket(ticket_id)
    if ticket["status"] == TicketStatus.CLOSED:
        raise HTTPException(status_code=409, detail="Closed tickets cannot be edited")
    ticket.update(payload.model_dump(exclude_unset=True))
    return ticket


@app.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int):
    ticket = get_ticket(ticket_id)
    if ticket["status"] == TicketStatus.CLOSED:
        raise HTTPException(status_code=409, detail="Closed tickets cannot be deleted")
    ticket["deleted"] = True
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/tickets/{ticket_id}/analysis", response_model=TicketAnalysis)
def analyze_ticket(ticket_id: int):
    ticket = get_ticket(ticket_id, include_deleted=True)
    history = [
        item
        for item in tickets.values()
        if item["id"] != ticket_id
        and item["status"] == TicketStatus.CLOSED
        and item["title"].casefold() == ticket["title"].casefold()
    ]
    return {
        "ticket_id": ticket_id,
        "summary": f"{ticket['title']}: {ticket['description']}",
        "suggestion": (
            "Revisa la soluciÃ³n de un caso cerrado con el mismo tÃ­tulo."
            if history
            else "Clasifica el problema y solicita los datos que falten antes de proponer una soluciÃ³n."
        ),
        "based_on_ticket_ids": [item["id"] for item in history],
    }
