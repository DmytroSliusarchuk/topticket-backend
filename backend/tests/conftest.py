import pytest

from backend.app import app, db, bcrypt
from backend.models.user import User
from sqlalchemy import delete


@pytest.fixture(scope="session")
def flask_app():
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope="session")
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture
def app_with_data(app_with_db):
    user = User(username="dimalogin",
                name="Dmytro",
                surname="Sliusarchuk",
                city="Lviv",
                email="dmiotrils@gmail.com",
                password=bcrypt.generate_password_hash(password="12345678"),
                phone="+380873837915")

    db.session.add(user)

    db.session.commit()

    yield app_with_db

    db.session.execute(delete(User))
    db.session.commit()


@pytest.fixture()
def flask_login(app_with_data):
    res = app_with_data.post("/user/login", json={"username": "dimalogin", "password": "12345678"})

    jwt = res.json["access_token"]
    return {"Authorization":f"Bearer {jwt}"}
