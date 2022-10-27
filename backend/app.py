from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from waitress import serve


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345@localhost/dimadb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    print("http://127.0.0.1:8080")
    serve(app, host='127.0.0.1', port=8080)
