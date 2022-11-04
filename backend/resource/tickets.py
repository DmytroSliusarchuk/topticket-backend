from backend.app import app
from backend.models.ticket import Ticket, TicketSchema
from flask import jsonify, request
from marshmallow import ValidationError


@app.route("/ticket", methods=["POST"])
def create_ticket():
    ticket_data = request.get_json()

    schema = TicketSchema()

    try:
        ticket = schema.load(ticket_data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 405

    ticket.save_to_db()
    result = schema.dump(ticket)

    return jsonify(result)


@app.route('/ticket', methods=['PUT'])
def update_ticket():
    ticket_data = request.get_json()

    schema = TicketSchema()
    try:
        ticket = schema.load(ticket_data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 405

    try:
        ticket.update_by_id(ticket_data)
        return jsonify({"Message": "Event was updated"})
    except:
        return jsonify({"Error": f"Event with id={ticket_data['idticket']} not found"}), 404


@app.route('/ticket/<idticket>', methods=['GET'])
def get_ticket_by_id(idticket: int):
    event = Ticket.find_by_id(idticket)
    if not event:
        return jsonify({"Error": f"Ticket with id={idticket} not found"}), 404
    schema = TicketSchema()
    result = schema.dump(event)
    return jsonify(result)


@app.route('/ticket/<idticket>', methods=['DELETE'])
def delete_ticket_by_id(idticket: int):
    try:
        Ticket.delete_by_id(idticket)
        return jsonify({"Message": "Ticket was deleted"})
    except:
        return jsonify({"Error": f"Ticket with id={idticket} not found"}), 404


@app.route('/tickets/<idevent>', methods=['GET'])
def get_all_tickets_by_eventid(idevent: int):
    tickets = Ticket.get_all_by_eventid(idevent)
    if not tickets:
        return jsonify({"Error": f"There are no tickets with that event ID"}), 404
    result = []
    for ticket in tickets:
        schema = TicketSchema()
        result.append(schema.dump(ticket))

    return jsonify(result)


@app.route('/tickets/user/<iduser>', methods=['GET'])
def get_all_tickets_by_userid(iduser: int):
    tickets = Ticket.get_all_by_userid(iduser)
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

    try:
        return Ticket.buy_ticket(ticket_data)
    except:
        return jsonify({"Error": f"Ticket with eventid={ticket_data['idevent']} not found"}), 404


@app.route('/ticket/book', methods=['PUT'])
def book_ticket():
    ticket_data = request.get_json()

    try:
        return Ticket.book_ticket(ticket_data)
    except:
        return jsonify({"Error": f"Ticket with eventid={ticket_data['idevent']} not found"}), 404
