from backend.tests.conftest import app_with_data, flask_login, app_with_db, flask_login_admin, app_with_data_admin
from backend.app import bcrypt
from backend.app import db
from backend.models.event import Event


def test_get_all_events(app_with_data, flask_login):
    res = app_with_data.get('/event', headers=flask_login)
    assert res.status_code == 200


def test_error_create_event(app_with_data_admin):
    res = app_with_data_admin.post("/event", json={
    "name": "halloween2",
    "city": "Lviv2",
    "address": "Gorodatska2",
    "date": "2022-02-02",
    "max_visitors": 2})
    assert res.status_code == 401


def test_get_event_by_id(app_with_data, flask_login):
    res = app_with_data.get("/event/3", headers=flask_login)
    assert res.status_code == 200


def test_error_get_event_by_id(app_with_data, flask_login):
    res = app_with_data.get("/event/1", headers=flask_login)
    assert res.status_code == 404


def test_delete_event_by_id(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.delete("/event/5", headers=flask_login_admin)
    assert res.status_code == 200
