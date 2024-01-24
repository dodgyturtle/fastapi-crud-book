from pydantic import (
    BaseModel,
)


class AuthorSchemaRequest(BaseModel):
    name: str


class AuthorSchemaResponse(AuthorSchemaRequest):
    id: int
    books: list["BookSchema"] | None


class AuthorSchemaPatch(BaseModel):
    name: str | None = None


from api.v1.schemas.book import BookSchema

AuthorSchemaResponse.model_rebuild()
