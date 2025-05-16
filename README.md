# MCD_TS1_SQL
# Sistema de Gestión de Libros con SQLite
Repositorio para proyecto final de Tópicos Selectos de Grandes Bases de Datos I

Este software fue desarrollado como proyecto final del curso "Tópicos Selectos de Grandes Bases de Datos I", con el objetivo de crear un sistema que permita almacenar, consultar y modificar información relacionada con libros, sus autores, géneros, usuarios y calificaciones. Utiliza SQLite como gestor de base de datos y Python como lenguaje de programación principal para el manejo de datos, interacción con la base de datos y la construcción del sistema.

# Como ejecutar el proyecto:
- Requisitos previos:
 Python >= 3.7
Clonar el repositorio:
```git clone https://github.com/JZGlez/MCD_TS1_SQL.git```
```cd MCD_TS1_SQ```
Instalar las dependencias indicadas en requirements.txt
  ```pip install -r requirements.txt```

- Instalar la Base de Datos
Ejecutar create_db.py para crear las tablas (si aún no han sido creadas):
  ```python src/create_db.py```
Ejecutar db_fill.py para poblar la base de datos con datos CSV (si aún no han sido llenadas):
  ```python src/db_fill.py```

- Ejecutar el programa principal
  ```python main.py```

# Estructura de archivos 
MCD_TS1_SQL
│
├── main.py                    # Archivo principal
├── README.md                  # Documentación del proyecto
├── requirements.txt           # Lista de dependencias de Python
│
├── /src                       # Código fuente dividido en módulos
│   ├── create_db.py           # Creación de la base de datos y tablas
│   ├── db_fill.py             # Relleno de las tablas con datos CSV
│   ├── db_functions.py        # Funciones de conexión y manipulación de la BD
│   ├── objects.py             # Definición de las clases de objetos
│   ├── utils.py               # Funciones utilitarias
│
├── /data                      # Archivos de datos en CSV
│   ├── Goodreads_books_with_genres.csv
│   ├── Goodreads_reviews_formated.csv
│   ├── User_rating_0_to_11000.csv
│
├── /notebooks                # Notebooks del proceso
│   ├── Goodreads-db-exploration.ipynb
│   ├── reviews_ETL.ipynb
│   ├── tableFill.ipynb
│
├── /db
│   └── goodreads-db.sqlite    # Base de datos SQLite creada

# Funciones principales por módulo
create_db.py
  create_connection(db_file): Establece conexión a la base de datos.
  create_table(con, create_table_sql): Crea una tabla si no existe.

db_fill.py
  Realiza el preprocesamiento de los datos y pobla las tablas desde archivos CSV.

db_functions.py
  connect(), close(): Manejo de conexión.
  add_author(author), add_book(book), add_genre(genre), add_user(user), add_review(review)
  add_bookGenre(bookGenre), add_bookAuthor(bookAuthor)
  get_authors_dictionary(): Consulta auxiliar.

utils.py
  remove_extra_spaces(text)
  get_author_id(df_authors, author_name)
  get_genre_id(df_genres, genre_name)


# La base de datos contiene 7 tablas:

-Authors: 9236 registros, contiene nombres e ID de autores.
-Books: 11125 registros, contiene datos como título, idioma, páginas, ISBN, etc.
-Genres: 887 registros, lista de géneros literarios.
-Users: 9104 registros, nombres e identificadores únicos de usuarios.
-Ratings: 50000 registros, contiene valoraciones y comentarios de libros hechos por usuarios.
-BooksGenres: 94774 registros, relación muchos a muchos entre libros y géneros.
-BooksAuthors: 19209 registros, relación muchos a muchos entre libros y autores.