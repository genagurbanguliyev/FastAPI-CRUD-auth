from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String)
    email: str = Column(String)
    first_name: str = Column(String)
    last_name: str = Column(String)
    hashed_password: str = Column(String)
    is_active: bool = Column(Boolean, default=False)
    role: str = Column(String)

class Todos(Base):
    __tablename__ = "todos"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String)
    description: str = Column(String)
    priority: int = Column(Integer)
    complete: bool = Column(Boolean)
