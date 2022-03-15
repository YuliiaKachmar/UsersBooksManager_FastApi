from sqlalchemy.orm import Session

from Models import book_model as model
from Schemas import book_schema as schemas


class BookRepo:

    async def create(db: Session, book: schemas.BookCreate):
        db_book = model.Book(name=book.name, author=book.author, pages=book.pages)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    def fetch_by_id(db: Session, _id: int):
        return db.query(model.Book).filter(model.Book.id == _id).first()

    def fetch_by_name(db: Session, name: str):
        return db.query(model.Book).filter(model.Book.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(model.Book).offset(skip).limit(limit).all()

    async def delete(db: Session, _id: int):
        db_book = db.query(model.Book).filter_by(id=_id).first()
        db.delete(db_book)
        db.commit()

    async def update(db: Session, book_data):
        updated_book = db.merge(book_data)
        db.commit()
        return updated_book