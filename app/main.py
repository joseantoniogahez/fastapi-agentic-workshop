from database import create_tables
from fastapi import FastAPI
from routers.tickets import router as tickets_router

app = FastAPI()


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(tickets_router, prefix="/api/v1/tickets", tags=["tickets"])
