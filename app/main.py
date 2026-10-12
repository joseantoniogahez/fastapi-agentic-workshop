from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

tickets = []

@app.post("/tickets")
def create_ticket(ticket: dict):
    tickets.append(ticket)
    return ticket

@app.get("/tickets")
def list_tickets():
    return tickets
