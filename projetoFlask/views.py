from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Book
from .models import Loan
from .models import find_books_availables
from .models import find_loan
from .models import find_loan_responses
from .models import find_loan_requests
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    books_availables = find_books_availables()
    return render_template("home.html", user=current_user, books=books_availables)


@views.route('/delete-book', methods=['POST'])
def delete_book():  
    book = json.loads(request.data) 
    bookId = book['bookId']
    book = Book.query.get(bookId)
    if book:
        if book.user_id == current_user.id:
            db.session.delete(book)
            db.session.commit()

    return jsonify({})


@views.route('/my-books', methods=['GET'])
def my_books():  
    return render_template("my_books.html", user=current_user)


@views.route('/new-book', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST': 
        author = request.form.get('author')
        title = request.form.get('title')
        release_year = request.form.get('release_year')
        category = request.form.get('category')
        url_image = request.form.get('urlImage')

        if author == '':
            flash('É obrigatório informar o autor do livro!', category='error') 
        if category == '':
            flash('É obrigatório informar a categoria do livro!', category='error') 
        if title == '':
            flash('É obrigatório informar o título do livro!', category='error')
        if url_image == '':
            flash('É obrigatório informar a url da imagem do livro!', category='error')
        if release_year == '':
            flash('É obrigatório informar o ano de lançamento do livro!', category='error') 
        else:
            new_book = Book(author=author, title=title, category=category, release_year=release_year, url_image=url_image, user_id=current_user.id)
            db.session.add(new_book) 
            db.session.commit()
            flash('Livro adicionado com sucesso!', category='success')

    return render_template("new_book.html", user=current_user)


@views.route('/share-book', methods=['POST'])
def share_book():  
    book = json.loads(request.data) 
    bookId = book['bookId']
    userId = book['userId']
    loan = find_loan(userId, current_user.id, bookId)
    print(loan)
    if loan is None:
        new_loan = Loan(lender_id=userId, borrower_id=current_user.id, book_id=bookId, status=1)
        db.session.add(new_loan) 
        db.session.commit()

    return jsonify({})


@views.route('/loan-requests', methods=['GET'])
def my_requests():  
    loansResponse = find_loan_responses(current_user.id)
    loansRequests = find_loan_requests(current_user.id)

    for loanResponse in loansResponse:
        loanResponse.book = Book.query.get(loanResponse.book_id)
    
    for loanRequests in loansRequests:
        loanRequests.book = Book.query.get(loanRequests.book_id)
  
    return render_template("loan_requests.html", loansResponse=loansResponse, loansRequests=loansRequests, user=current_user)


@views.route('/refuse-request', methods=['POST'])
def refuse_request():  
    loan = json.loads(request.data) 
    loanId = loan['loanId']
    loan = Loan.query.get(loanId)

    if loan:
        loan.status = 3
        db.session.add(loan)
        db.session.commit()

    return jsonify({})


@views.route('/accept-request', methods=['POST'])
def accept_request():  
    data = json.loads(request.data) 
    loanId = data['loanId']
    bookId = data['bookId']
    loan = Loan.query.get(loanId)
    book = Book.query.get(bookId)

    if loan:
        loan.status = 2
        db.session.add(loan)
        db.session.commit()
        if book:
            book.disponible = False
            db.session.add(book)
            db.session.commit()

    return jsonify({})