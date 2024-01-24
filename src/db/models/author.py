from typing import Type

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import expression

from api.v1.schemas.author import AuthorSchemaRequest, AuthorSchemaResponse, AuthorSchemaPatch
from db.base import BaseModel
from db.models.book import Book


class Author(BaseModel):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, server_default=expression.false(), default=False)
    books = relationship(Book, back_populates="author")

    @classmethod
    async def get_all(cls, session: Session) -> list[Type["Author"]]:
        return session.query(Author).all()

    @classmethod
    async def get_by_id(
        cls,
        session: Session,
        author_id: str,
    ) -> AuthorSchemaResponse:
        author = session.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No author with this id: {author_id} found",
            )
        return author

    @classmethod
    async def create_author(cls, session: Session, author: AuthorSchemaRequest) -> AuthorSchemaResponse:
        try:
            new_author = Author(**author.model_dump())
            session.add(new_author)
            session.commit()
            session.refresh(new_author)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed create author: {author}",
            )
        return new_author

    @classmethod
    async def update_author(cls, session: Session, author_id: str, author: AuthorSchemaPatch) -> AuthorSchemaResponse:
        try:
            author_query = session.query(Author).filter(Author.id == author_id)
            author_db = author_query.first()
            if not author_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No author with this id: {author_id} found",
                )
            author_query.update(author.model_dump(exclude_unset=True, exclude_none=True), synchronize_session=False)
            session.commit()
            session.refresh(author_db)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed update author with this id: {author_id}",
            )
        return author_db

    @classmethod
    async def delete_author(cls, session: Session, author_id: str):
        try:
            author_query = session.query(Author).filter(Author.id == author_id)
            author = author_query.first()
            if not author:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No author with this id: {author_id} found",
                )
            if not author.books:
                author_query.delete(synchronize_session=False)
            else:
                author_query.update({"is_deleted": True}, synchronize_session=False)
                session.commit()
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed delete author with this id: {author_id}",
            )
