from backend.app import db


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
