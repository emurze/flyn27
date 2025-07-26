from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Record(db.Model):  # TODO: rename, declarative style
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
