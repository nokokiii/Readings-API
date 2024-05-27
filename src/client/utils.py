"""
This module contains utility functions for the client.
"""

from os import system
from typing import List

from click import getchar, secho, prompt


def clear_screen() -> None:
    """
    This function will clear the screen.
    """
    system("cls")

def user_option() -> int:
    """
    This function will display the main menu and return the user's choice.
    """
    def validate_input(char: str) -> bool:
        """
        This function will validate the user's input.
        """
        return char in {"1", "2", "3"}

    options = ["Add a single book", "Add books", "Exit"]

    print("Choose an option: ")
    for key, value in options.items():
        print(f"[{key}] {value}")

    char = getchar()

    if not validate_input(char):
        clear_screen()
        secho("Invalid option. Please try again.", fg="red")
        return user_option()

    return int(char)


def get_kinds() -> str:
    """
    Get the kinds from the user
    """
    kinds = prompt("Enter the kinds you want to add (format: kind kind)", default="", show_default=False).strip().split()

    return "".join([f"/kinds/{kind}" for kind in kinds]) if kinds else ""


def get_authors() -> List[str]:
    """
    Get the authors from the user
    """
    authors = prompt("Enter the authors you want to add (format: name-lastname name-secondname-lastname)", default="", show_default=False).strip().lower().split()

    return [f'/authors/{author}' for author in authors] if authors else []
