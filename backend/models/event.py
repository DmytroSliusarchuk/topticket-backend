from backend.app import db
from marshmallow import Schema, fields, validate, post_load


class Event(db.Model):
    __tablename__ = "event"
    idevent = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    max_visitors = db.Column(db.Integer, nullable=False)

    tickets = db.relationship('Ticket', backref='event', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, event_id):
        return cls.query.filter_by(idevent=event_id).first()

    @classmethod
    def delete_by_id(cls, event_id):
        try:
            cls.query.filter_by(idevent=event_id).delete()
            db.session.commit()
            return "user was deleted"
        except:
            return "Something went wrong"

    @classmethod
    def update_by_id(cls, event_data):
        try:
            event = cls.query.filter_by(idevent=event_data['idevent']).first()
            event.name = event_data['name']
            event.description = event_data['description']
            event.city = event_data['city']
            event.address = event_data['address']
            event.date = event_data['date']
            event.max_visitors = event_data['max_visitors']
            db.session.commit()
            return "user was updated"
        except:
            return "Something went wrong"


class EventSchema(Schema):
    idevent = fields.Integer(required=False)
    name = fields.Str(validate=validate.Length(min=1, max=45), required=True)
    description = fields.Str(required=False)
    city = fields.Str(validate=validate.Length(min=1, max=45), required=True)
    address = fields.Str(validate=validate.Length(min=1, max=100), required=True)
    date = fields.DateTime(required=True)
    max_visitors = fields.Integer(required=True)

    @post_load
    def make_event(self, data, **kwargs):
        return Event(**data)
