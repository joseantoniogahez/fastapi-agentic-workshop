from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Ticket
from repositories import TicketRepository


def test_repository_persists_ticket_in_sqlite(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'repository.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        repository = TicketRepository(session)
        ticket = Ticket(
            title="SQLite persistence",
            description="Stored by the repository",
            priority="low",
            status="open",
        )
        saved = repository.create(ticket)
        ticket_id = saved.id

    with session_factory() as session:
        persisted = TicketRepository(session).get(ticket_id)

    assert persisted is not None
    assert persisted.title == "SQLite persistence"
    assert persisted.priority == "low"

    engine.dispose()
