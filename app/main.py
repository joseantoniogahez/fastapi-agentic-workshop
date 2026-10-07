from fastapi import FastAPI, HTTPException, Response, status

from schemas import TicketCreate, TicketResponse, TicketStatus, TicketUpdate

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


tickets: list[dict] = []
next_ticket_id = 1


def find_ticket(ticket_id: int) -> dict:
    for ticket in tickets:
        if ticket["id"] == ticket_id and not ticket["deleted"]:
            return ticket
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")


@app.post("/api/v1/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(payload: TicketCreate):
    global next_ticket_id

    ticket = payload.model_dump()
    ticket.update(
        id=next_ticket_id,
        status=TicketStatus.OPEN,
        deleted=False,
    )
    next_ticket_id += 1
    tickets.append(ticket)
    return ticket


@app.get("/api/v1/tickets", response_model=list[TicketResponse])
def list_tickets():
    return [ticket for ticket in tickets if not ticket["deleted"]]


@app.patch("/api/v1/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, payload: TicketUpdate):
    ticket = find_ticket(ticket_id)
    if ticket["status"] == TicketStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Closed tickets cannot be edited",
        )

    ticket.update(payload.model_dump(exclude_unset=True))
    return ticket


@app.delete("/api/v1/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int):
    ticket = find_ticket(ticket_id)
    if ticket["status"] == TicketStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Closed tickets cannot be deleted",
        )
    ticket["deleted"] = True
    return Response(status_code=status.HTTP_204_NO_CONTENT)
