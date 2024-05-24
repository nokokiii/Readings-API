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
                    response = requests.post(url="http://localhost:5001/books/add_book", json=found_book,
                                            headers={"Content-Type": "application/json"})

                    if response.status_code == 200:
                        print(f"{found_book['title']} added succesfully")
                    else:
                        print(f"Failed to add book:\n {response.text}")
            case 2:
                categories = [f"kinds/{cat}" for cat in (
                    input("Podaj kategorie które/ą chcesz dodać: (format: kategoria kategoria)\n")).strip().lower().split()]
                author = [
                    f"authors/{input("Podaj autora którego chcesz dodać: (format: imie nazwisko)\n").strip().lower().replace(' ', '-')}"]

                response = requests.get(f"https://wolnelektury.pl/api/{'/'.join(categories + author)}/books")
                if response.status_code != 200:
                    print(f"Error: {response.status_code}, {response.reason}")
                    break
                list_of_books = [{"title": book["title"], "author": book["author"], "kind": book["kind"]} for book in response.json()]
                for book in list_of_books:
                    response = requests.post(url="http://localhost:5001/books/add_book", json=book,
                                            headers={"Content-Type": "application/json"})

                    if response.status_code == 200:
                        print(f"{book['title']} added succesfully")
                    else:
                        print(f"Failed to add book:\n {response.text}")
            case 3:
                print("Thanks for using our client.")
                break


fetch_data()
