# WLapi

This is a simple api that uses fastapi and sqlalchemy to create an API that gives users more features then [Wolne Lektury](https://wolnelektury.pl/).

Also we created a client that users can use to insert books into the database.

## How to run

### Dependencies and environment variables

To install all the dependencies run this command `pip install -r requirements.txt`

In the root directory create a file called `.env` and add the following variables:

```env
connection_string = "postgresql+psycopg2://docker:docker@localhost:5432/wldatabase"
```

### Database

Before you run the app you need to create a database using the following command `docker-compose -f .\docker-compose.yaml up`

### API

To run the api run this command `uvicorn src.app.main:app`

### Client

To run the client run this command `python src/client.py`


## Documentation

### API

The API has the following endpoints:

- `/books/{authors}/{kinds}` - GET - Returns a list of books by authors and kinds. If no authors or kinds are provided it returns all the books.

- `/books/{id}` - GET - Returns a book by id

- `/books` - POST - Creates a book

### Client

After you run the client you will be see main menu with the following options:
- `1` - Add a book
- `2` - Add a list of books

If you choose option `1` you will be asked to provide the following information:
- Title

If you choose option `2` you will be asked to provide the following information:
- Kinds in this format `kind1 kind2 kind3`
- Authors in this format `authorname-authorlastname1 authorname-authorsecondname-authorlastname2`

After you provide the information the client will make a request to the API to add the book or books.

## Authors

- [nokokiii](https://github.com/nokokiii)
- [kubat1611](https://github.com/kubat1611)
- [Bart3kD](https://github.com/Bart3kD)