from app.models.user import User
from app.db.db import engine
from sqlmodel import Session, select

def addUser(user:User)->None:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

def getUserByEmail(email:str)-> User | None:
    with Session(engine) as session:
        stmt = select(User).where(User.email==email)
        result = session.exec(stmt).first()
        return result
    