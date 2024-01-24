from fastapi import Depends, status, APIRouter, Response
from sqlalchemy.orm import Session

from api.enums import ApiVersion, EndpointType
from api.v1.schemas.author import AuthorSchemaResponse, AuthorSchemaRequest, AuthorSchemaPatch
from db.database import get_db
from db.models.author import Author

router = APIRouter(prefix=f"{ApiVersion.V1}/{EndpointType.internal}/author", tags=["Author"])


@router.get("/", response_model=list[AuthorSchemaResponse])
async def get_authors(db: Session = Depends(get_db)):
    authors = await Author.get_all(db)
    return authors


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AuthorSchemaResponse)
async def create_author(payload: AuthorSchemaRequest = Depends(), db: Session = Depends(get_db)):
    new_author = Author.create_author(db, payload)
    return new_author


@router.patch("/{author_id}", response_model=AuthorSchemaResponse)
async def update_author(author_id: str, payload: AuthorSchemaPatch = Depends(), db: Session = Depends(get_db)):
    author = await Author.update_author(db, author_id, payload)
    return author


@router.get("/{author_id}", response_model=AuthorSchemaResponse)
async def get_author(author_id: str, db: Session = Depends(get_db)):
    author = await Author.get_by_id(db, author_id)
    return author


@router.delete("/{author_id}")
async def delete_author(author_id: str, db: Session = Depends(get_db)):
    await Author.delete_author(db, author_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
