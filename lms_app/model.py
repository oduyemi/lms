from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from lms_app import db


class Book(db.Model):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    ISBN = Column(String(255), unique=True, nullable=False)
    publicationYear = Column(Integer, nullable=False)

    def __init__(self, title, author, ISBN, publicationYear):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.publicationYear = publicationYear


class PhysicalBook(db.Model):
    __tablename__ = "physical_books"
    book_id = db.Column(Integer, ForeignKey('books.id'), primary_key=True)
    shelfLocation = Column(String(255), nullable=False)
    isAvailable = Column(Boolean, default=True, nullable=False)

    book = relationship('Book', backref='physical_book', uselist=False)

    def borrow(self):
        if self.isAvailable:
            self.isAvailable = False
            return True
        else:
            return False

    def returnBook(self):
        if not self.isAvailable:
            self.isAvailable = True
            return True
        else:
            return False


class DigitalBook(db.Model):
    __tablename__ = "digital_books"

    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    fileSize = Column(Float, nullable=False)
    downloadLink = Column(String(255), nullable=False)

    def getBookInfo(self):
        return f"{self.title} by {self.author}, ISBN: {self.ISBN}, File Size: {self.fileSize} MB"

class Member(db.Model):
    __tablename__ = "members"

    memberID = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    
    def __init__(self, memberID, name):
        self.memberID = memberID
        self.name = name
        self.borrowedBooks = []

    def borrowBook(self, book):
        if isinstance(book, PhysicalBook) and book.isAvailable:
            book.isAvailable = False
            self.borrowedBooks.append(book)
            return True
        else:
            return False

    def returnBook(self, book):
        if book in self.borrowedBooks:
            self.borrowedBooks.remove(book)
            book.isAvailable = True
            return True
        else:
            return False

class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def addBook(self, book):
        self.books.append(book)

    def removeBook(self, book):
        if book in self.books:
            self.books.remove(book)

    def registerMember(self, member):
        self.members.append(member)

    def getAvailableBooks(self):
        available_books = []
        for book in self.books:
            if isinstance(book, PhysicalBook) and book.isAvailable:
                available_books.append(book)
        return available_books

class Books(db.Model):
    books_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    books_title = db.Column(db.String(255))
    books_author = db.Column(db.String(255))
    books_isbn = db.Column(db.String(13), unique = True)
    books_year = db.Column(db.Integer())
    books_type = db.Column(db.Enum('Type1', 'Type2', 'Type3')) 
    books_isAvailable = db.Column(db.Boolean())
    books_filesize = db.Column(db.Float())
    books_downloadLink = db.Column(db.String(255))

class Members(db.Model):
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    member_id = db.Column(db.String(50), unique = True)
    member_name = db.Column(db.String(255))


class BorrowedBooks(db.Model):
    __tablename__ = "borrowed_books"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.books_id'))
    member_id = db.Column(db.String(50), db.ForeignKey('members.member_id')) 
    borrow_date = db.Column(db.DateTime())
    return_date = db.Column(db.DateTime(), default=None)




# - TESTING -

book = Book(title="Sample Book", author="Sample Author", ISBN="1234567890", publicationYear=2022)

physical_book = PhysicalBook(shelfLocation="A1")

member = Member(memberID="12345", name="John Doe")

library = Library()
library.addBook(book)

library.registerMember(member)

member.borrowBook(physical_book)

print(physical_book.isAvailable) #prints False

member.returnBook(physical_book)

print(physical_book.isAvailable)  # Prints True
