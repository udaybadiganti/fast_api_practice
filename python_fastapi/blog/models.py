from sqlalchemy import Column, String, Integer
from .database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)
