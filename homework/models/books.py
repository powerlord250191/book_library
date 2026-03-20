from .base import Base, str_150, int_pk, engine
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import ForeignKey, Integer, DATE, select
from datetime import date


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(str_150, nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=1)
    release_date: Mapped[date] = mapped_column(DATE, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))

    def __repr__(self):
        return (f"Книга: {self.name} автор - {self.author_id},"
                f" количество книг в библиотеке - {self.count}, дата публикации - {self.release_date}")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_books_by_author(cls, id):
        with Session(engine) as session:
            books_by_author = session.scalars(select(Book.count).where(Book.author_id == id)).all()
            return sum(books_by_author)
