from backend.tests.conftest import app_with_data, flask_login, app_with_db
from backend.app import bcrypt
from backend.app import db
from backend.models.user import User

def test_get(app_with_data, flask_login):
    res = app_with_data.get("/user/username/dimalogin", headers=flask_login)

    assert res.status_code == 200

    data = res.json

    assert data["username"] == "dimalogin"
    assert data["phone"] == "+380873837915"
    # assert bcrypt.check_password_hash("12345678", data["password"]) Не працює чомусь


def test_register(app_with_db):
    res = app_with_db.post("/user/register", json={
    "username": "dimalogin2",
    "name": "Dmytro",
    "surname": "Sliusarchuk",
    "city": "Lviv",
    "email": "dmiotril@gmail.com",
    "password": "65432101",
    "phone": "+380873937915"
})

    assert res.status_code == 200
    assert db.session.query(User).first().username == "dimalogin2"


