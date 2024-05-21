import requests

def collect_authors():
    r = requests.get("https://wolnelektury.pl/api/authors/").json()
    authors = [author["name"] for author in r]
    return authors

print(collect_authors())

