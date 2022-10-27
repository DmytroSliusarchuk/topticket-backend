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
