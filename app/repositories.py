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

    def get(self, ticket_id: int):
        ticket = self.session.get(Ticket, ticket_id)
        if ticket is None or ticket.is_deleted:
            return None
        return ticket

    def save(self, ticket: Ticket):
        self.session.commit()
        self.session.refresh(ticket)
        return ticket

    def delete(self, ticket: Ticket):
        ticket.is_deleted = True
        self.session.commit()
