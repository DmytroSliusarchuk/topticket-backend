from backend.app import db
from marshmallow import Schema, fields, validate, post_load


class User(db.Model):
    __tablename__ = "user"
    iduser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    role = db.Column(db.Enum("User", "Admin"), nullable=False, default="User")

    tickets = db.relationship('Ticket', backref='user', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(username=phone).first()

    @classmethod
    def delete_by_username(cls, username):
        try:
            cls.query.filter_by(username=username).delete()
            db.session.commit()
            return "user was deleted"
        except:
            return "Something went wrong"

    @classmethod
    def update_by_username(cls, username, user_data):
        try:
            user = cls.query.filter_by(username=username).first()
            user.name = user_data['name']
            user.surname = user_data['surname']
            user.city = user_data['city']
            user.email = user_data['email']
            user.password = user_data['password']
            user.phone = user_data['phone']
            db.session.commit()
            return "user was updated"
        except:
            return "Something went wrong"


class UserSchema(Schema):
    iduser = fields.Integer(required=False)
    username = fields.Str(validate=validate.Length(min=1, max=30), required=True)
    name = fields.Str(validate=validate.Length(min=1, max=30), required=True)
    surname = fields.Str(validate=validate.Length(min=1, max=45), required=True)
    city = fields.Str(validate=validate.Length(min=1, max=45), required=True)
    email = fields.Email(validate=validate.Length(min=1, max=45), required=True)
    password = fields.Str(required=True)
    phone = fields.Str(validate=validate.Regexp(r'^\+[0-9]{12}$'), required=True)
    role = fields.Str(validate=validate.OneOf(['User', 'Admin']), required=False)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
