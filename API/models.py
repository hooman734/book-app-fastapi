import uuid

from sqlalchemy import Column, Integer, String
from database import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    title = Column(String)
    description = Column(String, nullable=True)
    rating = Column(Integer, default=0)
