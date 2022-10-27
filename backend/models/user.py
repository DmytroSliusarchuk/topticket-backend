from backend.app import db


class User(db.Model):
    __tablename__ = "user"
    iduser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    role = db.Column(db.Enum("User", "Admin"), nullable=False)

    tickets = db.relationship('Ticket', backref='user', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
