from fastapi import Depends, status, APIRouter, Response
from sqlalchemy.orm import Session

from api.enums import ApiVersion, EndpointType
from api.v1.schemas.book import BookSchemaResponse, BookSchemaRequest, BookSchemaPatch
from db.database import get_db
from db.models.book import Book

router = APIRouter(prefix=f"{ApiVersion.V1}/{EndpointType.internal}/book", tags=["Book"])


@router.get("/", response_model=list[BookSchemaResponse])
async def get_books(db: Session = Depends(get_db)):
    books = await Book.get_all(db)
    return books


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookSchemaResponse)
async def create_book(payload: BookSchemaRequest = Depends(), db: Session = Depends(get_db)):
    book = await Book.create_book(db, payload)
    return book


@router.patch("/{book_id}", response_model=BookSchemaResponse)
async def update_book(book_id: str, payload: BookSchemaPatch = Depends(), db: Session = Depends(get_db)):
    book = await Book.update_book(db, book_id, payload)
    return book


@router.get("/{book_id}", response_model=BookSchemaResponse)
async def get_book(book_id: str, db: Session = Depends(get_db)):
    book = await Book.get_by_id(db, book_id)
    return book


@router.delete("/{book_id}")
async def delete_book(book_id: str, db: Session = Depends(get_db)):
    await Book.delete_book(db, book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
