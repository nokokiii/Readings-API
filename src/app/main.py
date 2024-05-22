from flask import Flask, Response, jsonify, request

from src.app.logic import Logic
from src.app.utils import get_status_code

app = Flask(__name__)
logic = Logic()

@app.route('/')
def ping():
    return "Welcome to the WLapi"



@app.post('/book')
def add_book():
    data = request.get_json()
    status_msg, res = logic.add_book(title=data['title'], author=data['author'], kind=data['kind'])

    return Response(status=get_status_code(status_msg=status_msg), response=jsonify(res))


@app.get('/book')
def get_book():
    title = request.params.get('title')
    status_msg, res = logic.get_book(title=title)

    return Response(status=get_status_code(status_msg=status_msg), response=jsonify(res))


@app.get('/books')
def get_books():
    status_msg, res = logic.get_books(params=request.params)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
