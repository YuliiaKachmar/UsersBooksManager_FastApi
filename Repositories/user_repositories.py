from sqlalchemy.orm import Session

from Models import user_model as model
from Schemas import user_schema as schema
from auth import Auth

auth_handler = Auth()


class UserRepo:

    async def create(db: Session, user: schema.UserCreate):
        db_user = model.User(name=user.name, surname=user.surname, email=user.email, country=user.country, password=auth_handler.encode_password(user.password,), is_admin=user.is_admin)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def fetch_by_id(db: Session, _id):
        return db.query(model.User).filter(model.User.id == _id).first()

    def fetch_by_email(db: Session, email):
        return db.query(model.User).filter(model.User.email == email).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(model.User).offset(skip).limit(limit).all()

    async def delete(db: Session, user_email):
        db_user = db.query(model.User).filter_by(email=user_email).first()
        db.delete(db_user)
        db.commit()

    async def update(db: Session, user_data):
        updated_user = db.merge(user_data)
        db.commit()
        return updated_user