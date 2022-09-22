from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!"

@app.route("/api/v1/hello-world-<int:num>")
def hello_world(num):
    return f"<h1>Hello World {num}</h1>"


if __name__ == "__main__":
    print("http://127.0.0.1:8080")
    serve(app, host='127.0.0.1', port=8080)
