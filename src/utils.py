# Utils (miscellaneous)

# functions
def remove_extra_spaces(text) -> str:
    return " ".join(text.split())

def get_author_id(df_authors, author_name):
    authors = df_authors.query(f'AuthorName == "{author_name}"')
    if(len(authors) == 0):
        return None
    author_id = authors.iloc[0].AuthorID
    return int(author_id)

def get_genre_id(df_genres, genre_name):
    genres = df_genres.query(f'GenreName == "{genre_name}"')
    if(len(genres) == 0):
        return None
    genre_id = genres.iloc[0].GenreID
    return int(genre_id)
