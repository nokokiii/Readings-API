import os
import sys
from typing import List, Dict

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
    


def get_single_book() -> Dict[str, str]:
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


def add_single_book(book: Dict[str, str]) -> None:
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
    kinds = click.prompt("Enter the kinds you want to add (format: kind kind)", default="", show_default=False).strip().split()

    return "".join([f"/kinds/{kind}" for kind in kinds]) if kinds else ""


def get_authors() -> List[str]:
    """
    Get the authors from the user
    """
    authors = click.prompt("Enter the authors you want to add (format: name-lastname name-secondname-lastname)", default="", show_default=False).strip().lower().split()

    return [f'/authors/{author}' for author in authors] if authors else []


def add_books(books: List[Dict[str, str]]) -> None:
    """
    Add a list of books to the database
    """
    for book in books:
        add_single_book(book)


def get_books() -> List[Dict[str, str]]:
    """
    Get filtered books from the API
    """
    os.system("cls")
    kinds = get_kinds()
    authors = get_authors()
    books = []

    spinner = halo.Halo(text="Fetching books", spinner="dots")
    spinner.start()
    
    if authors:
        for author in authors:
            print(f"https://wolnelektury.pl/api{kinds}{author}/books")
            response = requests.get(f"https://wolnelektury.pl/api{kinds}{author}/books")

            if response.status_code != 200:
                continue

            books.extend([{"title": book["title"], "author": book["author"], "kind": book["kind"]} for book in response.json()])
    else:
        print(f"https://wolnelektury.pl/api{kinds}/books")
        response = requests.get(f"https://wolnelektury.pl/api{kinds}/books")

        if response.status_code == 200:
            books = [{"title": book["title"], "author": book["author"], "kind": book["kind"]} for book in response.json()]

    spinner.stop()

    return books

def main() -> None:
    """
    Main function to run the program
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


if __name__ == "__main__":
    while True:
        main()
        os.system("cls")
