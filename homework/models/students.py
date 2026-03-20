import csv
import os.path

from sqlalchemy.ext.associationproxy import association_proxy

from .base import Base, str_50, engine, int_pk
from sqlalchemy import BOOLEAN, Float, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(str_50, nullable=False)
    surname: Mapped[str] = mapped_column(str_50, nullable=False)
    phone: Mapped[str] = mapped_column(str_50, nullable=False)
    email: Mapped[str] = mapped_column(str_50, nullable=False)
    average_score: Mapped[float] = mapped_column(Float, nullable=False)
    scholarship_boolean: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)

    student_receiving_books = relationship(
        'ReceivingBook',
        back_populates='student_with_book',
        cascade="all, delete-orphan",
        lazy='joined'
    )

    receive = association_proxy("student_receiving_books", "book")

    def __repr__(self):
        return (f"Студент: {self.surname}. {self.name}\n"
                f"Контактные данные:\nтелефон - {self.phone}, электронная почта - {self.email}\n"
                f"Средний балл - {self.average_score}\n"
                f"Стипендия - {self.scholarship_boolean}")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_all_students_scholarships(cls):
        with Session(engine) as session:
            students = session.scalars(select(Student).where(cls.scholarship_boolean == '1')).unique().all()
        return students

    @classmethod
    def get_all_students_by_average_point(cls, average_point: float):
        with Session(engine) as session:
            students = session.scalars(select(Student).filter(Student.average_score > average_point)).unique().all()
        return students

    @classmethod
    def inserting_from_file(cls, file):
        file.save(os.path.join(file.filename))
        with open(file.filename, "r") as filename:
            fieldnames = ["name", "surname", "phone", "email"]
            read_file = csv.DictReader(f=filename, fieldnames=fieldnames, delimiter=";")
            dict_list = [string_ for string_ in read_file]
            with Session(engine) as session:
                session.bulk_insert_mappings(Student, dict_list)
                session.commit()
        return True
