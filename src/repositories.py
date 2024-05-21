def get_book_data(book: dict[str, str]) -> tuple[str]:
    
    title = book["title"]
    author = book["author"]
    kind = book["kind"]

    return title,author,kind




# print(type(add_book_rep({'title': 'Tadeuszek', 'author': 'Stanisław Jachowicz', 'kind': 'Epika'})))