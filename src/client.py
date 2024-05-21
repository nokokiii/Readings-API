import requests
from thefuzz import fuzz
import logging


def fetch_data(title: str) -> None:
    r = requests.get("https://wolnelektury.pl/api/books/").json()
    last_ratio = 0
    for book in r:
        ratio = fuzz.ratio(title, book['title'])
        if title == book['title'] or ratio > last_ratio:
            last_ratio = ratio
            found_book = {
                "title": book['title'],
                "author": book['author'],
                "kind": book['kind'],
            }

    response = requests.post(url="http://localhost:5001/books/add_book", json=found_book,
                             headers={"Content-Type": "application/json"})

    if response.status_code == 201:
        logging.log("Book added succesfully")
    else:
        logging.error(f"Failed to add book:\n {response.text}")


print(fetch_data("Pan Tadeusz, czyli ostatni zajazd na Litwie"))
