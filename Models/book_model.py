from sqlalchemy import Column, Integer, String

from db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80))
    author = Column(String(80))
    pages = Column(Integer)

    def __repr__(self):
        return f'Book(name={self.name}, author={self.author}, pages={self.pages})'

