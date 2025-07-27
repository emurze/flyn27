from datetime import datetime

from pydantic import BaseModel, field_validator


class EntryRead(BaseModel):
    name: str
    date: datetime

    @field_validator("name")
    def name_must_be_short(cls, v: str) -> str:
        if len(v.strip()) == 0:
            raise ValueError("Имя не может быть пустым.")
        if len(v) >= 50:
            raise ValueError("Имя слишком длинное (>=50 символов).")
        return v
