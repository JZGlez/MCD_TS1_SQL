import pandas as pd
import numpy as np
from objects import Author, Book, Genre, BookAuthor, BookGenre, User, Review
import db_functions
from utils import remove_extra_spaces, get_genre_id, get_author_id
import os

## Data import
df = pd.read_csv("../data/Goodreads_books_with_genres.csv")
df = df.drop(axis=0, index=8180) # parche
df = df.drop(axis=0, index=11098) # parche
df["Author"] = df["Author"].str.replace('"',"'")
df['publication_date'] = pd.to_datetime(df['publication_date'], format='%m/%d/%Y')

df_reviews = pd.read_csv('../data/goodreads_reviews_formated.csv')

# abrir conexion
db_functions.connect()

# Fill authors table
series_authors = df['Author'] # column of interest
list_authors = series_authors.str.split(pat="/").values.tolist() # convert to list (separated)
flat_list_authors = [x2 for x1 in list_authors for x2 in x1] # list flatten
array_authors_unique = pd.Series(flat_list_authors).unique()

for element in array_authors_unique:
    element = remove_extra_spaces(element)
    author = Author(author_name=element)
    db_functions.add_author(author=author)
print("Authors table filled!")

# Fill books table

book_list = list(zip(df['Book Id'],df['Title'],df['isbn'],
                       df['isbn13'],df['language_code'],df['publication_date'].dt.year,
                       df['publisher'], df['num_pages']))

for element in book_list:
    book = Book(bookid=element[0],
                title=element[1],
                isbn=element[2],
                isbn13=element[3],
                language=element[4],
                publication_year=element[5],
                publisher=element[6],
                num_pages=element[7])
    db_functions.add_book(book=book)
print("Book table filled!")

# Fill genres table

series_genres = df['genres'].dropna()
list_genres = series_genres.str.split(pat=";").values.tolist()
# Flatten genres
flat_list_genres = [x2 for x1 in list_genres for x2 in x1]
# Capitalizar todos
flat_list_genres_cap = [x.capitalize().strip() for x in flat_list_genres]
array_genres_unique = pd.Series(flat_list_genres_cap).unique()

for genre_name in array_genres_unique:
    genre = Genre(genre_name=genre_name)
    db_functions.add_genre(genre)
print("Genres table filled!")

# Fill BookAuthors table

authors_dict = db_functions.get_authors_dictionary()
for index, row in df.iterrows():
    book_id = row["Book Id"]
    authors = row['Author']
    authors_array = authors.split("/")
    # Por cada autor, obtener su id
    for author in authors_array:
        # Quitar espacios extra
        author = " ".join(author.split())
        author_id = authors_dict.get(author)
        if(author_id != None):
            # Crear registro en la tabla BookAuthors
            bookAuthor = BookAuthor(book_id, author_id)
            db_functions.add_bookAuthor(bookAuthor)
        else:
            print(f"Author {author} not found!")
print("BookAuthors table filled!")

# Fill BookGenres table
genres_dictionary = db_functions.get_genres_dictionary()
for index, row in df.iterrows():
    book_id = row["Book Id"]
    genres = row['genres']
    if(pd.isna(genres)):
        continue
    genres_array = genres.split(";")
    genres_array = [x.capitalize().strip() for x in genres_array]
    # Por cada autor, obtener su id
    for genre in genres_array:
        genre_id = genres_dictionary.get(genre)
        if(genre_id != None):
            # Crear registro en la tabla BookAuthors
            bookGenre = BookGenre(book_id, genre_id)
            db_functions.add_bookGenre(bookGenre)
        else:
            print(f"Genre {genre} not found!")        

print("BookGenres table filled!")

# Fill users table
users_list = list(zip(df_reviews['user_id'],df_reviews['user']))

for element in users_list:
    user = User(userid=element[0],
                user=element[1])
    db_functions.add_user(user=user)
print("User table filled!")

# Fill reviews table

review_list = list(zip(df_reviews['user_id'], df_reviews['book_id'], df_reviews['review_id'],
                        df_reviews['rating'], df_reviews['review_text'], df_reviews['date_added'],
                        df_reviews['n_votes'], df_reviews['n_comments']))

for element in review_list:
    review = Review(userid=element[0],
                    bookid=element[1],
                    reviewid=element[2],
                    rating=element[3],
                    review=element[4],
                    review_date=element[5],
                    num_votes=element[6],
                    num_comments=element[7])
    db_functions.add_review(review=review)
print("Review table filled!")

# Close connection to database
db_functions.close()
