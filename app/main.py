from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()
from database import engine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import Base
from router import router
from services import (
    AIProviderUnavailable,
    AIResponseInvalid,
    TicketAlreadyClosed,
    TicketNotFound,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


def create_app(*, manage_database: bool = True) -> FastAPI:
    app = FastAPI(lifespan=lifespan if manage_database else None)

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

    @app.exception_handler(AIProviderUnavailable)
    def ai_provider_unavailable_handler(request: Request, exc: AIProviderUnavailable):
        return JSONResponse(
            status_code=503,
            content={"detail": "AI provider unavailable"},
        )

    @app.exception_handler(AIResponseInvalid)
    def ai_response_invalid_handler(request: Request, exc: AIResponseInvalid):
        return JSONResponse(
            status_code=502,
            content={"detail": "AI provider returned an invalid response"},
        )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.include_router(router)
    return app


app = create_app()
