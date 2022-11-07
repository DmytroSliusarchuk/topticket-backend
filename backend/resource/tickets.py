from backend.app import app
from backend.models.ticket import Ticket, TicketSchema
from backend.models.event import Event
from backend.models.user import User
from flask import jsonify, request
from marshmallow import ValidationError, EXCLUDE


@app.route("/ticket", methods=["POST"])
def create_ticket():
    ticket_data = request.get_json()

    schema = TicketSchema()

    try:
        ticket = schema.load(ticket_data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 400

    event = Event.query.get(ticket_data["idevent"])

    if not event:
        return jsonify({"Error": f"Event with id {ticket_data['idevent']} not found."}), 404

    if ticket_data["seat_number"] in [tick.seat_number for tick in
                                      Ticket.query.filter_by(idevent=ticket_data['idevent']).all()]:
        return jsonify({"Error": f"Ticket for seat {ticket_data['seat_number']} was already created."}), 402

    if ticket_data["seat_number"] > event.max_visitors:
        return jsonify({"Error": f"Event has only {event.max_visitors} seats."}), 402

    event.tickets.append(ticket)

    ticket.save_to_db()
    result = schema.dump(ticket)

    return jsonify(result)


@app.route('/ticket', methods=['PUT'])
def update_ticket():
    ticket_data = request.get_json()
    ticket_data["upd"] = 1

    if Ticket.query.get(ticket_data["idticket"]):

        schema = TicketSchema()

        try:
            schema.load(ticket_data, unknown=EXCLUDE)
        except ValidationError as err:
            return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 400

        event = Event.query.get(ticket_data["idevent"])

        if not event:
            return jsonify({"Error": f"Event with id {ticket_data['idevent']} not found."}), 404

        if ticket_data["seat_number"] in [tick.seat_number for tick in
                                          Ticket.query.filter_by(idevent=ticket_data['idevent']).all()]:
            return jsonify({"Error": f"Ticket for seat {ticket_data['seat_number']} was already created."}), 402

        if ticket_data["seat_number"] > event.max_visitors:
            return jsonify({"Error": f"Event has only {event.max_visitors} seats."}), 402

        Ticket.update_by_id(ticket_data)

        return jsonify({"Message": "Ticket was updated"})
    else:
        return jsonify({"Error": f"Ticket with id={ticket_data['idticket']} not found"}), 404


@app.route('/ticket/<idticket>', methods=['GET'])
def get_ticket_by_id(idticket: int):
    ticket = Ticket.find_by_id(idticket)
    if not ticket:
        return jsonify({"Error": f"Ticket with id={idticket} not found"}), 404
    schema = TicketSchema()
    result = schema.dump(ticket)
    return jsonify(result)


@app.route('/ticket/<idticket>', methods=['DELETE'])
def delete_ticket_by_id(idticket: int):
    return Ticket.delete_by_id(idticket)


@app.route('/tickets/<idevent>', methods=['GET'])
def get_all_tickets_by_eventid(idevent: int):
    tickets = Event.query.get(idevent).tickets
    if not tickets:
        return jsonify({"Error": f"There are no tickets with that event ID"}), 404
    result = []
    for ticket in tickets:
        schema = TicketSchema()
        result.append(schema.dump(ticket))

    return jsonify(result)


@app.route('/tickets/user/<iduser>', methods=['GET'])
def get_all_tickets_by_userid(iduser: int):
    tickets = User.query.get(iduser).tickets
    if not tickets:
        return jsonify({"Error": f"There are no tickets with that user ID"}), 404
    result = []
    for ticket in tickets:
        schema = TicketSchema()
        result.append(schema.dump(ticket))

    return jsonify(result)


@app.route('/ticket/buy', methods=['PUT'])
def buy_ticket():
    ticket_data = request.get_json()

    ticket = Ticket.query.filter_by(seat_number=ticket_data['seat_number']).filter_by(
        idevent=ticket_data['idevent']).first()
    if ticket:
        if ticket.is_bought or (ticket.is_booked and ticket.iduser != ticket_data['iduser']):
            return jsonify({"Error": "This seat is taken"}), 402
        user = User.query.get(ticket_data['iduser'])
        ticket.iduser = ticket_data['iduser']
        ticket.is_bought = 1
        user.tickets.append(ticket)
        ticket.save_to_db()
        return jsonify({"Message": "Ticket was bought"})
    return jsonify({
        "Error": f"Ticket with eventid={ticket_data['idevent']} or seat with number={ticket_data['seat_number']} not found"}), 404


@app.route('/ticket/book', methods=['PUT'])
def book_ticket():
    ticket_data = request.get_json()
    ticket = Ticket.query.filter_by(seat_number=ticket_data['seat_number']).filter_by(
        idevent=ticket_data['idevent']).first()
    if ticket:
        if ticket.is_booked or ticket.is_bought:
            return jsonify({"Error": "This seat is taken"}), 402
        else:
            user = User.query.get(ticket_data['iduser'])
            ticket.iduser = ticket_data['iduser']
            ticket.is_booked = 1
            user.tickets.append(ticket)
            ticket.save_to_db()
            return jsonify({"Message": "Ticket was booked"})
    return jsonify({
        "Error": f"Ticket with eventid={ticket_data['idevent']} or seat with number={ticket_data['seat_number']} not found"}), 404


@app.route('/ticket/cancel_book', methods=['PUT'])
def cancel_book_ticket():
    ticket_data = request.get_json()
    ticket = Ticket.query.filter_by(seat_number=ticket_data['seat_number']).filter_by(
        idevent=ticket_data['idevent']).first()
    if ticket:
        if not ticket.is_booked or ticket.iduser != ticket_data['iduser']:
            return jsonify({"Error": "You did not book this seat"}), 402
        else:
            user = User.query.get(ticket_data['iduser'])
            user.tickets.remove(ticket)

            ticket.iduser = None
            ticket.is_booked = 0
            ticket.save_to_db()
            return jsonify({"Message": "Booking was canceled"})
    return jsonify({
        "Error": f"Ticket with eventid={ticket_data['idevent']} or seat with number={ticket_data['seat_number']} not found"}), 404
