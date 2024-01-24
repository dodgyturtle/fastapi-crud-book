from typing import Type

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship, Session

from api.v1.schemas.book import BookSchemaResponse, BookSchemaRequest, BookSchemaPatch
from db.base import BaseModel


class Book(BaseModel):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_age_limit = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("author.id", ondelete="RESTRICT"))
    author = relationship("Author", back_populates="books")

    @classmethod
    async def get_all(cls, session: Session) -> list[Type["Book"]]:
        return session.query(Book).all()

    @classmethod
    async def get_by_id(
        cls,
        session: Session,
        book_id: str,
    ) -> BookSchemaResponse:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No book with this id: {book_id} found")
        return book

    @classmethod
    async def create_book(cls, session: Session, book: BookSchemaRequest) -> BookSchemaResponse:
        try:
            new_book = Book(**book.model_dump())
            session.add(new_book)
            session.commit()
            session.refresh(new_book)

        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed create book: {book}",
            )
        return new_book

    @classmethod
    async def update_book(cls, session: Session, book_id: str, book: BookSchemaPatch) -> BookSchemaResponse:
        try:
            book_query = session.query(Book).filter(Book.id == book_id)
            book_db = book_query.first()
            if not book_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"No book with this id: {book_id} found"
                )
            book_query.update(book.model_dump(exclude_unset=True, exclude_none=True), synchronize_session=False)
            session.commit()
            session.refresh(book_db)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed update book with this id: {book_id}",
            )
        return book_db

    @classmethod
    async def delete_book(cls, session: Session, book_id: str):
        try:
            book_query = session.query(Book).filter(Book.id == book_id)
            book = book_query.first()
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"No book with this id: {book_id} found"
                )
            book_query.delete(synchronize_session=False)
            session.commit()
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed delete book with this id: {book_id}",
            )
