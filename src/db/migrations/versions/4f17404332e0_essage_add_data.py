"""essage=add_data

Revision ID: 4f17404332e0
Revises: 2405264f51c6
Create Date: 2024-01-25 13:01:33.826969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Session

from db.database import get_db
from db.models.author import Author
from db.models.book import Book

# revision identifiers, used by Alembic.
revision: str = "4f17404332e0"
down_revision: Union[str, None] = "2405264f51c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    session = Session(op.get_bind())
    new_author1 = Author(name="Автор1")
    new_author2 = Author(name="Автор2")
    new_author3 = Author(name="Автор3", is_deleted=True)
    session.add(new_author1)
    session.add(new_author2)
    session.add(new_author3)
    session.commit()
    session.refresh(new_author1)
    session.refresh(new_author2)
    session.refresh(new_author3)
    books = [
        Book(name="Книга9", is_age_limit=True, author_id=new_author1.id),
        Book(name="Книга8", is_age_limit=False, author_id=new_author1.id),
        Book(name="Книга7", is_age_limit=True, author_id=new_author1.id),
        Book(name="Книга6", is_age_limit=False, author_id=new_author2.id),
        Book(name="Книга5", is_age_limit=True, author_id=new_author2.id),
        Book(name="Книга4", is_age_limit=True, author_id=new_author2.id),
        Book(name="Книга3", is_age_limit=False, author_id=new_author3.id),
        Book(name="Книга2", is_age_limit=False, author_id=new_author3.id),
        Book(name="Книга1", is_age_limit=False, author_id=new_author3.id),
    ]
    for book in books:
        session.add(book)
    session.commit()


def downgrade() -> None:
    pass
