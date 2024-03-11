from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(150))
    title = db.Column(db.String(150))
    release_year = db.Column(db.Integer)
    category = db.Column(db.String(150))
    disponible = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url_image = db.Column(db.String)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    books = db.relationship('Book')

def find_books_availables() -> list:
    return Book.query.filter_by(disponible=True).all()

def find_loan(lender_id, borrower_id, book_id) -> Loan:
    return Loan.query.filter_by(lender_id=lender_id, borrower_id=borrower_id,book_id=book_id ).first()

def find_loan_requests(lender_id) -> list:
    return Loan.query.filter_by(lender_id=lender_id, status=1).all()

def find_loan_responses(borrower_id) -> list:
    return Loan.query.filter_by(borrower_id=borrower_id).all()