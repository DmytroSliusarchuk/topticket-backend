from flask import jsonify
from marshmallow import Schema, fields, validate, post_load

from backend.app import db


class Ticket(db.Model):
    __tablename__ = "ticket"
    idticket = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.DECIMAL(6, 2), nullable=False)
    is_bought = db.Column(db.Boolean, nullable=False)
    is_booked = db.Column(db.Boolean, nullable=False)

    iduser = db.Column(db.Integer(), db.ForeignKey('user.iduser', ondelete='CASCADE'))
    idevent = db.Column(db.Integer(), db.ForeignKey('event.idevent', ondelete='CASCADE'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update_by_id(cls, ticket_data):
        ticket = cls.query.get(ticket_data['idticket'])
        ticket.seat_number = ticket_data['seat_number']
        ticket.price = ticket_data['price']
        ticket.is_bought = ticket_data['is_bought']
        ticket.is_booked = ticket_data['is_booked']
        if "iduser" in ticket_data:
            ticket.iduser = ticket_data["iduser"]
        ticket.idevent = ticket_data['idevent']
        ticket.save_to_db()

    @classmethod
    def find_by_id(cls, ticket_id):
        return cls.query.filter_by(idticket=ticket_id).first()

    @classmethod
    def delete_by_id(cls, ticketid):
        if cls.query.get(ticketid):
            cls.query.filter_by(idticket=ticketid).delete()
            db.session.commit()
            return jsonify({'message': f'Ticket with id={ticketid} was successfully deleted'})
        return jsonify({'error': f'Ticket with id={ticketid} does not exist!'}), 404


class TicketSchema(Schema):
    idticket = fields.Integer(required=False)
    seat_number = fields.Integer(validate=validate.Range(min=1), required=True)
    price = fields.Decimal(validate=validate.Range(min=0), required=True)
    is_bought = fields.Boolean(required=True)
    is_booked = fields.Boolean(required=True)
    iduser = fields.Integer(required=False)
    idevent = fields.Integer(required=True)

    @post_load(pass_original=True)
    def make_ticket(self, data, conf, **kwargs):
        if conf.get("upd", 0):
            return True
        return Ticket(**data)
