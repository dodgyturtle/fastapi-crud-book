from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger
from sqlalchemy.orm import Session

from api.v1.schemas.reader import ReaderSchemaResponse
from db.database import get_db, pwd_context
from db.models.reader import Reader


async def verify_and_get_reader(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())], db: Session = Depends(get_db)
) -> ReaderSchemaResponse:
    reader = db.query(Reader).filter(Reader.username == credentials.username).first()
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No reader with this id: {credentials.username} found",
        )
    try:
        is_correct = pwd_context.verify(credentials.password, reader.password)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed check password",
        )
    if not is_correct:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid password for {credentials.username}",
        )
    return reader
