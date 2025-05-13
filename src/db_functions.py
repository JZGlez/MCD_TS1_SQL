# DATABASE LAYER

import pandas as pd
import sqlite3 as sql
from contextlib import closing
from objects import Author, Book, Genre, BookAuthor, BookGenre

# Variable global que representa el string de conexion
conn = None

# Vamos a necesitar varios métodos
# Autores

def connect():
    global conn
    if not conn: # if conn has not been set then set
        conn =sql.connect("../db/goodreads-db.sqlite")
        conn.row_factory = sql.Row # returns a dict instead of a tuple
        
def close():
    if conn:
        conn.close()
    # we call from de ui moduls when the user terminate the application

### Author functions

def add_author(author): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO Authors (AuthorName)
    VALUES (?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (author.author_name,)) # representa al objeto employee
        conn.commit()

### Book functions

def add_book(book): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO Books (BookID, Title, ISBN, ISBN13, Language, PublicationYear, Publisher, NumPages)
    VALUES (?,?,?,?,?,?,?,?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book.bookid, book.title, book.isbn, book.isbn13,
                                   book.language, book.publication_year, book.publisher,
                                   book.num_pages)) # representa al objeto employee
        conn.commit()

# Agregar género
def add_genre(genre: Genre): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO Genres (GenreName)
    VALUES (?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (genre.genre_name,))
        conn.commit()

# Agregar BookAuthor
def add_bookAuthor(bookAuthor: BookAuthor):
    sql_query = '''INSERT OR IGNORE INTO BookAuthors (BookID, AuthorID)
    VALUES (?,?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (bookAuthor.bookId, bookAuthor.authorId))
        conn.commit()

# Agregar BookGenre
def add_bookGenre(bookGenre: BookGenre):
    sql_query = '''INSERT OR IGNORE INTO BookGenres (BookID, GenreID)
    VALUES (?,?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (bookGenre.bookId, bookGenre.genreId))
        conn.commit()

def get_authors_dictionary():
    sql_query = '''SELECT * FROM Authors'''
    df_authors = pd.read_sql_query(sql_query, conn)
    authors_dict = {}
    for index, row in df_authors.iterrows():
        authors_dict[row["AuthorName"]] = int(row["AuthorID"])
    return authors_dict

def get_genres_dictionary():
    sql_query = '''SELECT * FROM Genres'''
    df_genres = pd.read_sql_query(sql_query, conn)
    genres_dict = {}
    for index, row in df_genres.iterrows():
        genres_dict[row["GenreName"]] = int(row["GenreID"])
    return genres_dict
