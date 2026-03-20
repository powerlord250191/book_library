from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from typing import Annotated

str_150 = String(150)
str_50 = String(50)
int_pk = Annotated[int, mapped_column(Integer, autoincrement=True, primary_key=True)]


class Base(DeclarativeBase):
    pass


engine = create_engine('sqlite:///library_books.db')
Base.metadata.create_all(bind=engine)
