import re

import requests
from thefuzz import fuzz

def fetch_data() -> None:
    while True:
        print("1. Dodaj pojedyńczą książkę")
        print("2. Dodaj liste książek(dla danego autora bądź danej kategorii)")
        print("3. Wyjdź")
        num = int(input("Wybierz liczbę z listy powyżej:"))

        match num:
            case 1:
                title = str(input("Podaj tytuł książki:"))
                r = requests.get("https://wolnelektury.pl/api/books/").json()
                last_ratio = 0
                found_book = None
                for book in r:
                    ratio = fuzz.ratio(title, book['title'])
                    if title == book['title'] or ratio > last_ratio:
                        last_ratio = ratio
                        found_book = {
                            "title": book['title'],
                            "author": book['author'],
                            "kind": book['kind'],
                        }

                if found_book:
                    print(f"Book {title} added")
                    # response = requests.post(url="http://localhost:5001/books/add_book", json=found_book,
                    #                         headers={"Content-Type": "application/json"})

                    # if response.status_code == 200:
                    #     print("Book added succesfully")
                    # else:
                    #     print(f"Failed to add book:\n {response.text}")
            case 2:
                categories = str(input("Podaj kategorie które/ą chcesz dodać: (format: kategoria kategoria)\n"))
                categories = categories.split()
                categories = [f"/kinds/{cat}" for cat in categories]
                print(f"Wybrane kategorie: {categories}")

                authors = str(input("Podaj autora lub autorów których chcesz dodać: (format: imie nazwisko imie nazwisko)\n"))
                authors = re.findall(r'\b\w+\s\w+\b', authors)
                authors = [f"/authors/{name.lower().replace(' ', '-')}" for name in authors]
                print(f"Wybrani autorzy: {authors}")
                r = requests.get("https://wolnelektury.pl/api/books/").json()
            case 3:
                print("Thanks for using our client.")
                break 



                

fetch_data()