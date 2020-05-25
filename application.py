import os

import json
import requests 

from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy  import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

from login import login_required

app = Flask(__name__)

app.jinja_env.filters['zip'] = zip

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config['JSON_SORT_KEYS'] = False

app.secret_key = 'key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    session.clear()
    username = request.form.get("username")

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("login.html", alert=1)
        
        elif not request.form.get("password"):
            return render_template("login.html", alert=2)
        
        result = db.execute("""SELECT * FROM "user" WHERE username = (:username)""", {"username": username}).fetchone()

        if result == None or not check_password_hash(result[3], request.form.get("password")):
            return render_template("login.html", alert=3)
        
        session["user_id"] = result[0]
        session["username"] = result[1]

        return redirect("/dashboard")

    else:
        return render_template("login.html", alert=0)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    session.clear()
    
    if request.method == 'POST':
        if not request.form.get("username"):
            return render_template("signup.html", alert=2)
        
        if not request.form.get("email"):
            return render_template("signup.html", alert=3)
        
        user = db.execute("""SELECT username FROM "user" WHERE username = (:username)""", {"username": request.form.get("username")}).fetchone()
        email_id = db.execute(""" SELECT email FROM "user" WHERE email = (:email)""", {"email": request.form.get("email")}).fetchone()

        if user:
            return render_template("signup.html", alert=4)
        
        if email_id:
            return render_template("signup.html", alert=5) 
        
        elif not request.form.get("password"):
            return render_template("signup.html", alert=6)

        elif not request.form.get("confirmation"):
            return render_template("signup.html", alert=7)
        
        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("signup.html", alert=8)

        hashedPassword = generate_password_hash(request.form.get("password"), method = 'sha256')

        db.execute(""" INSERT INTO "user" (username, email, password) VALUES (:username, :email, :password)""", {"username": request.form.get("username"), "email": request.form.get("email") , "password": hashedPassword}) 

        db.commit()

        return render_template("signup.html", alert=1)
    
    else:
        return render_template("signup.html", alert=0)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route('/dashboard')
@login_required
def dashboard():
    name = session["username"]
    return render_template('dashboard.html', name = name)

@app.route("/dashboard/search", methods = ['GET'])
@login_required
def dashboardSearch():    
    if not request.args.get("book"):
        return render_template("searchresults.html", alert=1, name=session["username"], find=request.args.get("book"))
    
    book = ("%" + request.args.get("book") + "%").title()

    results = db.execute("""SELECT * FROM books WHERE "ISBN" LIKE (:book) OR "Title" LIKE (:book) OR "Author" LIKE (:book) OR "Year" LIKE (:book)""", {"book" : book})
    
    if results.rowcount == 0:
        return render_template("searchresults.html", alert=1, name=session["username"], find=request.args.get("book"))

    books = results.fetchall()
    count = len(books)
    return render_template("searchresults.html", alert=0, books = books, count = count, name=session["username"], find=request.args.get("book"))


@app.route("/dashboard/<book_isbn>", methods = ['GET', 'POST'])
def details(book_isbn):
    bookinfo = db.execute("""SELECT * FROM "books" WHERE books."ISBN" = (:isbn)""", {"isbn": book_isbn}).fetchone()
    
    reviews = db.execute("""SELECT "user".username, "review".content, review.rating, 
                            to_char(review.created, 'DD MONTH YYYY, HH24:MI:SS') as created
                            FROM "review"
                            JOIN "books" ON "review".book_id = "books"."ID"
                            JOIN "user" ON "review"."author_id" = "user"."id" 
                            WHERE books."ISBN" = (:isbn)""", {"isbn": book_isbn}).fetchall()

    goodreadsData = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "NJ628zsNMZHnxrzHV3n4A", "isbns": book_isbn})
    goodreadsData = goodreadsData.json()
    goodreadsAvg = goodreadsData['books'][0]['average_rating']
    goodreadsNo = int(goodreadsData['books'][0]['work_ratings_count'])
    goodreadsId = goodreadsData['books'][0]['id']

    countreviews = db.execute("""SELECT COUNT(*) FROM "review"
                                 JOIN "books" ON books."ID" = review.book_id
                                 WHERE books."ISBN" = (:isbn)""", {"isbn": book_isbn}).fetchone()

    imglink = "http://covers.openlibrary.org/b/isbn/" + str(book_isbn) + "-M.jpg"

    return render_template("bookinfo.html", name=session["username"], count=countreviews[0], bookinfo = bookinfo, reviews = reviews, goodreadsAvg = goodreadsAvg, goodreadsNo = goodreadsNo, goodreadsId = goodreadsId, imglink = imglink)

@app.route("/dashboard/<isbn>/review", methods = ['GET', 'POST'])   
@login_required
def review(isbn):
    bookname = db.execute("""SELECT "Title" FROM books WHERE "ISBN" = (:isbn)""", {"isbn": isbn}).fetchone()

    if request.method == 'POST':
        current_user = session["user_id"]

        rating = int(request.form.get("rating"))
        content = request.form.get("content")

        bookid = db.execute("""SELECT "ID" FROM books WHERE "ISBN" = (:isbn)""", {"isbn": isbn}).fetchone()[0]

        check = db.execute(""" SELECT * FROM "review" WHERE "author_id" = (:authorid) AND "book_id" = (:bookid)""", {"authorid": current_user, "bookid": bookid})

        if check.rowcount == 1:
            return render_template("review.html", isbn=isbn, bookname=bookname, alert=0, name=session["username"])
        
        db.execute("""INSERT INTO "review" (author_id, rating, content, book_id) VALUES (:authorid, :rating, :content, :bookid)""", {"authorid": current_user, "rating": rating, "content": content, "bookid": bookid})
        
        db.commit()
        
        return render_template("review.html", bookname=bookname, alert=2, isbn=isbn, name=session["username"])

    return render_template("review.html", bookname=bookname, alert=1, isbn=isbn, name=session["username"])

@app.route("/api/<book_isbn>", methods = ['GET'])
def apiAccess(book_isbn):
    result = db.execute("""SELECT * FROM "books" WHERE "ISBN" = (:book_isbn) """, {"book_isbn": book_isbn}).fetchone()

    if result is None:    
        return "<head><title>Error 404</title></head><h1>404 : Not Found</h1>", 404

    goodreadsData = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "NJ628zsNMZHnxrzHV3n4A", "isbns": book_isbn})
    
    goodreadsData = goodreadsData.json()
    goodreadsAvg = float(goodreadsData['books'][0]['average_rating'])
    goodreadsNo = int(goodreadsData['books'][0]['work_ratings_count'])

    return jsonify ({
            "title": result.Title,
            "author": result.Author,
            "year": int(result.Year),
            "isbn": result.ISBN,
            "review_count": goodreadsNo,
            "average_score": float("{:.1f}".format(goodreadsAvg))
    })




