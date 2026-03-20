from datetime import datetime, date
from sqlalchemy.ext.hybrid import hybrid_property
from .base import Base, engine
from .students import Student
from .books import Book
from sqlalchemy import select, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from calendar import monthrange


class ReceivingBook(Base):
    __tablename__ = "receiving_books"

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id', ondelete="CASCADE"), primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id', ondelete="CASCADE"), primary_key=True)
    date_of_issue: Mapped[date] = mapped_column(default=datetime.now)
    date_of_return: Mapped[date] = mapped_column(nullable=True)

    student_with_book: Mapped["Student"] = relationship(
        back_populates='student_receiving_books',
        cascade="all, delete",
        lazy="joined"
    )
    book: Mapped["Book"] = relationship()

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return ' '.join({c.name: getattr(self, c.name) for c in self.__table__.columns})

    @hybrid_property
    def count_date_with_book(self):
        """Количество дней, которые книга находится у студента"""
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (datetime.now().date() - self.date_of_issue).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        """SQL выражение для подсчета дней"""
        return func.julianday(func.coalesce(cls.date_of_return,
                                            datetime.now().date())) - func.julianday(cls.date_of_issue)

    @classmethod
    def debtors_by_14_days(cls):
        """Студенты, которые держат книги более 14 дней"""
        with Session(engine) as session:
            debtors = session.scalars(select(cls).where(
                cls.count_date_with_book > 14
            ).group_by(cls.student_id)).unique().all()
        return [debtor.to_json() for debtor in debtors]

    @classmethod
    def average_count_books(cls):
        month = datetime.now().month
        days = monthrange(datetime.now().year, month)[1]
        with Session(engine) as session:
            books = session.scalars(select(ReceivingBook).where(
                ReceivingBook.date_of_issue.between(
                    datetime(2025, month, 1), datetime(2025, month, days))
            )).unique().all()
        return len(books)

    @classmethod
    def find_the_most_popular_book(cls):
        with Session(engine) as session:
            books = session.execute(select(ReceivingBook.book_id, func.count(ReceivingBook.book_id)).where(
                ReceivingBook.student_id.in_(
                    session.scalars(select(Student.id).where(Student.average_score > 4))
                )).group_by(ReceivingBook.book_id)).unique().all()
            popular_book_id = max(books, key=lambda book: book[1])[0]
            popular_book_title = session.scalars(select(Book.name).where(Book.id == popular_book_id)).unique().first()
        return popular_book_title

    @classmethod
    def top_readers(cls):
        with Session(engine) as session:
            students = session.scalars(select(Student.name).where(
                Student.id.in_(session.scalars(select((
                    ReceivingBook.student_id
                )).filter(
                    ReceivingBook.date_of_issue.between(date(2025, 1, 1), date(2025, 12, 31))
                ).group_by(ReceivingBook.student_id).order_by(func.count(ReceivingBook.book_id).desc()).limit(3)
                                               )))).unique().all()
        return students
