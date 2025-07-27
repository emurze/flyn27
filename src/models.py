from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Entry(db.Model):
    """Database model representing a single entry."""

    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        """Returns a string representation of the Entry instance."""
        return f"<Entry id={self.id} name={self.name} date={self.date}>"
