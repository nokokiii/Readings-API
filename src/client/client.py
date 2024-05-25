import os
import sys

import requests
import click
import halo
from thefuzz import fuzz


HOST = "http://localhost:8000"

def user_option() -> int:
    """
    Get user option from the menu.
    """
    print("Choose an option: ")
    print("[1] Add a single book")
    print("[2] Add a list of books")
    print("[3] Exit")

    char = click.getchar()

    if char not in ["1", "2", "3"]:
        os.system("cls")
        click.secho("Invalid option. Please try again.", fg="red")
        return user_option()
    
    return int(char)
    


def get_single_book() -> dict:
    """
    Get a single book from the API that matches the title
    """
    os.system("cls")
    title = click.prompt("Enter the title of the book")

    request_spinner = halo.Halo(text="Fetching book", spinner="dots")
    request_spinner.start()
    response = requests.get("https://wolnelektury.pl/api/books/").json()
    request_spinner.stop()

    last_ratio = 0
    found_book = None

    for book in response:
        ratio = fuzz.ratio(title, book['title'])
        if title == book['title'] or ratio > last_ratio or ratio > 30:
            last_ratio = ratio
            found_book = book.copy()

    return found_book


def add_single_book(book: dict) -> None:
    """
    Add a single book to the database
    """
    response = requests.post(url=f"{HOST}/book", params=book,
                            headers={"Content-Type": "application/json"})

    if response.status_code == 201:
        click.echo(f"{book['title']} added succesfully")
        click.echo("Press any key to go back to the menu")
        if click.getchar():
            os.system("cls")
            return
    else:
        os.system("cls")
        click.secho(f"Failed to add book:\n {response.text}", fg="red")


def get_kinds() -> str:
    """
    Get the kinds from the user
    """
    kinds = click.prompt("Enter the kinds you want to add (format: kind kind)").strip().lower().split()
    return "".join([f"{kind}/" for kind in kinds])


def get_authors() -> list[str]:
    """
    Get the authors from the user
    """
    authors = click.prompt("Enter the authors you want to add (format: name-lastname name-secondname-lastname)").strip().lower().split()
    return [f'authors/{author}' for author in authors]


def add_books(books: list[dict]) -> None:
    with click.progressbar(books, label="Adding books") as bar:
        for book in books:
            add_single_book(book)


def get_books() -> list[dict]:
    """
    Get filtered books from the API
    """
    os.system("cls")
    kinds = get_kinds()
    authors = get_authors()
    books = []

    spinner = halo.Halo(text="Fetching books", spinner="dots")
    spinner.start()

    for author in authors:
        response = requests.get(f"https://wolnelektury.pl/api/{kinds}/{author}/books")

        if response.status_code != 200:
            continue

        books.extend([{"title": book["title"], "author": book["author"], "kind": book["kind"]} for book in response.json()])
    
    spinner.stop()

    return books

def cli() -> None:
    """
    Client logic
    """
    while True:
        num = user_option()

        match num:
            case 1:
                if book := get_single_book():
                    add_single_book(book)
                else: 
                    click.echo("Book not found")
            case 2:
                if books := get_books():
                    add_books(books)
                else:
                    click.echo("Books not found")
            case 3:
                click.secho("Exiting", fg="green")
                sys.exit(0)


def main() -> None:
    """
    Main loop
    """
    while True:
        cli()
        os.system("cls")


if __name__ == "__main__":
    main()
