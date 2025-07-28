from datetime import datetime

from pydantic import BaseModel, field_validator


class EntryRead(BaseModel):
    """
    Class representing a single entry with validation for name and date fields.
    """

    name: str
    date: datetime

    @field_validator("name")
    def name_must_be_short(cls, v: str) -> str:
        """Validates that the 'name' field is not empty or too long."""
        if len(v.strip()) == 0:
            raise ValueError("Name cannot be empty.")
        if len(v) >= 50:
            raise ValueError("Name is too long (>= 50 characters).")
        return v

    @field_validator("date", mode="before")
    def parse_custom_date_format(cls, v: str) -> datetime:
        """Parses 'date' from 'YYYY-MM-DD_HH:mm' format."""
        try:
            return datetime.strptime(v, "%Y-%m-%d_%H:%M")
        except Exception:
            raise ValueError("Date must be in 'YYYY-MM-DD_HH:mm' format.")
