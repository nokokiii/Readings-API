import requests
import controllers as controllers


def fetch_data():
    r = requests.get("https://wolnelektury.pl/api/books/").json()

    data = r

    response = requests.post(url="http://127.0.0.1:5001/add_book", json=data,
                             headers={"Content-Type": "application/json"})

    if response.status_code == 201:
        print("Book added successfully!")
    else:
        print("Failed to add book.")
        print(response.text)
        
    return data
