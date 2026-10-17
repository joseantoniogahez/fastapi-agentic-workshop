from database import Base
from domain import TicketData
from repositories.tickets import TicketRepository
from schemas import Priority, TicketStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_create_get_update_close_and_soft_delete(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'tickets.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    try:
        with session_factory() as session:
            repository = TicketRepository(session)
            created = repository.create(
                TicketData("Problem", "Details", Priority.MEDIUM)
            )
            ticket_id = created.id
            assert repository.get(ticket_id).title == "Problem"
            repository.update(created, {"title": "Updated title"})
            assert repository.get(ticket_id).title == "Updated title"
            repository.close(created)
            assert repository.get(ticket_id).status == TicketStatus.CLOSED
            repository.delete(created)
            assert repository.get(ticket_id) is None
            assert repository.list() == []
            assert session.get(type(created), ticket_id) is not None
    finally:
        engine.dispose()
