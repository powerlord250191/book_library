from models.author import Author
from models.books import Book
from models.students import Student
from models.receiving_books import ReceivingBook
from models.base import Base
from datetime import date
from models.base import engine
from sqlalchemy.orm import Session


def create_authors_and_books():
    authors = [
        Author(name='Leo', surname='Tolstoy'),
        Author(name='Joan', surname='Rouling'),
        Author(name='George', surname='Martin'),
        Author(name='Aleksandr', surname='Pushkin'),
        Author(name='Michail', surname='Bulgakov')
    ]

    authors[0].books.append(Book(
        name='Война и мир',
        count=4,
        release_date=date(1868, 1, 1)
    ))
    authors[0].books.append(Book(
        name='Анна Каренина',
        count=2,
        release_date=date(1873, 1, 1)
    ))

    authors[1].books.append(Book(
        name='Гарри Поттер и Философский камень',
        count=4,
        release_date=date(1997, 1, 1)
    ))
    authors[1].books.append(Book(
        name='Гарри Поттер и Принц-полукровка',
        count=4,
        release_date=date(2007, 1, 1)
    ))
    authors[2].books.append(Book(
        name='Песнь льда и пламени',
        count=3,
        release_date=date(1966, 1, 1)
    ))
    authors[2].books.append(Book(
        name='Битва королей',
        count=1,
        release_date=date(1998, 1, 1)
    ))
    authors[2].books.append(Book(
        name='Буря мечей',
        count=2,
        release_date=date(1998, 11, 1)
    ))
    authors[3].books.append(Book(
        name='Евгений Онегин',
        count=2,
        release_date=date(1825, 1, 1)
    ))
    authors[3].books.append(Book(
        name='Дубровский',
        count=3,
        release_date=date(1833, 1, 1)
    ))
    authors[3].books.append(Book(
        name='Капитанская дочка',
        count=5,
        release_date=date(1836, 1, 1)
    ))
    authors[4].books.append(Book(
        name='Морфий',
        count=5,
        release_date=date(1926, 1, 1)
    ))
    authors[4].books.append(Book(
        name='Собачье сердце',
        count=4,
        release_date=date(1925, 1, 1)
    ))
    with Session(engine) as session:
        session.add_all(authors)
        session.commit()


def create_students():
    students = [
        Student(
            name="Sol",
            surname="Goodman",
            phone='+79562314255',
            email='better_call_sol@albukerke.com',
            average_score=4.3,
            scholarship_boolean=True
        ),
        Student(
            name="Hank",
            surname="Shreider",
            phone='+79524585632',
            email='shreider@five.com',
            average_score=3.2,
            scholarship_boolean=False
        ),
        Student(
            name="Walter",
            surname="White",
            phone='89634781236',
            email='heisenberg@mail.ru',
            average_score=4.8,
            scholarship_boolean=True
        ),
        Student(
            name="Jassy",
            surname="Pinkman",
            phone='89652147563',
            email='the_capitan@chilli_peper.com',
            average_score=3.7,
            scholarship_boolean=False
        ),
        Student(
            name="Gustavo",
            surname="Fring",
            phone='+79541111213',
            email='los_poyes_ermanos@drug_empire.com',
            average_score=4.6,
            scholarship_boolean=True
        )
    ]
    with Session(engine) as session:
        session.add_all(students)
        session.commit()


def create_receiving_students_by_books():
    receiving_books = []
    rb_1 = ReceivingBook(
        student_id=1,
        book_id=2,
        date_of_issue=date(2025, 11, 1),
        date_of_return=date(2025, 11, 19)
    )
    rb_2 = ReceivingBook(
        student_id=1,
        book_id=3,
        date_of_issue=date(2025, 10, 12),
        date_of_return=date(2025, 11, 19)
    )
    rb_3 = ReceivingBook(
        student_id=2,
        book_id=8,
        date_of_issue=date(2025, 9, 12),
        date_of_return=date(2025, 9, 22)
    )
    rb_4 = ReceivingBook(
        student_id=4,
        book_id=11,
        date_of_issue=date(2025, 5, 12),
        date_of_return=date(2025, 11, 22)
    )
    rb_4 = ReceivingBook(
        student_id=4,
        book_id=6,
        date_of_issue=date(2025, 1, 22),
    )
    rb_5 = ReceivingBook(
        student_id=5,
        book_id=1,
        date_of_issue=date(2025, 5, 12),
        date_of_return=date(2025, 5, 25)
    )
    rb_6 = ReceivingBook(
        student_id=5,
        book_id=5,
        date_of_issue=date(2025, 5, 25),
        date_of_return=date(2025, 6, 14)
    )
    receiving_books.append(rb_1)
    receiving_books.append(rb_2)
    receiving_books.append(rb_3)
    receiving_books.append(rb_4)
    receiving_books.append(rb_5)
    receiving_books.append(rb_6)

    with Session(engine) as session:
        session.add_all(receiving_books)
        session.commit()


def insert_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    create_authors_and_books()
    create_students()
    create_receiving_students_by_books()

