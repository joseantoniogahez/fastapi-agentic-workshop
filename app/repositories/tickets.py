from datetime import datetime, timezone
from typing import Optional

from domain import TicketData
from models import Ticket
from schemas import TicketStatus
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
        return list(
            self._session.query(Ticket)
            .filter(Ticket.deleted_at.is_(None))
            .all()
        )

    def get(self, ticket_id: int) -> Optional[Ticket]:
        ticket = self._session.get(Ticket, ticket_id)
        return ticket if ticket is not None and ticket.deleted_at is None else None

    def update(self, ticket: Ticket, changes: dict) -> Ticket:
        for field, value in changes.items():
            setattr(ticket, field, value)
        self._session.commit()
        self._session.refresh(ticket)
        return ticket

    def close(self, ticket: Ticket) -> Ticket:
        ticket.status = TicketStatus.CLOSED
        self._session.commit()
        self._session.refresh(ticket)
        return ticket

    def delete(self, ticket: Ticket) -> None:
        ticket.deleted_at = datetime.now(timezone.utc)
        self._session.commit()
