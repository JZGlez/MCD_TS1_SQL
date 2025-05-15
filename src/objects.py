## Entities

class Author:
    def __init__(self, authorid=0, author_name=None):
        self.authorid = authorid
        self.author_name = author_name

class Book:
    def __init__(self, bookid=0, title=None, isbn=None, isbn13=None,
                 language=None, publication_year=None, publisher=None,
                 num_pages=None):
        self.bookid = bookid
        self.title = title
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language = language
        self.publication_year = publication_year
        self.publisher = publisher
        self.num_pages = num_pages

class Genre:
    def __init__(self, genreId = 0, genre_name = None):
        self.genreId = genreId
        self.genre_name = genre_name

class BookAuthor:
    def __init__(self, book_id = None, author_id = None):
        self.bookId = book_id
        self.authorId = author_id

class BookGenre:
    def __init__(self, book_id = None, genre_id = None):
        self.bookId = book_id
        self.genreId = genre_id
class User:
    def __init__(self, userid=0, user=None):
        self.userid = userid
        self.user = user

class Review:
    def __init__(self, userid=None, bookid=None, reviewid=None, rating=None, review=None,
                 review_date=None, num_votes=None, num_comments=None):
        self.userid = userid
        self.bookid = bookid
        self.reviewid = reviewid
        self.rating = rating
        self.review = review
        self.review_date = review_date
        self.num_votes = num_votes
        self.num_comments = num_comments
