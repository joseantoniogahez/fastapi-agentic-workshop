from database import Session
from models import Ticket


class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, ticket: Ticket):
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket
