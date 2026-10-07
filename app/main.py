from fastapi import FastAPI, HTTPException, Query, Response, status

from app.schemas import TicketCreate, TicketResponse, TicketStatus, TicketUpdate
from app.services import TicketNotFoundError, TicketService, TicketStateError

app = FastAPI(title="SupportDesk API", version="1.0.0")
service = TicketService()


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/api/v1/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tickets"],
)
def create_ticket(payload: TicketCreate) -> TicketResponse:
    return service.create(payload)


@app.get("/api/v1/tickets", response_model=list[TicketResponse], tags=["tickets"])
def list_tickets(
    status_filter: TicketStatus | None = Query(default=None, alias="status"),
    priority: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[TicketResponse]:
    return service.list(status=status_filter, priority=priority, limit=limit, offset=offset)


@app.get("/api/v1/tickets/{ticket_id}", response_model=TicketResponse, tags=["tickets"])
def get_ticket(ticket_id: int) -> TicketResponse:
    try:
        return service.get(ticket_id)
    except TicketNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Ticket not found") from exc


@app.patch("/api/v1/tickets/{ticket_id}", response_model=TicketResponse, tags=["tickets"])
def update_ticket(ticket_id: int, payload: TicketUpdate) -> TicketResponse:
    try:
        return service.update(ticket_id, payload)
    except TicketNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Ticket not found") from exc
    except TicketStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.delete("/api/v1/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tickets"])
def delete_ticket(ticket_id: int) -> Response:
    try:
        service.delete(ticket_id)
    except TicketNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Ticket not found") from exc
    except TicketStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
