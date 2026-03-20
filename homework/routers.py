from models.receiving_books import ReceivingBook
from models.base import Base, engine
from models.books import Book
from models.students import Student
from flask import Flask, jsonify, request
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

app = Flask(__name__)


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route('/')
def hello_world():
    return 'Hello World!'


# Эндпоинт для получения всех книг в библиотеке
@app.route('/books', methods=["GET"])
def get_all_books():
    with Session(engine) as session:
        books = session.query(Book).all()
    books_list = [book.to_json() for book in books]
    return jsonify(books_list), 200


# эндпоинт для получения списка должников по книгам
@app.route("/debtors", methods=["GET"])
def list_of_debtors():
    debtors = ReceivingBook.debtors_by_14_days()
    return jsonify(debtors), 200


# эндпоинт для выдачи книги студенту из библиотеки
@app.route("/outbook", methods=["POST"])
def give_out_a_book():
    student_id = request.form.get('student_id', type=int)
    book_id = request.form.get('book_id', type=int)
    date_of_issue = datetime.now()

    with Session(engine) as session:
        book = session.query(Book).filter(Book.id == book_id).one_or_none()
        if book is not None and book.count >= 1:
            book.id = book.id
            book.name = book.name
            book.release_date = book.release_date
            book.count = book.count - 1
            book.author_id = book.author_id

            book_receiving = ReceivingBook(
                book_id=book_id,
                student_id=student_id,
                date_of_issue=date_of_issue
            )
            session.add(book_receiving)
            session.commit()
            return f"Книга {book_id} выдана студенту {student_id}", 200
        return f"Извините {student_id} книги {book_id} закончились", 200


# эндпоинт для возврата книги в библиотеку
@app.route("/returnbook", methods=["POST"])
def return_the_book():
    student_id = request.form.get('student_id', type=int)
    book_id = request.form.get('book_id', type=int)
    date_of_return = datetime.now()

    with Session(engine) as session:
        book = session.query(ReceivingBook).where(
            (ReceivingBook.book_id == book_id) & (ReceivingBook.student_id == student_id)
        ).one_or_none()
        if book is not None:
            book_in_library = session.query(Book).filter(Book.id == book_id).one_or_none()
            update_book_id = book_in_library.id
            update_book_name = book_in_library.name
            update_book_release_date = book_in_library.release_date
            update_book_count = book_in_library.count + 1
            update_book_author_id = book_in_library.author_id
            session.query(Book).where(Book.id == book_id).update(
                {Book.id: update_book_id,
                 Book.name: update_book_name,
                 Book.release_date: update_book_release_date,
                 Book.count: update_book_count,
                 Book.author_id: update_book_author_id
                 }
            )
            session.commit()

            session.query(ReceivingBook).filter(ReceivingBook.book_id == book_id,
                                                ReceivingBook.student_id == student_id).update(
                {
                    ReceivingBook.book_id: book_id,
                    ReceivingBook.student_id: student_id,
                    ReceivingBook.date_of_issue: ReceivingBook.date_of_issue,
                    ReceivingBook.date_of_return: date_of_return
                }
            )
            session.commit()
            return f"Книга {book_id} возвращена студентом {student_id}", 200
        return f"Извините {student_id} возникла ошибка возврата, вы не должны книгу {book_id}", 404


# Эндпоинт для получения списка студентов которые получают стипендию
@app.route("/scholarships", methods=["GET"])
def scholarships():
    students = Student.get_all_students_scholarships()
    students_scholarships = [student.to_json() for student in students]
    return jsonify(students_scholarships), 200


# Эндпоинт для получения студентов чей средний балл выше переданного
@app.route("/average_point", methods=["POST"])
def average_point():
    point = request.form.get("point", type=float)
    students = Student.get_all_students_by_average_point(average_point=point)
    students_scholarships = [student.to_json() for student in students]
    return jsonify(students_scholarships), 200


# Эндпоинт для получения оставешгося количества книг по автору книг
@app.route("/books_by_author", methods=["POST"])
def books_by_author():
    if request.method == "POST":
        author_id = request.form.get('author_id', type=int)
        count_books_by_author = Book.get_books_by_author(author_id)
        return f"Всего книг этого автора осталось в библиотеке - {count_books_by_author}", 200
    else:
        return "Эта страница не поддерживает данный метод", 303


# Эндпоинт для получения рекомендованных к прочтению книг
@app.route("/recommended_books", methods=["POST"])
def recommended_books_by_author():
    student_id = request.form.get("student_id", type=int)
    if request.method == "POST":
        with Session(engine) as session:
            books_read_by_student = session.scalars(select(
                ReceivingBook.book_id).where(ReceivingBook.student_id == student_id)).all()
            authors = session.scalars(select(
                Book.author_id).where(Book.id.in_(books_read_by_student)))
            recommended_books = session.scalars(select(
                Book.name).where(Book.id.not_in(books_read_by_student)).where(Book.author_id.in_(authors))).all()
            recommended_books = '\n'.join(recommended_books)
        return f"Рекомендованные к прочтению книги: \n{recommended_books}", 200
    else:
        return "Эта страница не поддерживает данный метод", 303


# Эндпонит для получения количества книг взятых в текущем месяце
@app.route("/average_count_books", methods=["GET"])
def count_books_issue_in_during_month():
    count_books = ReceivingBook.average_count_books()
    return f"Количество книг которые студенты брали в этом месяце {count_books}", 200


# Эндпонит для получения самой популярной книги
@app.route("/most_popular_book", methods=["GET"])
def get_the_most_popular_book():
    book_name = ReceivingBook.find_the_most_popular_book()
    return f"Самая популярная книга у студентов с высоким средним баллом - {book_name}", 200


# Топ самых читающих студентов
@app.route("/top_readers")
def top_readers_students():
    students_name = '\n-'.join(ReceivingBook.top_readers())
    return f"Топ самых читающих студентов:\n-{students_name}", 200


@app.route("/load_student_by_csv", methods=["POST"])
def load_student_by_csv():
    if request.method == "POST":
        file = request.files["csv_file"]
        result = Student.inserting_from_file(file)
        if result:
            return f"Данные о студента загружены", 201
        else:
            return f"Во время загрузки проищошла ошибка", 401
    else:
        return "Эта страница не поддерживает данный метод", 303