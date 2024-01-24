from fastapi import Depends, status, APIRouter
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session

from api.enums import ApiVersion
from api.v1.schemas.author import AuthorSchemaResponse
from api.v1.schemas.book import BookSchemaResponse, BookSearch
from api.v1.schemas.reader import ReaderSchemaResponse, ReaderSchemaRequest, ReaderSchemaPatch
from db.database import get_db
from db.models.reader import Reader
from utils.utils import verify_and_get_reader

router = APIRouter(prefix=f"{ApiVersion.V1}/reader", tags=["Reader"])


@router.get("/", response_model=ReaderSchemaResponse)
async def get_readers(reader: ReaderSchemaResponse = Depends(verify_and_get_reader)):
    return reader


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReaderSchemaResponse,
)
async def create_reader(payload: ReaderSchemaRequest = Depends(), db: Session = Depends(get_db)):
    reader = await Reader.create_reader(db, payload)
    return reader


@router.patch("/", response_model=ReaderSchemaResponse)
async def update_reader(
    reader: ReaderSchemaResponse = Depends(verify_and_get_reader),
    payload: ReaderSchemaPatch = Depends(),
    db: Session = Depends(get_db),
):
    reader = await Reader.update_reader(db, reader, payload)
    return reader


@router.delete("/", response_model=Response)
async def delete_reader(reader: ReaderSchemaResponse = Depends(verify_and_get_reader), db: Session = Depends(get_db)):
    await Reader.delete_reader(db, reader)
    return Response(
        description="Reader deleted",
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.get("/books", response_model=list[BookSchemaResponse], summary="Get books for Reader")
async def get_reader_books(
    params: BookSearch = Depends(),
    reader: ReaderSchemaResponse = Depends(verify_and_get_reader),
    db: Session = Depends(get_db),
):
    books = await Reader.search_books_by_params(db, params, reader)
    return books


@router.get("/authors", response_model=list[AuthorSchemaResponse], summary="Get authors for Reader")
async def get_reader_authors(
    params: BookSearch = Depends(),
    reader: ReaderSchemaResponse = Depends(verify_and_get_reader),
    db: Session = Depends(get_db),
):
    authors = await Reader.search_authors_by_params(db, params, reader)
    return authors
