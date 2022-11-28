from backend.tests.conftest import app_with_data, flask_login, app_with_db
from backend.app import bcrypt
from backend.app import db
from backend.models.user import User


def test_register(app_with_db):
    res = app_with_db.post("/user/register", json={
    "username": "dimalogin2",
    "name": "Dmytro",
    "surname": "Sliusarchuk",
    "city": "Lviv",
    "email": "dmiofril@gmail.com",
    "password": "65432101",
    "phone": "+380873974615"
})

    assert res.status_code == 200
    assert db.session.query(User).first().username == "dimalogin2"


def test_login(app_with_data):
    res = app_with_data.post("/user/login", json={
    "username": "dimalogin",
    "password": "12345678"
})

    assert res.status_code == 200

    data = res.json

    assert data["message"] == "Logged in as dimalogin"


def test_get_by_id(app_with_data, flask_login):
    res = app_with_data.get("/user/12", headers=flask_login)

    assert res.status_code == 200

    data = res.json

    assert data["name"] == "Dmytro"


def test_get_by_username(app_with_data, flask_login):
    res = app_with_data.get("/user/username/dimalogin", headers=flask_login)

    assert res.status_code == 200

    data = res.json

    assert data["name"] == "Dmytro"
    assert data["username"] == "dimalogin"
    assert data["phone"] == "+380873837915"


def test_user_delete(app_with_data, flask_login):
    res = app_with_data.delete("/user/14", headers=flask_login)

    assert res.status_code == 200
    assert len(db.session.query(User).all()) == 0


def test_register_ValidationError(app_with_db):
    res = app_with_db.post("/user/register", json={
    "username": "dimalogin2",
    "name": "Dmytro",
    "surname": "Sliusarchuk",
    "city": "Lviv",
    "email": None,
    "password": "65432101",
    "phone": "+380873937915"
})

    assert res.status_code == 400


def test_login_username_error(app_with_data):
    res = app_with_data.post("/user/login", json={
    "iduser": 1,
    "username": None,
    "name": "Dmytro",
    "surname": "Sliusarchuk",
    "city": "Lviv",
    "email": "dmiotrils@gmail.com",
    "password": "12345678",
    "phone": "+380873837915"
})

    assert res.status_code == 404


def test_login_password_error(app_with_data):
    res = app_with_data.post("/user/login", json={
    "iduser": 1,
    "username": "dimalogin",
    "name": "Dmytro",
    "surname": "Sliusarchuk",
    "city": "Lviv",
    "email": "dmiotrils@gmail.com",
    "password": "372464872",
    "phone": "+380873837915"
})

    assert res.status_code == 403


def test_error_update_user_by_username(app_with_data, flask_login):
    res = app_with_data.put('/user', json={
    "username": "dimalogin",
    "name": "Dmytro",
    "surname": "Sliusarchuk",
    "city": "Lviv",
    "email": "dmiotrils@gmail.com",
    "password": "372464872",
    "phone": "+380873837915"}, headers=flask_login)
    assert res.status_code == 400


def test_error_update_user_by_username2(app_with_data, flask_login):
    res = app_with_data.put('/user', json={
    "username": "dimafrgfn",
    "name": "Dmytro",
    "surname": "Slifgdrchuk",
    "city": "Lviv",
    "email": "dmiotrils@gmail.com",
    "password": "372464872",
    "phone": "+380873837915"}, headers=flask_login)
    assert res.status_code == 404


