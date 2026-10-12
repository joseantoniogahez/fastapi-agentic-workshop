from models import Base, Ticket
from repositories import TicketRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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


def test_repository_lists_active_tickets_in_id_order(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'repository-list.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        repository = TicketRepository(session)
        first = repository.create(Ticket(title="First ticket", description="Details"))
        second = repository.create(Ticket(title="Second ticket", description="Details"))
        third = repository.create(Ticket(title="Third ticket", description="Details"))
        repository.delete(first)
        expected_ids = [second.id, third.id]

    with session_factory() as session:
        tickets = TicketRepository(session).list()

    assert [ticket.id for ticket in tickets] == expected_ids
    engine.dispose()
