import requests
from thefuzz import fuzz


def fetch_data(title: str):

    r = requests.get("https://wolnelektury.pl/api/books/").json()
    books = r
    last_ratio = 0
    for book in books:
        ratio = fuzz.ratio(title, book['title'])
        if title == book['title'] or ratio > last_ratio:
            last_ratio = ratio
            found_book = {
                "title": book['title'],
                "author": book['author'],
                "epoch": book['epoch'],
                "genre": book['genre'],
                "kind": book['kind'],
            }

    response = requests.post(url="http://localhost:5001/books/add_book", json=r,
                             headers={"Content-Type": "application/json"})

    if response.status_code == 201:
        print("Book added successfully!")
    else:
        print("Failed to add book.")
        print(response.text)

    return found_book


print(fetch_data("Pantera"))