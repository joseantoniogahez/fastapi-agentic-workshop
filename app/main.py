from database import create_tables
from domain import TicketConflict, TicketNotFound
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers.tickets import router as tickets_router

app = FastAPI()


@app.exception_handler(TicketNotFound)
async def ticket_not_found_handler(request: Request, exc: TicketNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": {"code": "ticket_not_found", "ticket_id": exc.ticket_id}},
    )


@app.exception_handler(TicketConflict)
async def ticket_conflict_handler(request: Request, exc: TicketConflict):
    return JSONResponse(
        status_code=409,
        content={
            "detail": {
                "code": "ticket_conflict",
                "ticket_id": exc.ticket_id,
                "operation": exc.operation,
            }
        },
    )


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(tickets_router, prefix="/api/v1/tickets", tags=["tickets"])
