import uvicorn
from fastapi import FastAPI
from fastapi.security import HTTPBasic
from loguru import logger
from passlib.context import CryptContext
from uvicorn import Config

from api.v1.routes import (
    book,
    reader,
    author,
)


def make_app() -> FastAPI:
    app = FastAPI(
        debug=True,
        title="CRUD BOOK",
        version="0.0.1",
    )
    include_routers(app=app)
    return app


def include_routers(app: FastAPI) -> None:
    routers = (
        book.router,
        author.router,
        reader.router,
    )
    for router in routers:
        app.include_router(router=router)


_app = make_app()


def main() -> None:
    for route in _app.routes:
        logger.info(route)
    server = uvicorn.Server(config=Config(app=_app, host="0.0.0.0", port=8000))
    server.run()


if __name__ == "__main__":
    main()
