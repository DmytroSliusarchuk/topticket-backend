from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!"

if __name__ == "__main__":
    print("http://127.0.0.1:8080")
    serve(app, host='127.0.0.1', port=8080)
