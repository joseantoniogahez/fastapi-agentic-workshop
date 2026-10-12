from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(
    "sqlite:///supportdesk.db",
    connect_args={"check_same_thread": False},
)

Base.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
