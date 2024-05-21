from flask import Flask, Response, jsonify, request
import json

app = Flask(__name__)




@app.route('/')
def ping():
    return "jebac baltiona"


@app.post('/add_book')
def add_book():
    return 'asd'        
    





    




if __name__ == "__main__":
    app.run(port=5001, debug=True)

