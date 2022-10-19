from backend.app import app

@app.route("/")
def index():
    return "Hello world!"

@app.route("/api/v1/hello-world-<int:num>")
def hello_world(num):
    return f"<h1>Hello World {num}</h1>"