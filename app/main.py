from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from router import router
from services import TicketNotFound

app = FastAPI()


@app.exception_handler(TicketNotFound)
def ticket_not_found_handler(request: Request, exc: TicketNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Ticket {exc.args[0]} not found"},
    )

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(router)
