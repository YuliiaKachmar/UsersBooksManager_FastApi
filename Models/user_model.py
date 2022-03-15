from sqlalchemy import Column, Integer, String, Boolean

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80))
    surname = Column(String(80))
    email = Column(String(80), unique=True)
    country = Column(String(80))
    password = Column(String(80))
    is_admin = Column(Boolean)

    def __repr__(self):
        return f'UserModel(name={self.name}, surname={self.surname}, email={self.email}, country={self.country}, password={self.password}is_admin={self.is_admin})'