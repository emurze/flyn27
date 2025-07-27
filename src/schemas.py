from datetime import datetime

from pydantic import BaseModel, field_validator


class EntryRead(BaseModel):
    name: str
    date: datetime

    @field_validator("name")
    def name_must_be_short(cls, v: str) -> str:
        if len(v.strip()) == 0:
            raise ValueError("Name cannot be empty.")
        if len(v) >= 50:
            raise ValueError("Name is too long (>= 50 characters).")
        return v

    @field_validator("date", mode="before")
    def parse_custom_date_format(cls, v: str) -> datetime:
        try:
            return datetime.strptime(v, "%Y-%m-%d_%H:%M")
        except Exception:
            raise ValueError("Date must be in 'YYYY-MM-DD_HH:mm' format.")
