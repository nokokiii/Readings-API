from flask import Flask, Response, jsonify, request
from logic import getLogic


app = Flask(__name__)

logic = getLogic()


@app.route('/')
def ping():
    return logic.ping()

@app.post('/book')
def add_book():
    data = request.get_json()
    status_msg, res = logic.add_book(title=data['title'], author=data['author'], kind=data['kind'])
    
    if status_msg == "Error":
        status = 500
    elif status_msg == "Created":
        status = 201

    return Response(status=status, response=jsonify({"msg": res}))

 
@app.get('/book')
def get_book():
    title = request.params.get('title')

    status_msg, res = logic.get_book(title=title)

    # Put this into function in somewhere
    if status_msg == "Error":
        status = 500
    elif status_msg == "Not Found":
        status = 404
    elif status_msg == "OK":
        status = 200

    return Response(status=status, response=jsonify(res))


@app.get('/books')
def get_books():
    authors = request.params.get('authors')
    kinds = request.params.get('kinds')
    # TODO: Add more filters

    status_msg, res = logic.get_books(authors=authors, kinds=kinds)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
