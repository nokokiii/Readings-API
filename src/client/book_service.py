"""
This module contains functions that interact with the Wolne Lektury API and the book service API
"""

from typing import Dict, List

import requests
from click import prompt, secho, progressbar
from thefuzz.fuzz import ratio
from halo import Halo

from config import HOST, WL_API
from utils import clear_screen, get_authors, get_kinds


@Halo(text="Fetching books", spinner="dots")
def fetch_books(url: str) -> List[Dict[str, str]]:
    """
    Fetch books from the Wolne Lektury API and return them as a list of dictionaries
    """
    return requests.get(url).json()


def get_single_book(title: str) -> Dict[str, str]:
    """
    Get a single book from the API that matches the title
    """
    books = fetch_books(f"{WL_API}/books")
    last_similarity = 0
    found_book = None

    for book in books:
        similarity = ratio(title, book['title'])

        if title == book['title'] or last_similarity < similarity > 30:
            last_similarity = similarity
            found_book = book.copy()

    return found_book


def post_book(book: Dict[str, str]) -> None:
    """
    This function will post a book to the API
    """
    response = requests.post(url=f"{HOST}/book", params=book, headers={"Content-Type": "application/json"})

    if response.status_code != 201:
        clear_screen()
        secho(f"Failed to add book:\n {response.text}", fg="red")


def add_books(books: List[Dict[str, str]]) -> None:
    """
    Add a list of books to the database
    """
    with progressbar(books, label="Adding books") as bar:
        for book in bar:
            post_book(book)


def format_books(books: List[Dict[str, str]]) -> str:
    return [{"title": book["title"], "author": book["author"], "kind": book["kind"]} for book in books]


@Halo(text="Fetching authors", spinner="dots")
def get_books(authors: List[str], kinds: str) -> List[Dict[str, str]]:
    """
    Get filtered books from the API
    """
    books = []
    
    if authors:
        for author in authors:
            books = fetch_books(f"{WL_API}{kinds}{author}/books")
            books.extend(format_books(books))
    else:
        books = fetch_books(f"{WL_API}{kinds}/books")
        books = format_books(books)

    return books
