from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from router import router
from services import TicketAlreadyClosed, TicketNotFound

app = FastAPI()


@app.exception_handler(TicketNotFound)
def ticket_not_found_handler(request: Request, exc: TicketNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Ticket {exc.args[0]} not found"},
    )


@app.exception_handler(TicketAlreadyClosed)
def ticket_already_closed_handler(request: Request, exc: TicketAlreadyClosed):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Ticket {exc.args[0]} is closed"},
    )

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(router)
