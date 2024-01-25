from enum import StrEnum

from pydantic import (
    BaseModel,
)

from api.v1.schemas.book import BookSchemaRequest


class ReaderSchema(BaseModel):
    username: str
    age: int | None = None


class ReaderSchemaResponse(ReaderSchema):
    id: int


class ReaderSchemaRequest(ReaderSchema):
    password: str


class ReaderSchemaPatch(BaseModel):
    username: str | None = None
    password: str | None = None
    age: int | None = None
