from backend.app import app
from backend.models.user import User


@app.route("/")
def index():
    return "Hello world!"


@app.route("/api/v1/hello-world-<int:num>")
def hello_world(num):
    return f"<h1>Hello World {num}</h1>"


@app.route("/test_add_user", methods=["GET"])
def test_add_user():
    user = User(idperson=1, username="dima", name="Dmytro"
               ,surname="Sliusarchuk", city="Lviv", email="dmitroslusarcuk@gmail.com"
              , password="qwerty1234", phone="+380673530318", role="Admin")

    user.save_to_db()

    return {"messege": "user was successfully created"}
