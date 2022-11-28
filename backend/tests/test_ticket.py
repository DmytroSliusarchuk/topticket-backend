from backend.tests.conftest import app_with_data, flask_login, app_with_db, flask_login_admin, app_with_data_admin
from backend.app import bcrypt
from backend.app import db
from backend.models.ticket import Ticket


def test_get_ticket_by_id(app_with_db, flask_login):
    res = app_with_db.get('/ticket/6', headers=flask_login)
    assert res.status_code == 200


def test_error_create_ticket(app_with_data_admin):
    res = app_with_data_admin.post("/ticket", json={
        "seat_number": 1,
        "price": 3000.99,
        "is_bought": 1,
        "is_booked": 1
    })

    assert res.status_code == 401


def test_delete_ticket_by_id(app_with_db, flask_login):
    res = app_with_db.get('/ticket/8', headers=flask_login)
    assert res.status_code == 200


def test_error_update_ticket(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.put("/ticket", json={
        "idticket": 5,
        "seat_number": 1,
        "price": 3000.99,
        "is_bought": 0,
        "is_booked": 1
    }, headers=flask_login_admin)
    assert res.status_code == 404
