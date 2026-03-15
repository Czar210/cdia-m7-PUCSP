from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timedelta

from config import settings


class ReservaInput(BaseModel):
    mesa: int = Field(ge=1, le=20)
    nome: str = Field(min_length=2, max_length=100)
    pessoas: int = Field(ge=1, le=10)
    data_hora: datetime

    @field_validator("data_hora")
    def must_be_in_future_with_minimum(cls, v: datetime) -> datetime:
        min_delta = timedelta(hours=settings.RESERVATION_MIN_HOURS)
        now = datetime.now()
        if v < now + min_delta:
            raise ValueError(
                f"`data_hora` must be at least {settings.RESERVATION_MIN_HOURS} hour(s) in the future"
            )
        return v


class ReservaOutput(BaseModel):
    id: int
    mesa: int
    nome: str
    pessoas: int
    data_hora: str
    ativa: bool
    criada_em: str
