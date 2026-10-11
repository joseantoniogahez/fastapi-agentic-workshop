from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(
    "sqlite:///supportdesk.db",
    connect_args={"check_same_thread": False},
)


def get_session():
    with Session(engine) as session:
        yield session
