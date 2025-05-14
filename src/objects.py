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
    def __init__(self, reviewid=0, review=None, isbn=None, isbn13=None,
                 language=None, publication_year=None, publisher=None,
                 num_pages=None):
        self.reviewid = reviewid
        self.review = review
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language = language
        self.publication_year = publication_year
        self.publisher = publisher
        self.num_pages = num_pages