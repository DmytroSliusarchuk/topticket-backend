from backend.app import db
from marshmallow import Schema, fields, validate, post_load


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
        try:
            ticket = cls.query.filter_by(idticket=ticket_data['idticket']).first()
            ticket.seat_number = ticket_data['seat_number']
            ticket.price = ticket_data['price']
            ticket.is_bought = ticket_data['is_bought']
            ticket.is_booked = ticket_data['is_booked']
            ticket.iduser = ticket_data['iduser']
            ticket.idevent = ticket_data['idevent']
            db.session.commit()
            return "user was updated"
        except:
            return "Something went wrong"

    @classmethod
    def find_by_id(cls, ticket_id):
        return cls.query.filter_by(idticket=ticket_id).first()

    @classmethod
    def delete_by_id(cls, ticket_id):
        try:
            cls.query.filter_by(idticket=ticket_id).delete()
            db.session.commit()
            return "Ticket was deleted"
        except:
            return "Something went wrong"

    @classmethod
    def get_all_by_eventid(cls, event_id):
        return cls.query.filter_by(idevent=event_id).all()

    @classmethod
    def get_all_by_userid(cls, user_id):
        return cls.query.filter_by(iduser=user_id).all()

    @classmethod
    def buy_ticket(cls, ticket_data):
        ticket = cls.query.filter_by(seat_number=ticket_data['seat_number']).filter_by(
            idevent=ticket_data['idevent']).first()
        if ticket.is_booked or ticket.is_bought:
            return "This seat is taken"
        else:
            ticket.iduser = ticket_data['iduser']
            ticket.is_bought = 1
            db.session.commit()
            return "Ticket was bought"

    @classmethod
    def book_ticket(cls, ticket_data):
        ticket = cls.query.filter_by(seat_number=ticket_data['seat_number']).filter_by(
            idevent=ticket_data['idevent']).first()
        if ticket.is_booked or ticket.is_bought:
            return "This seat is taken"
        else:
            ticket.iduser = ticket_data['iduser']
            ticket.is_booked = 1
            db.session.commit()
            return "Ticket was booked"


class TicketSchema(Schema):
    idticket = fields.Integer(required=False)
    seat_number = fields.Integer(required=True)
    price = fields.Decimal(required=True)
    is_bought = fields.Boolean(required=True)
    is_booked = fields.Boolean(required=True)
    iduser = fields.Integer(required=False)
    idevent = fields.Integer(required=True)

    @post_load
    def make_event(self, data, **kwargs):
        return Ticket(**data)
