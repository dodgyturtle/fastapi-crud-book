from enum import StrEnum

from pydantic import (
    BaseModel,
)


class BookSchema(BaseModel):
    name: str
    is_age_limit: bool


class BookSchemaResponse(BookSchema):
    id: int
    author: "AuthorSchemaRequest"


class BookSchemaRequest(BookSchema):
    author_id: int | None = None


class BookSchemaPatch(BaseModel):
    name: str | None = None
    is_age_limit: bool | None = None
    author_id: int | None = None


class SortingBookBy(StrEnum):
    author = "author"
    book_name = "book_name"


class BookSearch(BaseModel):
    sorting_by: SortingBookBy
    author: str | None = None
    book_name: str | None = None
    is_age_limit: bool | None = None


from api.v1.schemas.author import AuthorSchemaRequest

BookSchemaResponse.model_rebuild()
