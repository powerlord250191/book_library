from .base import Base, str_50, int_pk
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(str_50)
    surname: Mapped[str] = mapped_column(str_50)

    def __repr__(self):
        return f"Автор: {self.surname}. {self.name}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    books = relationship("Book", backref="author", lazy="joined", cascade="all, delete-orphan")
