from domain import TicketData
from models import Ticket
from sqlalchemy.orm import Session


class TicketRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: TicketData) -> Ticket:
        ticket = Ticket(**data.__dict__)
        self._session.add(ticket)
        self._session.commit()
        self._session.refresh(ticket)
        return ticket

    def list(self) -> list[Ticket]:
        return list(self._session.query(Ticket).all())
