from sqlalchemy import select

from models import Entry, db
from schemas import EntryRead


def upload_entries(validated_entries: list[EntryRead]) -> None:
    """Save a list of validated entries to the database."""
    entries = [
        Entry(name=entry.name, date=entry.date) for entry in validated_entries
    ]
    db.session.add_all(entries)
    db.session.commit()


def get_entries() -> list[Entry]:
    """Retrieve all entries from the database."""
    query = select(Entry)
    res = db.session.execute(query)
    return list(res.scalars())
