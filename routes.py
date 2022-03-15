from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from fastapi import HTTPException, Depends

from db import get_db
from Schemas import user_schema, book_schema
from Repositories.user_repositories import UserRepo
from Repositories.book_repositories import BookRepo

from auth import Auth

router = APIRouter()
auth_handler = Auth()


@router.post('/registration', tags=["User"], response_model=user_schema.User, status_code=201)
async def create_user(user_request: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = UserRepo.fetch_by_email(db, email=user_request.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists!")

    return await UserRepo.create(db=db, user=user_request)


@router.post('/login', tags=["User"])
def login(user_details: user_schema.UserLogIn, db: Session = Depends(get_db)):
    db_user = UserRepo.fetch_by_email(db, email=user_details.email)
    if db_user is None:
        return HTTPException(status_code=401, detail='Invalid data')
    if not auth_handler.verify_password(user_details.password, db_user.password):
        return HTTPException(status_code=401, detail='Invalid password')

    access_token = auth_handler.encode_token(db_user)
    return access_token


@router.put('/users/{user_id}', tags=["User"], response_model=user_schema.User)
async def update_user(user_id: int, user_request: user_schema.User, db: Session = Depends(get_db)):
    db_user = UserRepo.fetch_by_id(db, user_id)
    if db_user:
        update_item_encoded = jsonable_encoder(user_request)
        db_user.name = update_item_encoded['name']
        db_user.surname = update_item_encoded['surname']
        db_user.email = update_item_encoded['email']
        db_user.country = update_item_encoded['country']
        db_user.is_admin = update_item_encoded['is_admin']
        return await UserRepo.update(db=db, user_data=db_user)
    else:
        raise HTTPException(status_code=400, detail="User not found with the given ID")


@router.get('/users', tags=["User"], response_model=List[user_schema.User])
def get_all_users(email: Optional[str] = None, db: Session = Depends(get_db)):
    if email:
        users = []
        db_user = UserRepo.fetch_by_email(db, email)
        users.append(db_user)
        return users
    else:
        return UserRepo.fetch_all(db)


@router.get('/users/{user_id}', tags=["User"], response_model=user_schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserRepo.fetch_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_user


@router.delete('/users/{user_email}', tags=["User"])
async def delete_user(user_email: str, db: Session = Depends(get_db)):
    db_user = UserRepo.fetch_by_email(db, user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await UserRepo.delete(db, user_email)
    return "User deleted successfully!"


@router.post('/book', tags=["Book"], response_model=book_schema.Book, status_code=201)
async def create_book(book_request: book_schema.BookCreate, db: Session = Depends(get_db)):
    db_book = BookRepo.fetch_by_name(db, name=book_request.name)
    print(db_book)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists!")

    return await BookRepo.create(db=db, book=book_request)


@router.put('/books/{book_id}', tags=["Book"], response_model=book_schema.Book)
async def update_user(book_id: int, book_request: book_schema.Book, db: Session = Depends(get_db)):
    db_book = BookRepo.fetch_by_id(db, book_id)
    if db_book:
        update_item_encoded = jsonable_encoder(book_request)
        db_book.name = update_item_encoded['name']
        db_book.author = update_item_encoded['author']
        db_book.pages = update_item_encoded['pages']
        return await BookRepo.update(db=db, book_data=db_book)
    else:
        raise HTTPException(status_code=400, detail="Book not found with the given ID")


@router.get('/books', tags=["Book"], response_model=List[book_schema.Book])
def get_all_books(name: Optional[str] = None, db: Session = Depends(get_db)):
    if name:
        books = []
        db_books = BookRepo.fetch_by_name(db, name)
        print(db_books)
        books.append(db_books)
        return books
    else:
        return BookRepo.fetch_all(db)


@router.get('/books/{book_id}', tags=["Book"], response_model=book_schema.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = BookRepo.fetch_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found with the given ID")
    return db_book


@router.delete('/books/{book_id}', tags=["Book"])
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = BookRepo.fetch_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found with the given ID")
    await BookRepo.delete(db, book_id)
    return "Book deleted successfully!"
