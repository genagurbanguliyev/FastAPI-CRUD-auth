from db_config.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True)
    email: str = Column(String, unique=True)
    first_name: str = Column(String)
    last_name: str = Column(String)
    hashed_password: str = Column(String)
    is_active: bool = Column(Boolean, default=True)
    role: str = Column(String)
    phone_number: str = Column(String)

    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    address = relationship("Address", back_populates="user_address")

    todos = relationship("Todos", back_populates="owner")


class Todos(Base):
    __tablename__ = "todos"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String)
    description: str = Column(String)
    priority: int = Column(Integer)
    complete: bool = Column(Boolean)
    owner_id: int = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")


class Address(Base):
    __tablename__ = "address"

    id: int = Column(Integer, primary_key=True, index=True)
    address1: str = Column(String)
    address2: str = Column(String)
    city: str = Column(String)
    state: str = Column(String)
    postalcode: str = Column(String)
    apt_num: int = Column(Integer, nullable=True)

    user_address = relationship("Users", back_populates="address")
