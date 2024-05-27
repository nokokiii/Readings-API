"""
This is the main module for the client
"""

from click import prompt, secho, getchar, echo

from book_service import *
from utils import *


def handle_add_book() -> None:  
    """
    This function will handle opttion 1 in the main menu
    """
    title = prompt("Enter the title of the book")

    if book := get_single_book(title):
        post_book(book)
        
        if getchar():
            echo("Press any key to go back to the menu")
    else: 
        echo("Book not found")


def handle_add_books() -> None:
    """
    This function will handle option 2 in the main menu
    """
    kinds = get_kinds()
    authors = get_authors()

    if books := fetch_books(authors, kinds):
        add_books(books)
    else:
        echo("Books not found")
        return

    if getchar():
        echo("Press any key to go back to the menu")


def main() -> None:
    """
    Main function to run the client
    """
    num = user_option()

    if num == 1:
        clear_screen()
        handle_add_book()
    elif num == 2:
        clear_screen()
        handle_add_books()
    elif num == 3:
        secho("Exiting", fg="green")
        exit(0)


if __name__ == "__main__":
    while True:
        main()
        clear_screen()
