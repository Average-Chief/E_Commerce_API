from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def get_session():
    return Session(engine)

