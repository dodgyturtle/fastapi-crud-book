from typing import Type

from fastapi import status, HTTPException
from loguru import logger
from passlib.context import CryptContext
from psycopg2 import errors
from sqlalchemy import Column, String, Integer, Table, ForeignKey, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, Session

from api.v1.schemas.book import BookSearch, SortingBookBy
from api.v1.schemas.reader import ReaderSchemaRequest, ReaderSchemaResponse, ReaderSchemaPatch
from db.base import BaseModel
from db.database import pwd_context
from db.models.author import Author
from db.models.book import Book
from settings import settings


class Reader(BaseModel):
    __tablename__ = "reader"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=True)

    @classmethod
    async def create_reader(cls, session: Session, reader: ReaderSchemaRequest) -> ReaderSchemaResponse:
        try:
            reader.password = pwd_context.hash(reader.password)
            new_reader = Reader(**reader.model_dump())
            session.add(new_reader)
            session.commit()
            session.refresh(new_reader)
            return new_reader
        except IntegrityError as e:
            if isinstance(e.orig, errors.lookup("23505")):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Reader {reader.username} already exist",
                )
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed create reader: {reader}",
            )

    @classmethod
    async def update_reader(
        cls, session: Session, current_reader: ReaderSchemaResponse, new_reader: ReaderSchemaPatch
    ) -> ReaderSchemaResponse:
        try:
            reader_query = session.query(Reader).filter(Reader.id == current_reader.id)
            if new_reader.password:
                new_reader.password = pwd_context.hash(new_reader.password)
            reader_query.update(new_reader.model_dump(exclude_unset=True, exclude_none=True), synchronize_session=False)
            session.commit()
            session.refresh(current_reader)
            return current_reader
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed update reader with this id: {current_reader.id}",
            )

    @classmethod
    async def delete_reader(cls, session: Session, reader: ReaderSchemaResponse):
        try:
            reader_query = session.query(Reader).filter(Reader.id == reader.id)
            reader_query.delete(synchronize_session=False)
            session.commit()
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed delete reader with this id: {reader.id}",
            )

    @classmethod
    async def search_authors_by_params(
        cls, session: Session, params: BookSearch, reader: ReaderSchemaResponse
    ) -> list[Type["Author"]]:
        authors_query = session.query(Author).outerjoin(Book).filter(Author.is_deleted == False)
        if params.sorting_by == SortingBookBy.book_name:
            authors_query = authors_query.order_by(Book.name)
        if params.sorting_by == SortingBookBy.author:
            authors_query = authors_query.order_by(Author.name)
        if params.book_name:
            authors_query = authors_query.filter(func.lower(Book.name).contains(params.book_name.lower()))
        if params.author:
            authors_query = authors_query.filter(func.lower(Author.name).contains(params.author.lower()))
        if reader.age:
            if reader.age < settings.AGE_LIMIT:
                authors_query = authors_query.filter(Book.is_age_limit == False)
        elif params.is_age_limit:
            authors_query = authors_query.filter(Book.is_age_limit == params.is_age_limit)
        else:
            authors_query = authors_query.filter(Book.is_age_limit == False)

        return authors_query.all()

    @classmethod
    async def search_books_by_params(
        cls, session: Session, params: BookSearch, reader: ReaderSchemaResponse
    ) -> list[Type["Book"]]:
        books_query = session.query(Book).join(Author).filter(Author.is_deleted == False)
        if params.sorting_by == SortingBookBy.book_name:
            books_query = books_query.order_by(Book.name)
        if params.sorting_by == SortingBookBy.author:
            books_query = books_query.order_by(Author.name)
        if params.book_name:
            books_query = books_query.filter(func.lower(Book.name).contains(params.book_name.lower()))
        if params.author:
            books_query = books_query.filter(func.lower(Author.name).contains(params.author.lower()))
        if reader.age:
            if reader.age < settings.AGE_LIMIT:
                books_query = books_query.filter(Book.is_age_limit == False)
        elif params.is_age_limit:
            books_query = books_query.filter(Book.is_age_limit == params.is_age_limit)
        else:
            books_query = books_query.filter(Book.is_age_limit == False)
        return books_query.all()
